"""Read-only real-worktree doctor and independent-worker failure boundaries."""
import copy
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
import test_numbered_queue as fixtures

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('worker_doctor', BASE/'scripts/worker_doctor.py')
doctor = importlib.util.module_from_spec(spec); spec.loader.exec_module(doctor)


class WorkerDoctorTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.NumberedQueueTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.f.card(); self.now = datetime.datetime.now(datetime.timezone.utc)
        self.binding = dict(schema_version=1, mode='simulation', observed_at=self.now.isoformat(),
            host='claude', host_version='2.1.318', provider='fixture',
            capabilities={'ListAgents':True,'SendMessage':True}, capability_reference='simulated tool observation',
            human_authority_reference='fixture authorization, not a real user grant', inbound='accept', transport='not_attempted')
        for role, root in [('plan',self.f.plan),('dev',self.f.dev)]:
            self.binding[role] = dict(role=role,role_reference='fixture explicit '+role,session_id=role+'-fixture',
                host_id='local',worktree=str(root),session_cwd=str(root),writer_count=1,status='idle')

    def check(self, binding=None, inventory=None):
        return doctor.diagnose(self.f.dev,self.binding if binding is None else binding,inventory,self.now)

    def test_no_network_or_mutation_and_simulation_never_live(self):
        def hashes():
            return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for root in [self.f.plan,self.f.dev]
                    for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}
        before=hashes(); result=self.check(); self.assertEqual(result['dispatch'],'simulation_only')
        self.assertEqual(before,hashes()); self.assertFalse(result['performs_actions'])
        self.assertNotIn('plan-fixture',json.dumps(result)); self.assertEqual(result['next_dev'],'P001')
        self.assertEqual(doctor.diagnose(self.f.dev)['dispatch'],'pending')
        self.assertEqual((self.f.plan/'scripts/worker_doctor.py').read_bytes(),(BASE/'scripts/worker_doctor.py').read_bytes())

    def test_identity_project_branch_writer_and_capability_fail_closed(self):
        cases=[]
        b=copy.deepcopy(self.binding);b['dev']['session_id']=b['plan']['session_id'];cases.append((b,'same_session'))
        b=copy.deepcopy(self.binding);b['dev']['worktree']=str(self.f.plan);cases.append((b,'same_worktree'))
        b=copy.deepcopy(self.binding);b['dev']['writer_count']=2;cases.append((b,'dev_writer_unconfirmed_or_conflicting'))
        b=copy.deepcopy(self.binding);b['dev']['writer_count']=True;cases.append((b,'dev_writer_unconfirmed_or_conflicting'))
        b=copy.deepcopy(self.binding);b['capabilities']['SendMessage']=False;cases.append((b,'native_tools_unconfirmed'))
        b=copy.deepcopy(self.binding);b['human_authority_reference']='';cases.append((b,'human_authority_unconfirmed'))
        foreign=self.f.root/'foreign';subprocess.run(['git','init','-b','develop',str(foreign)],capture_output=True,check=True)
        b=copy.deepcopy(self.binding);b['dev']['worktree']=str(foreign);cases.append((b,'dev_wrong_project'))
        for b,issue in cases:
            with self.subTest(issue=issue):
                r=self.check(b);self.assertEqual(r['dispatch'],'pending');self.assertIn(issue,r['issues'])

    def test_inventory_absence_ambiguity_and_reconnection(self):
        row={'sessionId':'dev-fixture','cwd':str(self.f.dev)}
        for inventory in [[],[row,row],[{'sessionId':'dev-fixture','cwd':str(self.f.plan)}]]:
            self.assertEqual(self.check(inventory=inventory)['dispatch'],'pending')
        b=copy.deepcopy(self.binding);b['mode']='host_observation'
        b['observed_at']=(self.now-datetime.timedelta(minutes=6)).isoformat()
        self.assertIn('observation_stale_or_future',self.check(b)['issues'])
        b['observed_at']=self.now.isoformat();b['dev']['session_id']='reconnected'
        self.assertEqual(self.check(b,[row])['dispatch'],'pending')
        inventory=[{'sessionId':'plan-fixture','cwd':str(self.f.plan)},{'sessionId':'reconnected','cwd':str(self.f.dev)}]
        result=self.check(b,inventory);self.assertEqual(result['dispatch'],'preflight_consistent')
        self.assertIn('not_independently_authenticated',result['binding_evidence'])

    def test_held_refused_unknown_and_busy_do_not_start_or_fallback(self):
        self.binding['dev']['status']='busy'
        for outcome in ['held','refused','unknown','failed']:
            self.binding['transport']=outcome;r=self.check()
            self.assertEqual(r['dispatch'],'pending');self.assertEqual(r['execution'],'defer_to_safe_boundary')
            self.assertIn('no_plan_implementation_fallback',r['notes']);self.assertIn('do_not_retry_unknown_send',r['notes'])
        self.binding['transport']='sent';self.assertEqual(self.check()['execution'],'defer_to_safe_boundary')

    def test_existing_pause_and_open_are_not_cleared(self):
        self.f.run_cmd('python3','scripts/workflow_control.py','pause','--request','Fixture stop',cwd=self.f.dev)
        paused=self.check();self.assertEqual(paused['paused_sessions'],1);self.assertIsNone(paused['next_dev'])
        self.f.run_cmd('python3','scripts/workflow_control.py','resume','--request','Fixture explicit resume',cwd=self.f.dev)
        q=self.f.root/'question.txt';q.write_text('Fixture question, no human answer invented.')
        self.f.run_cmd('python3','scripts/workflow_control.py','decision','--task','P001','--question-file',str(q),cwd=self.f.dev)
        before=list((self.f.dev/'docs/feedback/dev').glob('*.md'))[0].read_bytes();r=self.check()
        self.assertEqual(r['pending_decisions'],1);self.assertIsNone(r['next_dev'])
        self.assertEqual(before,list((self.f.dev/'docs/feedback/dev').glob('*.md'))[0].read_bytes())

    def test_cli_inventory_failure_is_unknown_and_codex_keeps_adapter(self):
        b=copy.deepcopy(self.binding);b['host']='codex';b['capabilities']={n:True for n in ['list_threads','read_thread','send_message_to_thread']}
        self.assertEqual(self.check(b)['dispatch'],'simulation_only')
        self.assertIn('inventory_host_mismatch',self.check(b,[])['issues'])
        with patch.object(doctor,'command',side_effect=ValueError('blocked')), patch.object(doctor,'diagnose',return_value={'dispatch':'preflight_consistent','issues':[],'notes':[],'execution':'unknown'}), patch('builtins.print') as out:
            self.assertEqual(doctor.main(['--repo',str(self.f.dev),'--claude-inventory','--json']),0)
            self.assertEqual(json.loads(out.call_args.args[0])['host_inventory'],'unavailable_in_this_execution_environment')
