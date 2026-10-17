"""Pinned vendor, user-approved logo, historic neutral templates and current metadata."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import arketype
from arketype_ecosystem import inspect_framework,inspect_modern_kit

ROOT=Path(__file__).resolve().parents[1]
USER_LOGO_SHA256='6b02eaf8ab47803f58e8fd56c942c9438639c7a303fdb6a5ba4c5a3f9e137b28'

class Upgrade160Tests(unittest.TestCase):
    def test_logo_exact_svg_from_user(self):
        original=ROOT/'assets/logo-k.svg'
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),USER_LOGO_SHA256)
        self.assertTrue(original.read_bytes().startswith(b'<?xml'))
        self.assertIn(b'viewBox="0 0 209 92"',original.read_bytes())
        self.assertTrue((ROOT/'assets/logo-k-ui.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    def test_vendor_pin_current_and_exact(self):
        meta=json.loads((ROOT/'outils/authoring_v11/VENDOR_PIN.json').read_text())
        self.assertEqual(meta['kit_version'],'4.0.0-draft.3')
        self.assertEqual(meta['framework_reference'],'11.0.0-draft.4')
        self.assertEqual(len(meta['copied_paths']),11)
        self.assertEqual(inspect_modern_kit()['status'],'vendored_source_verified')
        self.assertEqual(len({x['upstream'] for x in meta['copied_paths']}),11)
    def test_19_historic_models_have_no_canon_mutation_and_valid_receipts(self):
        refs=set()
        for model in (ROOT/'modeles').iterdir():
            if not model.is_dir():continue
            state=json.loads((model/'kristal.workspace.json').read_text())
            index=json.loads((model/'canon/state.index.json').read_text())
            receipt=json.loads((model/'build/v9/build-receipt.json').read_text())
            self.assertEqual(receipt['kit_version'],'3.2.4')
            self.assertEqual(receipt['state_ref'],state['state_ref'])
            self.assertEqual(receipt['generated_logical_artifacts'],0)
            self.assertEqual(index['canonical_artifacts'],[])
            refs.add(state['state_ref'])
        self.assertEqual(len(refs),19)
    def test_casefile_form_provenance(self):
        self.assertFalse((ROOT/'modeles/dossier-suivi/design/fiche-deposition-vierge.json').exists())
        self.assertTrue((ROOT/'modeles/dossier-suivi/design/fiche-suivi-vierge.json').exists())
        self.assertTrue((ROOT/'modeles/deposition-temoignage/design/fiche-deposition-vierge.json').exists())
    def test_catalogue_framework_and_dik_versions(self):
        cat=json.loads((ROOT/'catalogue.json').read_text())
        self.assertEqual((cat['version'],cat['framework_reference'],cat['authoring_kit_reference'],cat['dik_reference']),
                         ('1.6.0','11.0.0-draft.4','4.0.0-draft.3','1.0.0-alpha.7'))
    def test_new_v11_workspace_uses_new_vendor_and_no_semantic_invention(self):
        with tempfile.TemporaryDirectory() as td:
            p=arketype.create('taxonomie-classification','fresh160','Fresh 160',td,authoring='v11')
            origin=arketype.read_json(p/'arketype.instance.json')
            plan=arketype.read_json(p/'design/v11-semantic-readiness.json')
            self.assertEqual(origin['library_version'],'1.6.0')
            self.assertEqual(origin['authoring_kit_reference'],'4.0.0-draft.3')
            self.assertEqual(plan['framework_baseline'],'11.0.0-draft.4')
            self.assertFalse(origin['authorized_for_publication'])
            self.assertFalse(plan['strict_v11_enabled'])
            self.assertEqual(arketype.read_json(p/'canon/state.index.json')['canonical_artifacts'],[])
            tool=(p/'tools/kristal.py').read_text()
            for cmd in ['import-dik-catalog','select-v11-catalog','recover-v11']:
                self.assertIn(cmd,tool)
    def test_logo_referenced_in_generated_html_and_gui(self):
        self.assertIn('../assets/logo-k.svg',(ROOT/'catalogue/index.html').read_text())
        self.assertIn('logo-k-ui.png',(ROOT/'arketype_gui.py').read_text())

if __name__=='__main__': unittest.main()
