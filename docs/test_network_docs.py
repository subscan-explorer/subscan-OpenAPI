"""Check inventory semantics and the generated public documentation artifacts."""

import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest

from network_docs import DOC_DIR, load_endpoints


TABLE_TOOLS = runpy.run_path(str(DOC_DIR / "gen-api-endpoint.py"))
ENV_TOOLS = runpy.run_path(str(DOC_DIR / "doc-env-tools.py"))


class NetworkDocsTests(unittest.TestCase):
    def load_fixture(self, networks):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "network.json"
            path.write_text(json.dumps(networks), encoding="utf-8")
            return load_endpoints(path)

    def test_archive_status_takes_precedence_over_network_type(self):
        endpoints = self.load_fixture({
            "old-mainnet": {"type": "mainnet", "is_archive": True, "api_domains": ["old-mainnet"]},
            "old-testnet": {"type": "testnet", "is_archive": True, "api_domains": ["old-testnet"]},
            "mainnet": {"type": "mainnet", "api_domains": ["mainnet"]},
            "testnet": {"type": "testnet", "api_domains": ["testnet"]},
        })
        self.assertEqual({endpoint["domain"]: endpoint["status"] for endpoint in endpoints}, {
            "old-mainnet": "archive", "old-testnet": "archive", "mainnet": "live", "testnet": "test",
        })

    def test_api_domains_preserve_generation_and_skip_legacy_aliases(self):
        endpoints = self.load_fixture({
            "creditcoin-cc3": {
                "type": "mainnet", "api_domains": ["creditcoin3", "creditcoin-classic"],
                "ui_domains": ["creditcoin"],
            },
            "statemine": {"type": "mainnet", "api_domains": ["assethub-kusama"]},
        })
        self.assertEqual(endpoints, [
            {"name": "Assethub-kusama", "domain": "assethub-kusama", "status": "live"},
            {"name": "Creditcoin-cc3", "domain": "creditcoin3", "status": "live"},
        ])

    def test_invalid_type_and_duplicate_public_domains_fail(self):
        with self.assertRaisesRegex(ValueError, "unsupported network type"):
            self.load_fixture({"unknown": {"type": "unknown", "api_domains": ["unknown"]}})
        with self.assertRaisesRegex(ValueError, "duplicate public API domain"):
            self.load_fixture({
                "one": {"type": "mainnet", "api_domains": ["same"]},
                "two": {"type": "testnet", "api_domains": ["same"]},
            })

    def test_committed_table_and_environments_match_inventory(self):
        endpoints = load_endpoints()
        content = (DOC_DIR / "Introduction.md").read_text(encoding="utf-8")
        table = content.split(TABLE_TOOLS["BEGIN_MARKER"])[1].split(TABLE_TOOLS["END_MARKER"])[0]
        self.assertEqual(table, "\n\n" + TABLE_TOOLS["generate_table"](endpoints) + "\n")
        expected_environments = ENV_TOOLS["generate_json"]([endpoint["domain"] for endpoint in endpoints])
        self.assertEqual(json.loads((DOC_DIR / "environments.json").read_text()), expected_environments)

    def test_apidog_introduction_matches_markdown(self):
        data = json.loads((DOC_DIR / "subscan.apidog.json").read_text(encoding="utf-8"))
        introduction = next(item for item in data["docCollection"][0]["items"]
                            if item["name"] == "Introduction")
        self.assertEqual(introduction["content"], (DOC_DIR / "Introduction.md").read_text(encoding="utf-8"))

    def test_table_update_rejects_missing_or_ambiguous_markers_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Introduction.md"
            for content in ["no markers", TABLE_TOOLS["BEGIN_MARKER"] * 2 + TABLE_TOOLS["END_MARKER"]]:
                path.write_text(content, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "exactly one"):
                    TABLE_TOOLS["update_table"](path, "replacement")
                self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_generators_work_outside_document_directory_and_are_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            for filename in ["network_docs.py", "network.json", "gen-api-endpoint.py",
                             "doc-env-tools.py", "Introduction.md"]:
                shutil.copyfile(DOC_DIR / filename, docs / filename)
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            for _ in range(2):
                for script, args in [("gen-api-endpoint.py", ["--write"]), ("doc-env-tools.py", [])]:
                    subprocess.run([sys.executable, str(docs / script), *args],
                                   cwd=root, env=env, check=True, capture_output=True, text=True)
                for filename in ["Introduction.md", "environments.json"]:
                    self.assertEqual((docs / filename).read_bytes(), (DOC_DIR / filename).read_bytes())
            preview = subprocess.run([sys.executable, str(docs / "gen-api-endpoint.py")],
                                     cwd=root, env=env, check=True, capture_output=True, text=True)
            self.assertEqual(preview.stdout, TABLE_TOOLS["generate_table"](load_endpoints()))


if __name__ == "__main__":
    unittest.main()
