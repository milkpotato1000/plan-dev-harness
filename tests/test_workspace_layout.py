"""Exercise real Git relocation, preservation, refusal and repeatability."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/nest_worktrees.py'


class WorkspaceLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nested-harness-')
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name).resolve()
        self.primary = self.parent / 'demo'
        self.plan = self.parent / 'demo-plan'
        self.dev = self.parent / 'demo-dev'
        self.git('init', '-b', 'release', str(self.primary), cwd=self.parent)
        self.git('config', 'user.name', 'Layout test')
        self.git('config', 'user.email', 'layout@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        (self.primary / '.harness').mkdir()
        (self.primary / '.harness/policy.json').write_text(json.dumps({
            'planning_branch': 'design', 'development_branch': 'develop', 'release_branch': 'release'}))
        (self.primary / 'AGENTS.md').write_text('Original project rules\n')
        (self.primary / '.gitignore').write_text('.venv/\n')
        self.git('add', '.')
        self.git('commit', '-m', 'Initial baseline')
        self.git('config', 'core.hooksPath', '.githooks')
        self.git('remote', 'add', 'personal', 'https://example.invalid/demo.git')
        self.git('worktree', 'add', '-b', 'design', str(self.plan))
        self.git('worktree', 'add', '-b', 'develop', str(self.dev))
        self.sha = self.git('rev-parse', 'HEAD')

    def git(self, *args, cwd=None):
        return subprocess.run(['git', '-C', str(cwd or self.primary), *args],
                              text=True, capture_output=True, check=True).stdout.strip()

    def run_layout(self, *args, repo=None, workspace=None, ok=True):
        result = subprocess.run(['python3', str(SCRIPT), '--repo', str(repo or self.primary),
                                 '--workspace-root', str(workspace or self.primary), *args],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_preview_does_not_move_or_write(self):
        self.run_layout()
        self.assertTrue((self.primary / '.git').is_dir())
        self.assertTrue(self.plan.exists())
        self.assertTrue(self.dev.exists())
        self.assertEqual((self.primary / 'AGENTS.md').read_text(), 'Original project rules\n')

    def test_migration_preserves_repository_and_ignored_runtime_and_is_repeatable(self):
        (self.dev / '.venv').mkdir()
        (self.dev / '.venv/keep.bin').write_bytes(b'ignored runtime')
        self.run_layout('--apply')
        common = None
        for role, branch in [('main', 'release'), ('plan', 'design'), ('dev', 'develop')]:
            root = self.primary / ('demo_' + role)
            self.assertEqual(self.git('branch', '--show-current', cwd=root), branch)
            self.assertEqual(self.git('rev-parse', 'HEAD', cwd=root), self.sha)
            self.assertEqual(self.git('status', '--porcelain', cwd=root), '')
            self.assertEqual(self.git('config', '--get', 'core.hooksPath', cwd=root), '.githooks')
            self.assertEqual(self.git('remote', 'get-url', 'personal', cwd=root), 'https://example.invalid/demo.git')
            actual = (root / self.git('rev-parse', '--git-common-dir', cwd=root)).resolve()
            common = common or actual
            self.assertEqual(actual, common)
        self.assertFalse((self.primary / '.git').exists())
        self.assertFalse(self.plan.exists())
        self.assertFalse(self.dev.exists())
        self.assertEqual((self.primary / 'demo_dev/.venv/keep.bin').read_bytes(), b'ignored runtime')
        self.assertEqual((self.primary / 'demo_main/AGENTS.md').read_text(), 'Original project rules\n')
        self.run_layout('--apply', repo=self.primary / 'demo_main')

    def test_dirty_worktree_refused_before_any_movement(self):
        (self.dev / 'AGENTS.md').write_text('Uncommitted dev work\n')
        self.run_layout('--apply', ok=False)
        self.assertTrue((self.primary / '.git').is_dir())
        self.assertEqual((self.dev / 'AGENTS.md').read_text(), 'Uncommitted dev work\n')

    def test_occupied_destination_refused(self):
        (self.primary / 'demo_plan').mkdir()
        self.run_layout('--apply', ok=False)
        self.assertTrue((self.primary / '.git').is_dir())
        self.assertTrue(self.plan.exists())

    def test_locked_worktree_refused(self):
        self.git('worktree', 'lock', str(self.dev))
        self.run_layout('--apply', ok=False)
        self.assertTrue((self.primary / '.git').is_dir())

    def test_existing_container_instructions_are_preserved(self):
        self.run_layout('--apply')
        instructions = self.primary / 'AGENTS.md'
        instructions.write_text('Custom routing rules\n')
        self.run_layout('--apply', repo=self.primary / 'demo_main', ok=False)
        self.assertEqual(instructions.read_text(), 'Custom routing rules\n')

    def test_new_container_with_spaces_and_shell_metacharacters(self):
        workspace = self.parent / 'team demo; safe'
        self.run_layout('--apply', workspace=workspace)
        root = workspace / 'team demo; safe_dev'
        self.assertEqual(self.git('rev-parse', 'HEAD', cwd=root), self.sha)
        self.assertIn("cd 'team demo; safe_plan'", (workspace / 'AGENTS.md').read_text())

    def test_symlink_container_refused(self):
        alias = self.parent / 'alias'
        alias.symlink_to(self.primary, target_is_directory=True)
        self.run_layout('--apply', workspace=alias, ok=False)
        self.assertTrue((self.primary / '.git').is_dir())


if __name__ == '__main__':
    unittest.main()
