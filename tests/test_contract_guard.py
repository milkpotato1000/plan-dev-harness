"""Exercise real Git snapshots and hooks in disposable repositories."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest


SOURCE = pathlib.Path(__file__).resolve().parents[1] / "assets"


class ContractGuardTests(unittest.TestCase):
    def run_command(self, *args, ok=True, input=None):
        result = subprocess.run(args, cwd=self.root, text=True, input=input, capture_output=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def git(self, *args, **kwargs):
        return self.run_command("git", *args, **kwargs)

    def guard(self, *args, **kwargs):
        return self.run_command("python3", "scripts/contract_guard.py", *args, **kwargs)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="contract-guard-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.git("init", "-b", "plan")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Harness test")
        self.git("config", "commit.gpgsign", "false")
        # Do not inherit host hooks in disposable test repos.
        self.git("config", "core.hooksPath", ".githooks")
        for name in (".harness/policy.json", "scripts/contract_guard.py", "scripts/plan_cards.py", "scripts/work_queue.py", "scripts/plan_intake.py", "scripts/workflow_control.py"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / name, target)
        self.write(".gitignore", "__pycache__/\n*.pyc\n")
        self.write("config/metric.json", '{"grain": "tracking"}\n')
        shutil.copytree(SOURCE / ".githooks", self.root / ".githooks")
        self.git("add", ".")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-m", "Planning baseline")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "-b", "dev")
        self.guard("adopt", self.base, "--review-reference", "Fixture reviewed handoff")
        self.git("add", ".")
        self.git("commit", "-m", "Adopt baseline")

    def test_latest_plan_can_advance_without_blocking_dev(self):
        self.git("checkout", "plan")
        self.write("config/metric.json", '{"grain": "future"}\n')
        self.git("add", "config")
        self.git("commit", "-m", "Future unadopted proposal")
        self.git("checkout", "dev")
        self.guard("check", "--target", "HEAD")

    def test_staged_contract_edit_is_rejected_by_commit_hook(self):
        self.write("config/metric.json", '{"grain": "cargo"}\n')
        self.git("add", "config")
        result = self.git("commit", "-m", "Unauthorized definition", ok=False)
        self.assertIn("Protected files differ", result.stderr)

    def test_new_and_deleted_contracts_are_rejected(self):
        self.write("config/new.json", "{}\n")
        self.guard("check", ok=False)
        self.git("add", "config/new.json")
        self.guard("check", "--target", "index", ok=False)
        self.git("reset", "--hard", "HEAD")
        self.git("rm", "config/metric.json")
        self.guard("check", "--target", "index", ok=False)

    def test_dev_records_allowed_despite_unstaged_contract_draft(self):
        self.write("config/metric.json", "draft\n")
        self.write("docs/progress/run.md", "Validation complete\n")
        self.git("add", "docs/progress")
        self.git("commit", "-m", "Record development progress")
        self.guard("check", ok=False)

    def test_policy_edit_cannot_remove_protected_paths_in_index(self):
        policy = json.loads((self.root / ".harness/policy.json").read_text())
        policy["protected_paths"] = []
        self.write(".harness/policy.json", json.dumps(policy))
        self.git("add", ".harness/policy.json")
        self.guard("check", "--target", "index", ok=False)

    def test_adoption_of_dev_only_commit_is_rejected_without_losing_record(self):
        self.write("docs/progress/run.md", "Result\n")
        self.git("add", "docs/progress")
        self.git("commit", "-m", "Development result")
        before = (self.root / ".harness/adopted-plan.json").read_bytes()
        self.guard("adopt", "HEAD", "--review-reference", "Not a plan commit", ok=False)
        self.assertEqual(before, (self.root / ".harness/adopted-plan.json").read_bytes())

    def test_reviewed_merge_and_new_adoption_pass(self):
        self.git("checkout", "plan")
        self.write("config/metric.json", '{"grain": "reviewed change"}\n')
        self.git("add", "config")
        self.git("commit", "-m", "Reviewed contract update")
        newer = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "dev")
        self.git("merge", "--no-commit", "plan")
        self.guard("adopt", newer, "--review-reference", "Accepted review")
        self.git("add", ".harness/adopted-plan.json")
        self.git("commit", "-m", "Merge and adopt reviewed plan")
        self.guard("check", "--target", "HEAD")

    def test_push_checks_actual_commit_even_when_launched_from_plan(self):
        self.write("config/metric.json", "bad definition\n")
        self.git("add", "config")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-m", "Simulate hook bypass")
        bad = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "plan")
        result = self.run_command(".githooks/pre-push", "origin", "unused", ok=False,
                                  input=f"refs/heads/alias {bad} refs/heads/dev {'0' * 40}\n")
        self.assertIn("Protected files differ", result.stderr)

    def test_direct_main_commit_is_rejected(self):
        self.git("checkout", "-b", "main")
        self.write("app.py", "print('direct change')\n")
        self.git("add", "app.py")
        result = self.git("commit", "-m", "Direct main commit", ok=False)
        self.assertIn("No direct release-branch commits", result.stderr)

    def test_missing_baseline_fails_closed(self):
        self.git("rm", ".harness/adopted-plan.json")
        self.guard("check", "--target", "index", ok=False)

    def test_installer_preserves_existing_custom_hooks(self):
        self.git("config", "core.hooksPath", ".custom-hooks")
        self.guard("install", ok=False)
        self.assertEqual(self.git("config", "--get", "core.hooksPath").stdout.strip(), ".custom-hooks")


if __name__ == "__main__":
    unittest.main()
