"""v11 opt-in integration: design-only, no ghost KQ or unapproved migration."""
from __future__ import annotations
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import arketype
from arketype_semantic import semantic_status,run_dik_coverage
from arketype_ecosystem import inspect_dik,inspect_framework

ROOT=Path(__file__).resolve().parents[1]
DIK=Path(os.environ.get('ARKETYPE_TEST_DIK_SOURCE', '/no-external-dik-configured'))
FRAMEWORK=Path(os.environ.get('ARKETYPE_TEST_FRAMEWORK_SOURCE', '/no-external-framework-configured'))

class SemanticOptInTests(unittest.TestCase):
    def test_v11_dry_run_no_files_and_no_fake_identifiers(self):
        with tempfile.TemporaryDirectory() as d:
            preview=arketype.create('referentiel-semantique','start-v11','Start v11',d,authoring='v11',dry_run=True)
            self.assertEqual(preview['authoring_mode'],'v11')
            self.assertFalse(preview['strict_v11_enabled'])
            self.assertFalse(Path(preview['destination']).exists())
    def test_v11_workspace_creation_is_empty_and_has_kit4(self):
        with tempfile.TemporaryDirectory() as d:
            path=arketype.create('referentiel-semantique','start-v11','Start v11',d,authoring='v11')
            data=arketype.read_json(path/'arketype.instance.json')
            self.assertEqual(data['authoring_kit_reference'],'4.0.0-draft.3')
            self.assertEqual(data['v11_readiness'],'identity_registry_and_graph_not_created')
            self.assertEqual(arketype.read_json(path/'canon/state.index.json')['canonical_artifacts'],[])
            note=arketype.read_json(path/'design/v11-semantic-readiness.json')
            self.assertFalse(note['strict_v11_enabled'])
            self.assertTrue(note['no_provisional_wikidata_qids'])
            self.assertFalse((path/'.kristal/v11/authoring.json').exists())
            self.assertFalse((path/'canon/domain/v11-graph.json').exists())
            self.assertEqual(semantic_status(path)['bundled_workspace_kit_version'],'4.0.0-draft.3')
    def test_legacy_mode_is_still_default(self):
        with tempfile.TemporaryDirectory() as d:
            path=arketype.create('referentiel-semantique','start-old','Start old',d)
            self.assertEqual(semantic_status(path)['bundled_workspace_kit_version'],'3.2.4')
            self.assertFalse((path/'design/v11-semantic-readiness.json').exists())
    def test_reject_made_up_authoring_mode(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):arketype.create('referentiel-semantique','x','X',d,authoring='automatic-Q')
    def test_semantic_status_does_not_claim_proof_from_profile(self):
        with tempfile.TemporaryDirectory() as d:
            path=arketype.create('referentiel-semantique','status-v11','Status v11',d,authoring='v11')
            profile=path/'.kristal/v11/authoring.json';profile.parent.mkdir(parents=True)
            profile.write_text(json.dumps({'semantic_profile':'kristal.semantic-identity/11.0','graph':'canon/domain/nope.json'}))
            report=semantic_status(path)
            self.assertTrue(report['flags']['v11_authoring_profile_present'])
            self.assertFalse(report['flags']['v11_strict_validation_performed'])
            self.assertEqual(report['semantic_completeness'],'unknown_not_evaluated')
    def test_dik_is_never_implicit(self):
        self.assertEqual(inspect_dik()['status'],'not_configured')
        with self.assertRaises(ValueError):run_dik_coverage(ROOT,ROOT/'catalogue.json')
    @unittest.skipUnless(DIK.is_dir(), 'Integration source is available only in build environment')
    def test_dik_source_coverage_is_real_and_read_only(self):
        project=DIK/'examples/demo/dik.project.json'
        before=project.read_bytes()
        r=json.loads(run_dik_coverage(DIK,project,'fr,en,fr-CA'))
        self.assertEqual(r['artifact_type'],'kristal_dik_coverage_report')
        self.assertEqual(r['semantic_reference_count'],{'KQ':2,'KP':1})
        self.assertEqual(before,project.read_bytes())
        self.assertEqual(inspect_dik(DIK)['status'],'local_source_present')
    @unittest.skipUnless(FRAMEWORK.is_dir(), 'Framework source only available in build environment')
    def test_framework_11_metadata_inspection_not_certification(self):
        r=inspect_framework(ROOT,FRAMEWORK)
        self.assertEqual(r['status'],'declared_version_matches')
        self.assertIn('NOT run',r['details'])

if __name__=='__main__':unittest.main()
