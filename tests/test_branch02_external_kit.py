"""Opt-in Kit draft.4: actual two-source preflight, no default migration."""
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import arketype
from arketype_external_kit import preflight_external_v11_kit

KIT=Path(os.environ.get('ARKETYPE_TEST_KIT_SOURCE','/missing-kit'))
FRAMEWORK=Path(os.environ.get('ARKETYPE_TEST_FRAMEWORK_SOURCE','/missing-framework'))

class ExternalKitDraft4Tests(unittest.TestCase):
    def test_external_kit_requires_both_pinned_sources(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError,'Both external Kit and Framework'):
                arketype.create('referentiel-semantique','demo','Demo',td,authoring='v11',external_kit=td)
            with self.assertRaisesRegex(ValueError,'only supported for opt-in v11'):
                arketype.create('referentiel-semantique','demo','Demo',td,external_kit=td,framework=td)

    def test_no_implicit_upgrade_of_bundled_kit(self):
        with tempfile.TemporaryDirectory() as td:
            preview=arketype.create('referentiel-semantique','demo','Demo',td,authoring='v11',dry_run=True)
            self.assertEqual(preview['selected_kit_version'],'4.0.0-draft.3')
            self.assertFalse(Path(preview['destination']).exists())

    @unittest.skipUnless(KIT.is_dir() and FRAMEWORK.is_dir(),'Explicit Kit and Framework fixture sources are required')
    def test_real_draft4_creates_empty_noncanonical_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            a=preflight_external_v11_kit(KIT,FRAMEWORK)
            self.assertTrue(a['framework_pin_checked'])
            preview=arketype.create('referentiel-semantique','demo-v11','Demo',td,authoring='v11',
                                    external_kit=KIT,framework=FRAMEWORK,dry_run=True)
            self.assertFalse(Path(preview['destination']).exists())
            path=arketype.create('referentiel-semantique','demo-v11','Demo',td,authoring='v11',
                                 external_kit=KIT,framework=FRAMEWORK)
            info=json.loads((path/'arketype.instance.json').read_text())
            self.assertEqual(info['authoring_kit_reference'],'4.0.0-draft.4')
            self.assertTrue(info['externally_verified_framework_pin'])
            self.assertFalse(info['authorized_for_publication'])
            self.assertEqual(json.loads((path/'canon/state.index.json').read_text())['canonical_artifacts'],[])
            self.assertFalse((path/'.kristal/v11/authoring.json').exists())
            self.assertEqual(json.loads((path/'design/v11-semantic-readiness.json').read_text())['authoring_kit_baseline'],'4.0.0-draft.4')

    @unittest.skipUnless(KIT.is_dir() and FRAMEWORK.is_dir(),'Explicit Kit and Framework fixture sources are required')
    def test_tampered_framework_source_denied_without_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            copy=Path(td)/'fw'
            shutil.copytree(FRAMEWORK,copy)
            pinned=copy/'schemas/v11/kristal-dictionary-catalog.schema.json'
            pinned.write_bytes(pinned.read_bytes()+b' ')
            with self.assertRaisesRegex(ValueError,'source drift'):
                arketype.create('referentiel-semantique','demo','Demo',td,authoring='v11',external_kit=KIT,framework=copy)
            self.assertFalse((Path(td)/'demo').exists())

if __name__=='__main__':unittest.main()
