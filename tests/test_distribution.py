"""Actual CLI packaging, cross-agent layout, bootstrap and upgrade integration."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='harness-distribution-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def cmd(self,*args,ok=True,cwd=None):
        r=subprocess.run(args,cwd=cwd or self.root,text=True,capture_output=True)
        self.assertEqual(r.returncode==0,ok,r.stdout+r.stderr)
        return r

    def script(self,name,*args,**kw):
        return self.cmd(sys.executable,str(BASE/'scripts'/name),*args,**kw)

    def repo(self):
        p=self.root/'repo';self.cmd('git','init','-b','plan',str(p))
        self.cmd('git','config','core.hooksPath','.githooks',cwd=p)
        return p

    def install(self,p,*args,**kw):
        return self.script('install_harness.py','--repo',str(p),'--protect','specs','--agent','both',*args,**kw)

    def test_agent_entrypoints_and_idempotence(self):
        p=self.repo();self.install(p,'--apply');self.install(p,'--apply')
        self.assertEqual((p/'CLAUDE.md').read_text(),'@AGENTS.md\n')
        self.assertIn('new scope', (p/'AGENTS.md').read_text())
        self.assertTrue((p/'scripts/plan_intake.py').is_file())
        m=json.loads((p/'.harness/installation.json').read_text())
        for n,h in m['files'].items():self.assertEqual(hashlib.sha256((p/n).read_bytes()).hexdigest(),h)

    def test_existing_agent_instructions_refuse_every_write(self):
        p=self.repo();(p/'CLAUDE.md').write_text('User rules\n')
        self.install(p,'--apply',ok=False)
        self.assertEqual((p/'CLAUDE.md').read_text(),'User rules\n')
        self.assertFalse((p/'scripts').exists())

    def test_skill_install_both_agents_and_standalone_scripts(self):
        for agent in ('codex','claude'):
            parent=self.root/agent
            self.script('install_skill.py','--agent',agent,'--skills-dir',str(parent))
            self.assertFalse(parent.exists())
            self.script('install_skill.py','--agent',agent,'--skills-dir',str(parent),'--apply')
            self.script('install_skill.py','--agent',agent,'--skills-dir',str(parent),'--apply')
            skill=parent/'plan-dev-harness'
            self.assertIn('name: plan-dev-harness',(skill/'SKILL.md').read_text())
            self.cmd(sys.executable,str(skill/'scripts/install_harness.py'),'--help')
            self.assertTrue((skill/'assets/scripts/plan_intake.py').exists())

    def test_skill_collision_and_symlink_refused(self):
        p=self.root/'skills';dest=p/'plan-dev-harness';dest.mkdir(parents=True)
        (dest/'SKILL.md').write_text('Existing skill')
        self.script('install_skill.py','--agent','claude','--skills-dir',str(p),'--apply',ok=False)
        self.assertEqual((dest/'SKILL.md').read_text(),'Existing skill')
        link=self.root/'linked';link.symlink_to(p,target_is_directory=True)
        self.script('install_skill.py','--agent','codex','--skills-dir',str(link),'--apply',ok=False)

    def test_upgrade_preview_and_unchanged_files_only(self):
        p=self.repo();self.install(p,'--apply')
        package=self.root/'next';shutil.copytree(BASE,package,ignore=shutil.ignore_patterns('.git','__pycache__'))
        (package/'VERSION').write_text('0.1.1\n')
        target=package/'assets/scripts/plan_intake.py';target.write_text(target.read_text()+'\n# fixture next version\n')
        call=[sys.executable,str(package/'scripts/install_harness.py'),'--repo',str(p),'--protect','specs','--agent','both','--upgrade']
        before=(p/'scripts/plan_intake.py').read_bytes()
        self.cmd(*call);self.assertEqual((p/'scripts/plan_intake.py').read_bytes(),before)
        self.cmd(*call,'--apply');self.assertIn('fixture next version',(p/'scripts/plan_intake.py').read_text())
        self.assertEqual(json.loads((p/'.harness/installation.json').read_text())['version'],'0.1.1')
        (p/'scripts/plan_intake.py').write_text('User customization\n')
        self.cmd(*call,'--apply',ok=False)
        self.assertEqual((p/'scripts/plan_intake.py').read_text(),'User customization\n')

    def test_bootstrap_preview_then_real_shared_worktrees(self):
        args=['--parent',str(self.root),'--name','demo','--plan-branch','design',
              '--dev-branch','develop','--release-branch','release',
              '--author-name','Harness Test','--author-email','fixture@example.invalid']
        self.script('bootstrap_workspace.py',*args)
        self.assertFalse((self.root/'demo').exists())
        self.script('bootstrap_workspace.py',*args,'--apply')
        root=self.root/'demo';self.assertFalse((root/'.git').exists())
        commons=[]
        for role in ('main','plan','dev'):
            work=root/('demo_'+role)
            commons.append(self.cmd('git','rev-parse','--path-format=absolute','--git-common-dir',cwd=work).stdout)
            self.assertEqual(self.cmd('git','status','--porcelain',cwd=work).stdout,'')
            self.assertEqual((work/'CLAUDE.md').read_text(),'@AGENTS.md\n')
        self.assertEqual(len(set(commons)),1)
        dev=root/'demo_dev'
        for target in ('worktree','index','HEAD'):
            self.cmd(sys.executable,'scripts/contract_guard.py','check','--target',target,cwd=dev)
        q=json.loads(self.cmd(sys.executable,'scripts/work_queue.py','--json','--owner','all',cwd=dev).stdout)
        self.assertEqual(q['tasks'],[])
        self.script('bootstrap_workspace.py',*args,'--apply',ok=False)

    def test_bootstrap_refuses_invalid_and_nested_destinations(self):
        self.script('bootstrap_workspace.py','--parent',str(self.root),'--name','../escape',ok=False)
        p=self.repo()
        self.script('bootstrap_workspace.py','--parent',str(p),'--name','nested',ok=False)
        self.assertFalse((p/'nested').exists())

    def test_z_timestamp_compatibility(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('cards_test',BASE/'assets/scripts/plan_cards.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        text=(BASE/'assets/docs/planning/plans/_TEMPLATE.md').read_text().replace('<!-- EXECUTION:END -->','- 2026-10-29T10:00Z | STATE | NOTE | - | Started.\n<!-- EXECUTION:END -->')
        self.assertTrue(mod.parse(text))


if __name__=='__main__':unittest.main()
