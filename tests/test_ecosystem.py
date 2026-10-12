"""Read-only ecosystem checks; no network, external programs or canonical changes."""
from pathlib import Path
import hashlib
import json
import tempfile
import unittest

from arketype_ecosystem import (ROOT, inspect_bootstrap, inspect_ecosystem,
                                inspect_framework, inspect_kit, inspect_manager,
                                inspect_templates, inspect_workspace, format_ecosystem_report)
from arketype_launcher_ops import OperationError, parse_operation, run_operation


class EcosystemInspectionTests(unittest.TestCase):
    def test_bundled_version_and_19_neutral_template_identities(self):
        report = inspect_ecosystem()
        self.assertEqual(report['authoring_kit']['bundled_version'], '3.2.4')
        self.assertEqual(report['templates']['status'], 'templates_consistent')
        self.assertEqual(report['templates']['unique_state_refs'], 19)
        self.assertEqual(report['templates']['count'], 19)
        self.assertEqual(report['framework']['status'], 'not_configured')
        self.assertFalse(report['is_qualification'])
        self.assertTrue(report['does_not_publish'])

    def test_external_kit_exact_hash_and_drift(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'tools' / 'kristal.py'
            path.parent.mkdir()
            path.write_bytes((ROOT / 'outils' / 'kristal.py').read_bytes())
            self.assertEqual(inspect_kit(selected=Path(td))['status'], 'identical_bytes')
            path.write_text(path.read_text(encoding='utf-8') + '\n# locally modified\n', encoding='utf-8')
            self.assertEqual(inspect_kit(selected=Path(td))['status'], 'review_required')

    def test_framework_version_matches_without_claiming_conformance(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td) / 'contracts'
            folder.mkdir()
            for filename, obj in [('release.json', {'version': '10.0.0-draft.3.1', 'status': 'draft'}),
                                  ('contract-set.json', {'version': '10.0.0-draft.3.1'}),
                                  ('v10-compatibility-lock.json', {'release': '10.0.0-draft.1'})]:
                (folder / filename).write_text(json.dumps(obj), encoding='utf-8')
            result = inspect_framework(ROOT, td)
            self.assertEqual(result['status'], 'declared_version_matches')
            self.assertEqual(result['release_status'], 'draft')
            self.assertIn('NOT run', result['details'])
            (folder / 'release.json').write_text('{"version":"9.0.0"}', encoding='utf-8')
            self.assertEqual(inspect_framework(ROOT, td)['status'], 'review_required')
            (folder / 'contract-set.json').unlink()
            self.assertEqual(inspect_framework(ROOT, td)['status'], 'not_available')

    def test_workspace_is_metadata_only_and_no_files_changed(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / 'kristal.workspace.json').write_text(json.dumps({
                'format': 'kristal.local-workspace/3.2.0',
                'state_ref': 'urn:kristal:state:case',
                'target': {'hosted_network_baseline': 'kristal.hosting/10.0'},
                'portable_ai': {'enabled': False}}), encoding='utf-8')
            (p / 'canon').mkdir()
            (p / 'canon' / 'state.index.json').write_text(json.dumps({'canonical_artifacts': [
                {'path': 'secret.json'}]}), encoding='utf-8')
            (p / 'canon' / 'secret.json').write_text('DO_NOT_EXPOSE', encoding='utf-8')
            before = {f.relative_to(p): hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
            report = inspect_workspace(p)
            self.assertEqual(report['registered_artifact_count'], 1)
            self.assertEqual(report['state_ref'], 'urn:kristal:state:case')
            self.assertNotIn('DO_NOT_EXPOSE', str(report))
            after = {f.relative_to(p): hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
            self.assertEqual(before, after)

    def test_no_implicit_manager_or_bootstrap_capability(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(inspect_manager(td)['status'], 'source_incomplete')
            self.assertEqual(inspect_bootstrap(td)['status'], 'source_incomplete')
            self.assertEqual(inspect_manager()['status'], 'not_configured')
            self.assertEqual(inspect_bootstrap()['status'], 'not_configured')

    def test_missing_template_is_not_silently_ok(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'catalogue.json').write_text(json.dumps({'archetypes': [{'slug': 'nope'}]}))
            self.assertEqual(inspect_templates(root)['status'], 'error')

    def test_allowlist_for_local_inspection(self):
        self.assertEqual(parse_operation('compat').kind, 'local')
        self.assertEqual(parse_operation('compat --framework "C:/Program Files/Framework"').argv,
                         ('--framework', 'C:/Program Files/Framework'))
        for unsafe in ['compat --unknown /tmp', 'compat --framework',
                       'compat --framework /tmp --framework /var',
                       'compat; rm -rf /', 'compat --kit', 'compat --framework /tmp --invalid /home',
                       'compat --workspace "unterminated']:
            with self.subTest(unsafe=unsafe), self.assertRaises(OperationError):
                parse_operation(unsafe)

    def test_console_status_and_no_publication(self):
        code, output = run_operation(parse_operation('compat'))
        self.assertEqual(code, 0)
        self.assertIn('NOT a qualification', output)
        self.assertIn('No network, publication, sync, or activation', output)
        self.assertIn('TEMPLATES [templates_consistent]', output)
        self.assertIn('No remote GitHub checks', str(inspect_ecosystem()['limits']))


if __name__ == '__main__':
    unittest.main()
