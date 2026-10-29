import json
from pathlib import Path
import subprocess
import tempfile
import unittest

INSTALLER = Path(__file__).resolve().parents[1] / 'scripts/install_harness.py'


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='harness-install-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-b', 'design', str(self.root)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(self.root), 'config', 'core.hooksPath', '.githooks'], check=True)

    def install(self, *extra, ok=True):
        result = subprocess.run(['python3', str(INSTALLER), '--repo', str(self.root),
                                 '--plan-branch', 'design', '--dev-branch', 'develop',
                                 '--release-branch', 'release', '--protect', 'specs', *extra],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_preview_writes_nothing(self):
        self.install()
        self.assertEqual([p.name for p in self.root.iterdir()], ['.git'])

    def test_apply_is_idempotent_and_configurable(self):
        self.install('--apply')
        before = (self.root / '.harness/policy.json').read_bytes()
        self.install('--apply')
        self.assertEqual(before, (self.root / '.harness/policy.json').read_bytes())
        config = json.loads(before)
        self.assertEqual(config['development_branch'], 'develop')
        self.assertIn('specs', config['protected_paths'])
        self.assertTrue((self.root / '.githooks/pre-commit').stat().st_mode & 0o111)

    def test_differing_existing_file_aborts_all_writes(self):
        (self.root / 'scripts').mkdir()
        existing = self.root / 'scripts/contract_guard.py'
        existing.write_text('existing project script\n')
        self.install('--apply', ok=False)
        self.assertEqual(existing.read_text(), 'existing project script\n')
        self.assertFalse((self.root / '.harness').exists())

    def test_symlink_destination_is_refused(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / 'scripts').symlink_to(outside, target_is_directory=True)
            self.install('--apply', ok=False)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_existing_hook_system_preserved(self):
        subprocess.run(['git', '-C', str(self.root), 'config', 'core.hooksPath', '.existing'], check=True)
        self.install('--apply', ok=False)
        self.assertFalse((self.root / '.harness').exists())

    def test_adoption_record_cannot_be_in_protected_scope(self):
        self.install('--protect', '.harness', '--apply', ok=False)
        self.assertFalse((self.root / '.harness').exists())


if __name__ == '__main__':
    unittest.main()
