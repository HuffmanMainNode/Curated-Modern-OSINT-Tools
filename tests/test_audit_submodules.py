import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.audit_submodules import audit


class SubmoduleAuditTests(unittest.TestCase):
    def make_repo(self, root, mappings, gitlinks):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        for name, path, url in mappings:
            subprocess.run(["git", "-C", str(root), "config", "-f", ".gitmodules", f"submodule.{name}.path", path], check=True)
            subprocess.run(["git", "-C", str(root), "config", "-f", ".gitmodules", f"submodule.{name}.url", url], check=True)
        for path, commit in gitlinks:
            subprocess.run(["git", "-C", str(root), "update-index", "--add", "--cacheinfo", f"160000,{commit},{path}"], check=True)
        if (root / ".gitmodules").exists():
            subprocess.run(["git", "-C", str(root), "add", ".gitmodules"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)

    def test_matching_gitlink_and_mapping_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sha = "a" * 40
            self.make_repo(root, [("one", "tools/one", "https://github.com/example/one")], [("tools/one", sha)])
            report = audit(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["matched_count"], 1)

    def test_missing_gitlink_mapping_is_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, [("one", "tools/one", "https://github.com/example/one")], [])
            report = audit(root)
            self.assertIn("mapping_missing_gitlink", [item["code"] for item in report["errors"]])

    def test_missing_mapping_for_gitlink_is_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, [], [("tools/one", "a" * 40)])
            report = audit(root)
            self.assertIn("gitlink_missing_mapping", [item["code"] for item in report["errors"]])

    def test_rejects_non_https_and_spoofed_hosts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mappings = [
                ("one", "tools/one", "http://github.com/example/one"),
                ("two", "tools/two", "https://github.com.evil.example/example/two"),
            ]
            gitlinks = [("tools/one", "a" * 40), ("tools/two", "b" * 40)]
            self.make_repo(root, mappings, gitlinks)
            report = audit(root)
            self.assertEqual(
                sum(item["code"] == "untrusted_or_malformed_url" for item in report["errors"]),
                2,
            )

    def test_duplicate_upstream_is_warning_not_silent_deduplication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            url = "https://github.com/example/shared"
            mappings = [("one", "tools/one", url), ("two", "tools/two", url)]
            gitlinks = [("tools/one", "a" * 40), ("tools/two", "b" * 40)]
            self.make_repo(root, mappings, gitlinks)
            report = audit(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(len(report["duplicate_upstream_url_groups"]), 1)


if __name__ == "__main__":
    unittest.main()
