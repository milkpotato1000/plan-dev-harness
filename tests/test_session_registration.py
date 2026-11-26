"""Real isolated worktrees; lifecycle simulations are deliberately not live-host evidence."""
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import unittest
from unittest.mock import patch
import test_numbered_queue as fixtures

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'scripts'))
import session_registry as reg
import configure_sessions as setup
import session_handoff as handoff


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.NumberedQueueTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.now=dt.datetime.now(dt.timezone.utc)
        self.args=(self.f.plan,self.f.dev,'fixture explicit roles')
        setup.install(*self.args,apply=True)
        self.directory=reg.config_for(self.f.plan)[1]

    def event(self,role='plan',sid=None,event='SessionStart',host='claude',**kw):
        root=getattr(self.f,role);payload=dict(session_id=sid or role+'-one',cwd=str(root),hook_event_name=event)
        return reg.lifecycle(root,role,host,payload,now=kw.pop('now',self.now),**kw)

    def rows(self,dev='dev-one'):
        return [dict(sessionId='plan-one',cwd=str(self.f.plan),status='idle'),dict(sessionId=dev,cwd=str(self.f.dev),status='busy')]

    def test_start_order_late_peer_and_idempotent_resume(self):
        self.event('dev');a=reg.diagnose(self.f.dev,'claude',self.rows(),self.now)
        self.assertIn('plan_missing',a['issues'])
        first=self.event();self.event('dev',event='UserPromptSubmit');same=self.event()
        self.assertEqual(first['generation'],same['generation'])
        a=reg.diagnose(self.f.dev,'claude',self.rows(),self.now)
        self.assertEqual(a['dispatch'],'identity_consistent');self.assertFalse(a['performs_actions'])
        self.assertEqual(a['peers']['dev']['state'],'busy');self.assertNotIn('plan-one',json.dumps(a))

    def test_restart_requires_end_and_positive_inventory_not_ttl(self):
        self.event();self.event('dev')
        late=self.now+dt.timedelta(hours=1)
        r=self.event('dev','dev-two',now=late,inventory=self.rows('dev-two'))
        self.assertEqual(r['status'],'writer_conflict')
        self.event('dev','dev-two',event='SessionEnd',now=late)
        self.event('dev',event='SessionEnd',now=late)
        self.assertEqual(self.event('dev','dev-two',now=late,inventory=[])['status'],'replacement_host_proof_required')
        self.assertEqual(self.event('dev','dev-two',now=late,inventory=self.rows())['status'],'replacement_host_proof_required')
        gen=self.event('dev','dev-two',now=late,inventory=self.rows('dev-two'))['generation']
        self.assertEqual(self.event('dev',event='SessionEnd',now=late)['status'],'retired_identity_ignored')
        row=reg.load_registry(self.directory,reg.config_for(self.f.dev)[2])['records']['dev']
        self.assertEqual(row['session_id'],'dev-two');self.assertEqual(row['generation'],gen)

    def test_same_id_closed_resume_positive_proof_and_old_generation(self):
        a=self.event();self.event(event='SessionEnd')
        self.assertEqual(self.event(inventory=[])['status'],'ended_identity_resume_needs_host_review')
        self.assertEqual(self.event(inventory=self.rows())['generation'],a['generation'])
        self.assertEqual(self.event(event='SessionEnd',expected_generation=a['generation']+1)['status'],'stale_generation_ignored')
        self.assertEqual(reg.load_registry(self.directory,reg.config_for(self.f.plan)[2])['records']['plan']['state'],'idle')

    def test_conflict_blocks_dispatch_preserves_busy_and_contender_end(self):
        self.event();self.event('dev');self.event('dev',event='UserPromptSubmit')
        self.event('dev','contender')
        a=reg.diagnose(self.f.dev,'claude',self.rows(),self.now)
        self.assertIn('dev_writer_conflict',a['issues']);self.assertEqual(a['peers']['dev']['state'],'busy')
        self.event('dev','contender',event='SessionEnd')
        self.assertEqual(reg.diagnose(self.f.dev,'claude',self.rows(),self.now)['dispatch'],'identity_consistent')

    def test_other_clone_branch_cwd_host_and_duplicate_names_fail_closed(self):
        self.event();self.event('dev')
        with self.assertRaises(ValueError):reg.lifecycle(self.f.dev,'dev','claude',dict(session_id='x',cwd=str(self.f.plan),hook_event_name='SessionStart'))
        self.assertIn('plan_cross_host_transport_unavailable',reg.diagnose(self.f.plan,'codex',self.rows(),self.now)['issues'])
        duplicate=self.rows()+[dict(sessionId='another',cwd=str(self.f.dev),status='idle',name='same')]
        self.assertIn('dev_multiple_host_writers',reg.diagnose(self.f.plan,'claude',duplicate,self.now)['issues'])
        foreign=self.f.root/'clone';self.f.git('clone',str(self.f.plan),str(foreign),cwd=self.f.root)
        with self.assertRaises(FileNotFoundError):reg.config_for(foreign)
        self.f.git('checkout','-b','wrong-role',cwd=self.f.dev)
        with self.assertRaises(ValueError):self.event('dev')

    def test_malformed_clock_limits_symlink_and_atomic_failure(self):
        self.event();p=self.directory/'registry.json';before=p.read_bytes()
        with self.assertRaises(ValueError):self.event(now=self.now-dt.timedelta(seconds=1))
        self.assertEqual(before,p.read_bytes())
        with patch.object(reg.os,'replace',side_effect=OSError('fixture failure')):
            with self.assertRaises(OSError):self.event('dev')
        self.assertEqual(before,p.read_bytes());self.assertFalse(list(self.directory.glob('.write-*')))
        p.write_text('{bad')
        with self.assertRaises(ValueError):self.event()
        self.assertEqual(p.read_text(),'{bad');p.write_bytes(before)
        r=json.loads(before);r['records']['plan']['generation']='wrong';p.write_text(json.dumps(r))
        with self.assertRaises(ValueError):self.event()
        p.unlink();target=self.f.root/'outside';target.write_bytes(before);p.symlink_to(target)
        with self.assertRaises(ValueError):self.event()
        self.assertEqual(target.read_bytes(),before)

    def test_nonblocking_lock_and_real_competing_processes(self):
        with reg.locked(self.directory):
            with self.assertRaises(ValueError):self.event()
        processes=[]
        for sid in ['concurrent-a','concurrent-b']:
            args=[sys.executable,'-B',str(BASE/'scripts/session_registry.py'),'--repo',str(self.f.dev),'--host','claude','hook','--role','dev']
            p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            p.stdin.write(json.dumps(dict(session_id=sid,cwd=str(self.f.dev),hook_event_name='SessionStart')).encode());p.stdin.close();processes.append(p)
        for p in processes:p.wait(timeout=10)
        row=reg.load_registry(self.directory,reg.config_for(self.f.dev)[2])['records']['dev']
        self.assertIn(row['session_id'],['concurrent-a','concurrent-b'])
        loser='concurrent-b' if row['session_id']=='concurrent-a' else 'concurrent-a'
        self.assertEqual(self.event('dev',loser,now=dt.datetime.now(dt.timezone.utc))['status'],'writer_conflict')
        self.assertEqual(reg.load_registry(self.directory,reg.config_for(self.f.dev)[2])['records']['dev']['session_id'],row['session_id'])
        for p in processes:p.stdout.close();p.stderr.close()

    def test_hook_ignores_sensitive_fields_and_rejects_shell_identity(self):
        p=dict(session_id='actual-test-id',cwd=str(self.f.plan),hook_event_name='SessionStart',prompt='SECRET_FIXTURE',transcript_path='/do/not/read',token='SECRET_FIXTURE')
        reg.lifecycle(self.f.plan,'plan','claude',p)
        self.assertNotIn('SECRET_FIXTURE',(self.directory/'registry.json').read_text())
        self.assertNotIn('transcript',(self.directory/'registry.json').read_text())
        p['session_id']='$(touch /tmp/UNAUTHORIZED)'
        with self.assertRaises(ValueError):reg.lifecycle(self.f.plan,'plan','claude',p)
        self.assertEqual((self.directory/'registry.json').stat().st_mode&0o777,0o600)

    def test_stops_open_current_work_and_readonly_doctor(self):
        self.f.card();self.event();self.event('dev')
        self.f.run_cmd('python3','scripts/workflow_control.py','pause','--request','Fixture human stop',cwd=self.f.dev)
        q=self.f.root/'question';q.write_text('Fixture unresolved decision')
        self.f.run_cmd('python3','scripts/workflow_control.py','decision','--task','P001','--question-file',str(q),cwd=self.f.dev)
        def snap():return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in self.f.dev.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts}
        before=snap();self.event('dev',event='UserPromptSubmit');self.event('dev',event='Stop')
        r=reg.diagnose(self.f.dev,'claude',self.rows(),self.now)
        self.assertEqual(before,snap());self.assertIn('workflow_stops_or_open_require_scoped_review',r['issues']);self.assertIsNone(r['next_dev'])
        raw=(self.directory/'registry.json').read_bytes();reg.diagnose(self.f.dev,'claude',[],self.now);self.assertEqual(raw,(self.directory/'registry.json').read_bytes())

    def test_keep_custom_fields_owned_conflict_and_inline_codex_refusal(self):
        self.assertTrue(all(x['action']=='KEEP' for x in setup.install(*self.args)))
        p=self.f.plan/'.claude/settings.local.json';obj=json.loads(p.read_text());obj['permissions']={'deny':['Bash(rm *)']};obj['futureUserField']={'a':1};p.write_text(json.dumps(obj))
        setup.install(*self.args,apply=True);saved=json.loads(p.read_text());self.assertEqual(saved['permissions'],obj['permissions']);self.assertEqual(saved['futureUserField'],{'a':1})
        self.assertTrue(all(x['action']=='KEEP' for x in setup.install(*self.args,apply=True)))
        saved['hooks']['SessionStart'][0]['hooks'][0]['command']='custom';p.write_text(json.dumps(saved));raw=p.read_bytes()
        with self.assertRaises(ValueError):setup.install(*self.args,apply=True)
        self.assertEqual(raw,p.read_bytes())
        # Nothing can overwrite a customized owned hook to make an upgrade pass.

    def test_hook_command_spaces_unicode_and_no_duplicate_settings(self):
        p=self.f.plan/'.claude/settings.local.json';obj=json.loads(p.read_text());cmd=obj['hooks']['SessionStart'][0]['hooks'][0]['command']
        argv=shlex.split(cmd);self.assertEqual(argv[2],str((self.f.plan/'scripts/session_registry.py').resolve()))
        payload=json.dumps(dict(session_id='from-hook',cwd=str(self.f.plan),hook_event_name='SessionStart'))
        r=subprocess.run(cmd,shell=True,input=payload,text=True,capture_output=True,cwd=self.f.root)
        self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(r.stdout,'')
        self.assertTrue(reg.load_registry(self.directory,reg.config_for(self.f.plan)[2])['records'])
        extra=self.f.plan/'.claude/settings.json';extra.write_text(json.dumps({'hooks':{'SessionStart':[{'hooks':[{'type':'command','command':cmd}]}]}}))
        with self.assertRaises(ValueError):setup.install(*self.args)

    def test_install_partial_failure_rolls_back_owned_changes(self):
        path=self.f.plan/'.claude/settings.local.json';obj=json.loads(path.read_text());obj['userField']=True;path.write_text(json.dumps(obj))
        orig={p:p.read_bytes() for root in [self.f.plan,self.f.dev,self.directory] for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}
        actual=os.replace;count=[0]
        def fail_second(src,dst):
            count[0]+=1
            if count[0]==2:raise OSError('fixture interrupted write')
            return actual(src,dst)
        # Change executable path to require updates in every hook while retaining explicit ownership.
        with patch.object(setup.sys,'executable','/tmp/python fixture 한'),patch.object(setup.os,'replace',side_effect=fail_second):
            with self.assertRaises(OSError):setup.install(*self.args,apply=True)
        for p,raw in orig.items():self.assertEqual(p.read_bytes(),raw,str(p))

    def test_codex_capabilities_and_fresh_observation_envelope(self):
        self.event(host='codex');self.event('dev',host='codex')
        a=reg.diagnose(self.f.plan,'codex',None,self.now);self.assertEqual(a['dispatch'],'pending')
        path=self.f.root/'host.json';path.write_text(json.dumps(dict(host='codex',source='codex_app_tools',observed_at=self.now.isoformat(),sessions=self.rows())))
        self.assertEqual(len(handoff.host_rows(path,'codex',self.now)),2)
        with self.assertRaises(ValueError):handoff.host_rows(path,'codex',self.now+dt.timedelta(seconds=31))
        with self.assertRaises(ValueError):handoff.host_rows(path,'claude',self.now)

    def test_handoff_exact_event_and_queue_unknown_dedup(self):
        self.f.card();self.event(host='codex');self.event('dev',host='codex')
        sha=self.f.git('rev-parse','HEAD');doc='docs/planning/plans/P001.md'
        result=self.f.run_cmd('python3','scripts/workflow_control.py','handoff','--kind','WORK_READY','--target-role','dev','--commit',sha,'--document',doc,'--summary','Fixture handoff','--next-action','Exact adoption')
        event=next((self.f.plan/'docs/progress/handoffs/plan').glob('*.json'))
        self.f.git('add','docs/progress/handoffs/plan');self.f.git('commit','-m','Fixture pending')
        packet=handoff.prepare(self.f.plan,'codex',str(event.relative_to(self.f.plan)),'fixture actual grant',self.rows())
        self.assertEqual(packet['exact_commit'],sha);self.assertNotIn('--resume',packet['action']['cli_argv'])
        with self.assertRaises(ValueError):handoff.prepare(self.f.plan,'codex','../event','reference',self.rows())
        real=subprocess.run
        def fake(args,**kwargs):
            if args[:3]==['codex','queue','--help']:return subprocess.CompletedProcess(args,0,'--thread --message','')
            if args[:2]==['codex','queue']:raise subprocess.TimeoutExpired(args,10)
            return real(args,**kwargs)
        with patch.object(handoff.subprocess,'run',side_effect=fake):
            self.assertEqual(handoff.enqueue(self.f.plan,packet)['status'],'unknown')
            with self.assertRaises(ValueError):handoff.enqueue(self.f.plan,packet)
        self.assertEqual(json.loads(event.read_text())['status'],'PENDING')


    def test_fresh_preview_unicode_shell_paths_inline_hooks_and_configuration_conflict(self):
        parent=self.f.root/'space 한 $(literal)';parent.mkdir()
        args=[sys.executable,str(BASE/'scripts/bootstrap_workspace.py'),'--parent',str(parent),'--name','sample','--author-name','Fixture','--author-email','test@example.invalid','--apply']
        p=subprocess.run(args,capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        plan=parent/'sample/sample_plan';dev=parent/'sample/sample_dev'
        options=setup.install(plan,dev,'fixture role mapping');self.assertTrue(any(x['action']=='CREATE' for x in options))
        directory=reg.repository(plan)[1]/'plan-dev-sessions';self.assertFalse(directory.exists());self.assertFalse((plan/'.claude').exists())
        (plan/'.codex').mkdir();toml=plan/'.codex/config.toml';toml.write_text('[[hooks.SessionStart]]\nmatcher = "startup"\n')
        with self.assertRaises(ValueError):setup.install(plan,dev,'fixture role mapping',apply=True)
        self.assertFalse(directory.exists());toml.write_text('model = "user-choice"\n')
        setup.install(plan,dev,'fixture role mapping',apply=True)
        self.assertEqual(toml.read_text(),'model = "user-choice"\n')
        cmd=json.loads((plan/'.claude/settings.local.json').read_text())['hooks']['SessionStart'][0]['hooks'][0]['command']
        p=subprocess.run(cmd,shell=True,cwd=self.f.root,input=json.dumps(dict(session_id='space-id',cwd=str(plan),hook_event_name='SessionStart')),text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(reg.load_registry(directory,reg.config_for(plan)[2])['records']['plan']['session_id'],'space-id')
        self.assertTrue(all(x['action']=='KEEP' for x in setup.install(plan,dev,'fixture role mapping',apply=True)))
        with self.assertRaises(ValueError):setup.install(plan,dev,'changed unreviewed role reference',apply=True)

    def test_codex_reconnect_entry_uses_official_observation_without_id_argument(self):
        self.event(host='codex');self.event('dev',host='codex');self.event('dev',event='SessionEnd',host='codex')
        path=self.f.root/'host.json';path.write_text(json.dumps(dict(host='codex',source='codex_app_tools',observed_at=dt.datetime.now(dt.timezone.utc).isoformat(),sessions=self.rows('dev-restarted'))))
        p=subprocess.run([sys.executable,'-B',str(BASE/'scripts/session_registry.py'),'--repo',str(self.f.dev),'--host','codex','reconnect','--role','dev','--host-observation',str(path)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['status'],'registered')
        self.assertEqual(reg.load_registry(self.directory,reg.config_for(self.f.dev)[2])['records']['dev']['session_id'],'dev-restarted')


if __name__=='__main__':unittest.main()
