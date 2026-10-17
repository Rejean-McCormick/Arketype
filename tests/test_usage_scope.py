"""Use-case, recognition and scope guidance regressions; synthetic local metadata only."""
from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arketype
from use_cases import inspect_local, recognize, scope_guidance

class UsageProfilesTests(unittest.TestCase):
    def test_all_profiles_have_coverage_not_evaluated(self):
        ps=arketype.use_case_profiles()
        self.assertEqual(len(ps), 21)
        self.assertEqual(len({p['slug'] for p in ps}),len(ps))
        for p in ps:
            self.assertTrue(p['coverage_checks'])
            self.assertTrue(all(c['status']=='not_evaluated' for c in p['coverage_checks']))
            self.assertEqual(p['profile_status'],'design_guidance_only')
            self.assertEqual(arketype.assembly(p['assemblage_reference'])['primary_archetype'],p['primary_archetype'])
    def test_all_specialized_profiles_present(self):
        for slug in ('campus-federe','publication-moodle','collection-traditions','organisations-sociales','navigation-preuves-longues','recherche-mathematique','dossier-scolaire','dossier-medical','dossier-civique','diagnostic-vehicule','operations-police','operations-hopital','orchestration-medicale','cartographie-scolaire','referentiel-polyusage','temoignages-enquete'):
            self.assertEqual(arketype.use_case_profile(slug)['slug'],slug)
    def test_scope_guide_is_not_injection(self):
        guide=scope_guidance(arketype.use_case_profile('navigation-preuves-longues'))
        self.assertEqual(guide['status'],'draft_requires_review')
        self.assertFalse(guide['publication_authorized'])
        self.assertFalse(guide['activation_authorized'])
        self.assertTrue(all(c['status']=='not_evaluated' for c in guide['coverage_questions']))
        self.assertNotIn('proposed_state_scope', guide)
    def test_different_domains_share_structure(self):
        vals=[arketype.use_case_profile(s) for s in ('dossier-scolaire','dossier-medical','dossier-civique')]
        self.assertEqual({v['primary_archetype'] for v in vals},{'dossier-suivi'})
        self.assertEqual({v['domain'] for v in vals},{'education','health','civic'})
    def test_scope_guide_output_wont_overwrite(self):
        from subprocess import run
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'scope.json'
            call=[sys.executable,str(arketype.ROOT/'arketype.py'),'scope-guide','--profile','dossier-medical','--output',str(target)]
            a=run(call,capture_output=True,text=True)
            self.assertEqual(a.returncode,0,a.stderr)
            self.assertEqual(json.loads(target.read_text())['status'],'draft_requires_review')
            b=run(call,capture_output=True,text=True)
            self.assertNotEqual(b.returncode,0)
    def test_create_with_profile_does_not_write_scope_to_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            path=arketype.create('dossier-suivi','school-test','School Test',td,usage_profile='dossier-scolaire')
            origin=arketype.read_json(path/'arketype.instance.json')
            self.assertEqual(origin['use_case_profile'],'dossier-scolaire')
            self.assertEqual(origin['library_version'],'1.6.0')
            self.assertEqual(arketype.read_json(path/'design/scope-guidance.json')['status'],'draft_requires_review')
            self.assertNotIn('scope_guidance',arketype.read_json(path/'kristal.workspace.json'))
            self.assertFalse(origin['published'])
    def test_wrong_profile_type_does_not_write(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                arketype.create('diagnostic-causal','bad-one','Bad',td,usage_profile='dossier-scolaire')
            self.assertFalse((Path(td)/'bad-one').exists())

class MetadataReaderTests(unittest.TestCase):
    def make_zip(self,path):
        with zipfile.ZipFile(path,'w') as z:
            z.writestr('campus/university/state.json','{"private": "ignored"}')
            z.writestr('campus/voies/AS/cours/AS101/state.json','{}')
            z.writestr('cars/kristal.workspace.json',json.dumps({'format':'kristal.local-workspace/3.2.0','title':'Vehicle diagnostics','native_model':{'kind':'multiplex_causal_diagnostic_model'},'state_scope':{'subdomain':'automotive/diagnostics'}}))
            z.writestr('cars/canon/private-sensitive.json', '{"patient_secret": "never read"}')
            z.writestr('../unsafe','{}')
    def test_zip_focus_isolation(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'archive.zip';self.make_zip(path)
            campus=inspect_local(path,focus='campus')
            self.assertEqual(len(campus['workspace_metadata']),0)
            result=recognize(campus,arketype.use_case_profiles())
            self.assertEqual(result['candidates'][0]['profile_slug'],'campus-federe')
            cars=recognize(inspect_local(path,focus='cars'),arketype.use_case_profiles())
            self.assertEqual(cars['candidates'][0]['profile_slug'],'diagnostic-vehicule')
    def test_no_raw_private_content_copied(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'archive.zip';self.make_zip(path)
            scanned=inspect_local(path,focus='cars')
            self.assertNotIn('patient_secret',str(scanned))
            self.assertNotIn('../unsafe',str(scanned))
    def test_unsafe_focus_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'archive.zip';self.make_zip(path)
            for invalid in ('../other','stuff/../campus'):
                with self.assertRaises(ValueError):inspect_local(path,focus=invalid)
    def test_multi_workspace_not_single_certainty(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'multi.zip'
            with zipfile.ZipFile(path,'w') as z:
                for name in ('First','Second'):
                    z.writestr(name+'/kristal.workspace.json',json.dumps({'slug':name,'native_model':{'kind':'unknown'}}))
            report=recognize(inspect_local(path),arketype.use_case_profiles())
            self.assertIn('Multiple workspaces',report['warnings'][0])
    def test_unrecognized_does_not_fabricate_type(self):
        with tempfile.TemporaryDirectory() as td:
            report=recognize(inspect_local(td),arketype.use_case_profiles())
            self.assertEqual(report['candidates'],[])
            self.assertEqual(report['status'],'heuristic_candidates_not_classification')

if __name__=='__main__':unittest.main()
