"""Headless launcher checks: no display or external services required."""
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from arketype_launcher_ops import HELP, OperationError, inventory_report, parse_operation, run_operation

ROOT = Path(__file__).resolve().parents[1]


class LauncherOperationTests(unittest.TestCase):
    def test_allowed_operations(self):
        cases = {
            'help': ('local', ()),
            'status': ('local', ()),
            'list': ('cli', ('list',)),
            'search "causal diagnosis"': ('cli', ('search', 'causal diagnosis')),
            'show diagnostic-causal': ('cli', ('show', 'diagnostic-causal')),
            'profile suivi-employe': ('cli', ('profile', 'suivi-employe')),
            'recipe troubleshooting-systeme': ('cli', ('recipe', 'troubleshooting-systeme')),
            'validate --check-kit': ('cli', ('validate', '--check-kit')),
            'test': ('tests', ()),
            'inventory': ('local', ()),
            'build-html': ('cli', ('build-html',)),
            'open-catalogue': ('open', ()),
            'clear': ('clear', ()),
        }
        for cmd, (kind, argv) in cases.items():
            with self.subTest(cmd=cmd):
                op = parse_operation(cmd)
                self.assertEqual((op.kind, op.argv), (kind, argv))

    def test_reject_unsafe_or_unrecognized_commands(self):
        rejected = ['', '    ', 'rm -rf /', 'python -c "print(1)"',
                    'validate --unknown', 'validate --check-kit --something',
                    'build-html --output /tmp/out.html', 'show',
                    'show example extra', 'search --type files',
                    'create --type diagnostic-causal --slug test',
                    'publish', 'activate', 'curl https://example.com',
                    'list;rm -rf /', 'show "unterminated']
        for value in rejected:
            with self.subTest(value=value), self.assertRaises(OperationError):
                parse_operation(value)

    def test_validation_is_read_only_and_regeneration_marked(self):
        self.assertFalse(parse_operation('validate --check-kit').changes_files)
        self.assertTrue(parse_operation('build-html').changes_files)
        code, output = run_operation(parse_operation('status'))
        self.assertEqual(code, 0)
        self.assertIn('Archetypes: 19', output)
        self.assertIn('no publication', output.lower())

    def test_local_commands_and_inventory(self):
        code, output = run_operation(parse_operation('list'), timeout=40)
        self.assertEqual(code, 0)
        self.assertIn('ARK-19', output)
        code, output = run_operation(parse_operation('help'))
        self.assertEqual(code, 0)
        self.assertIn('No shell commands', output)

    def test_inventory_detects_edits(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'a.txt').write_text('abc', encoding='utf-8')
            import hashlib, json
            data = b'abc'
            (root/'INVENTAIRE.json').write_text(json.dumps({'files': [{
                'path': 'a.txt', 'sha256': hashlib.sha256(data).hexdigest(), 'size_bytes': len(data)}]}))
            self.assertIn('0 discrepancies', inventory_report(root))
            (root/'a.txt').write_text('modified', encoding='utf-8')
            self.assertIn('1 discrepancies', inventory_report(root))


class LauncherSourceTests(unittest.TestCase):
    def test_unified_navigation_and_logo(self):
        ui = (ROOT/'arketype_gui.py').read_text(encoding='utf-8')
        for label in ('Home', 'Catalogue', 'Create Kristal', 'Developer Ops', 'logo-k-ui.png',
                      '#1e6864', 'Open full visual catalogue', 'Preview (no files written)'):
            self.assertIn(label, ui)
        bootstrap = (ROOT/'Lancer_Arketype.pyw').read_text(encoding='utf-8')
        self.assertIn('from arketype_gui import main', bootstrap)

    def test_launcher_uses_explicit_threaded_jobs(self):
        ui = (ROOT/'arketype_gui.py').read_text(encoding='utf-8')
        self.assertIn('threading.Thread', ui)
        self.assertIn('self.events.put', ui)
        self.assertNotIn('shell=True', ui)


if __name__ == '__main__':
    unittest.main()
