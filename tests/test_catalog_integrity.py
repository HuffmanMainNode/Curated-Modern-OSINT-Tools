import tempfile
import unittest
from pathlib import Path
from scripts.catalog_integrity import audit_submodules

class CatalogIntegrityTests(unittest.TestCase):
    def write_modules(self, root, content):
        (root / ".gitmodules").write_text(content, encoding="utf-8")

    def test_valid_metadata_matches_gitlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write_modules(root, '[submodule "sherlock"]\n path = tools/popular/sherlock\n url = https://github.com/sherlock-project/sherlock.git\n')
            report=audit_submodules(root, {"tools/popular/sherlock"})
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["submodule_count"], 1)

    def test_detects_missing_and_unconfigured_gitlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write_modules(root, '[submodule "one"]\n path = tools/a\n url = https://github.com/owner/repo\n')
            report=audit_submodules(root, {"tools/b"})
            self.assertTrue(any("no tracked gitlink" in error for error in report["errors"]))
            self.assertTrue(any("no .gitmodules entry" in error for error in report["errors"]))

    def test_rejects_spoofed_and_non_https_urls(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write_modules(root, '[submodule "one"]\n path = tools/a\n url = https://github.com.evil.example/owner/repo\n[submodule "two"]\n path = tools/b\n url = git://github.com/owner/repo\n')
            report=audit_submodules(root, {"tools/a","tools/b"})
            self.assertEqual(len(report["errors"]), 2)

    def test_reports_duplicate_upstreams_without_deleting_them(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write_modules(root, '[submodule "one"]\n path = tools/popular/project\n url = https://github.com/Owner/Repo\n[submodule "two"]\n path = tools/niche/project\n url = https://github.com/owner/repo.git\n')
            report=audit_submodules(root, {"tools/popular/project","tools/niche/project"})
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["duplicate_url_group_count"], 1)
            self.assertEqual(report["submodule_count"], 2)

    def test_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.write_modules(root, '[submodule "one"]\n path = ../outside\n url = https://github.com/owner/repo\n')
            report=audit_submodules(root, {"../outside"})
            self.assertTrue(any("unsafe" in error for error in report["errors"]))

    def test_missing_gitmodules_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            report=audit_submodules(directory, set())
            self.assertIn("missing .gitmodules", report["errors"])

if __name__ == "__main__":
    unittest.main()
