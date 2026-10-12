"""Tests standard library; aucun accès réseau ni publication."""
import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import arketype

class CatalogueTests(unittest.TestCase):
    def test_integrity(self):
        r=arketype.validate(check_kit=False)
        self.assertTrue(r['ok'],r['errors'])
        self.assertEqual(r['archetype_count'],19)
        self.assertEqual(r['recipe_count'],14)
        self.assertEqual(r['profile_count'],5)
    def test_recherche_unicode(self):
        self.assertIn('parcours-pedagogique',[i['slug'] for i in arketype.search('PEDAGOGIQUE')])
        self.assertIn('procedure-protocole',[i['slug'] for i in arketype.search('PoliceOps')])
    def test_deposition_recherche(self):
        self.assertIn('deposition-temoignage',[a['slug'] for a in arketype.search('TÉMOIGNAGE')])
        self.assertIn('deposition-temoignage',[a['slug'] for a in arketype.search('Déposition')])
        self.assertEqual(len(arketype.search('',family='Sources')),1)
    def test_deposition_aucune_verite_impliquee(self):
        a=arketype.archetype('deposition-temoignage')
        self.assertFalse(a['canonical_claims_in_template'])
        path=arketype.ROOT/'modeles/deposition-temoignage'
        source=arketype.read_json(path/'design/fiche-deposition-vierge.json')
        self.assertIsNone(source['identifiant_deposition'])
        self.assertEqual(source['evaluation_distincte']['statut_factuel'],'non_evalue')
        self.assertFalse(source['validation_du_compte_rendu']['statut_verifie'])
        self.assertEqual(arketype.read_json(path/'canon/state.index.json').get('canonical_artifacts',[]),[])
    def test_deposition_assemblage(self):
        p=arketype.plan_for('deposition-temoignage',recipe='dossier-depositions')
        self.assertEqual(len(p['components']),3)
        self.assertFalse(p['publication_authorized'])
        self.assertTrue(all(c['status']=='unresolved' for c in p['components']))
    def test_familles(self):
        self.assertEqual(len(arketype.search('',family='Composition')),4)
    def test_plan_non_canonique(self):
        p=arketype.plan_for('referentiel-semantique',recipe='ekole-multiusage')
        self.assertEqual(len(p['components']),2)
        self.assertFalse(p['publication_authorized'])
        self.assertTrue(p['not_registered_as_logical_artifact'])
    def test_mismatch_recipe(self):
        with self.assertRaises(ValueError):
            arketype.plan_for('procedure-protocole',recipe='ekole-multiusage')
    def test_no_self_composition(self):
        with self.assertRaises(ValueError):
            arketype.plan_for('procedure-protocole',additions=['procedure-protocole'])
    def test_no_duplicate_component(self):
        p=arketype.plan_for('referentiel-semantique',recipe='ekole-multiusage',additions=['parcours-pedagogique'])
        self.assertEqual(len(p['components']),2)

class InstantiationTests(unittest.TestCase):
    def test_dry_run_no_write(self):
        with tempfile.TemporaryDirectory() as td:
            r=arketype.create('carte-jalons-preuves','nouveau-kristal','Un exemple',td,dry_run=True)
            self.assertFalse(r['will_write'])
            self.assertFalse((Path(td)/'nouveau-kristal').exists())
    def test_single_instance_clean_and_independent(self):
        with tempfile.TemporaryDirectory() as td:
            p=arketype.create('carte-jalons-preuves','mon-atlas-test','Mon atlas',td)
            self.assertTrue(p.is_dir())
            ws=arketype.read_json(p/'kristal.workspace.json')
            model_ws=arketype.read_json(arketype.ROOT/'modeles'/'carte-jalons-preuves'/'kristal.workspace.json')
            self.assertNotEqual(ws['state_ref'],model_ws['state_ref'])
            self.assertEqual(ws['slug'],'mon-atlas-test')
            self.assertEqual(ws['status'],'stub')
            self.assertEqual(arketype.read_json(p/'canon'/'state.index.json').get('artifacts',[]),[])
            self.assertEqual(arketype.read_json(p/'canon'/'state.index.json').get('canonical_artifacts',[]),[])
            self.assertEqual(arketype.read_json(p/'arketype.instance.json')['status'],'stub_no_domain_assertions')
            self.assertFalse(arketype.read_json(p/'design'/'composition-plan.json')['publication_authorized'])
            self.assertEqual([],list(Path(td).glob('.arketype-staging-*')))
    def test_composed_instance_plan(self):
        with tempfile.TemporaryDirectory() as td:
            p=arketype.create('referentiel-semantique','exemple-ekole','Référentiel',td,'ekole-multiusage')
            cp=arketype.read_json(p/'design'/'composition-plan.json')
            self.assertEqual(cp['recipe'],'ekole-multiusage')
            self.assertEqual(len(cp['components']),2)
            self.assertEqual(cp['ownership'],'to_define')
            self.assertFalse(arketype.read_json(p/'arketype.instance.json')['published'])
    def test_deposition_instance_contient_fiche_vierge(self):
        with tempfile.TemporaryDirectory() as td:
            dest=arketype.create('deposition-temoignage','auditions-test','Collecte d’essai',td)
            data=arketype.read_json(dest/'design/fiche-deposition-vierge.json')
            self.assertEqual(data['evaluation_distincte']['statut_factuel'],'non_evalue')
            self.assertFalse(arketype.read_json(dest/'arketype.instance.json')['published'])
            self.assertNotEqual(arketype.read_json(dest/'kristal.workspace.json')['state_ref'],
                                arketype.read_json(arketype.ROOT/'modeles/deposition-temoignage/kristal.workspace.json')['state_ref'])
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/'existant').mkdir()
            with self.assertRaises(FileExistsError):
                arketype.create('referentiel-semantique','existant','Existant',td)
    def test_path_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            for bad in ('../ailleurs','A-Majuscules','mon projet','-mauvais'):
                with self.subTest(bad=bad),self.assertRaises(ValueError):
                    arketype.create('referentiel-semantique',bad,'Test',td)
    def test_invalid_recipe_no_write(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                arketype.create('procedure-protocole','un-test','Un',td,recipe='ekole-multiusage')
            self.assertEqual([],list(Path(td).iterdir()))


class Upgrade121Tests(unittest.TestCase):
    def test_all_template_refs_unique_and_named(self):
        refs=[]
        for a in arketype.catalogue():
            model=arketype.ROOT/a['template_path']
            ws=arketype.read_json(model/'kristal.workspace.json')
            self.assertEqual(ws['slug'],'tpl-'+a['slug'])
            self.assertEqual(ws['state_ref'],'urn:kristal:state:tpl-'+a['slug'])
            self.assertFalse(arketype.read_json(model/'canon/state.index.json').get('artifacts',[]))
            refs.append(ws['state_ref'])
        self.assertEqual(len(set(refs)),19)
    def test_new_build_receipts_match_their_models(self):
        for slug in ('taxonomie-classification','etat-systemes','dossier-suivi'):
            model=arketype.ROOT/'modeles'/slug
            ws=arketype.read_json(model/'kristal.workspace.json')
            receipt=arketype.read_json(model/'build/v9/build-receipt.json')
            self.assertEqual(ws['state_ref'],receipt['state_ref'])
            self.assertEqual(receipt['generated_logical_artifacts'],0)
    def test_casefile_has_no_deposition_form(self):
        model=arketype.ROOT/'modeles/dossier-suivi'
        self.assertFalse((model/'design/fiche-deposition-vierge.json').exists())
        self.assertTrue((model/'design/fiche-suivi-vierge.json').exists())
    def test_profile_inventory_consistency(self):
        profiles=arketype.use_case_profiles()
        self.assertEqual(len(profiles),5)
        for profile in profiles:
            self.assertEqual(arketype.assembly(profile['assemblage_reference'])['primary_archetype'], profile['primary_archetype'])
    def test_diagrams_have_named_nodes_and_valid_edges(self):
        d=arketype.read_json(arketype.ROOT/'inventaires/diagrammes-situes.json')['diagrams']
        self.assertEqual(len(d),24)
        for diag in d:
            ids={n['id'] for n in diag['nodes']}
            self.assertTrue(all(n['label'] for n in diag['nodes']))
            self.assertTrue(all(e['from'] in ids and e['to'] in ids for e in diag['edges']))
            self.assertEqual(diag['status'],'illustration_non_canonique')
    def test_html_color_logo_and_sources(self):
        with tempfile.TemporaryDirectory() as td:
            dest=arketype.generate_html_catalog(Path(td)/'index.html')
            html=dest.read_text(encoding='utf-8')
            for term in ('#1e6864','../assets/logo-k.svg','diagrammes-situes.json','search-arch','beforeprint','Diagnostic causal','Taxonomie de la nature'):
                self.assertIn(term,html)
    def test_all_kits_check_locally(self):
        report=arketype.validate(check_kit=True)
        self.assertTrue(report['ok'],report['errors'])
    def test_new_archetype_instance_form(self):
        with tempfile.TemporaryDirectory() as td:
            dest=arketype.create('etat-systemes','essai-etat','Essai d’état',td)
            self.assertTrue((dest/'design/matrice-etat-vierge.json').is_file())
            self.assertFalse(arketype.read_json(dest/'arketype.instance.json')['published'])
    def test_dossier_instance_not_deposition(self):
        with tempfile.TemporaryDirectory() as td:
            dest=arketype.create('dossier-suivi','essai-dossier','Dossier neutre',td)
            self.assertFalse((dest/'design/fiche-deposition-vierge.json').exists())
            self.assertTrue((dest/'design/fiche-suivi-vierge.json').exists())
    def test_taxonomy_instance_is_independent(self):
        with tempfile.TemporaryDirectory() as td:
            dest=arketype.create('taxonomie-classification','essai-taxonomie','Taxonomie neutre',td)
            ref=arketype.read_json(dest/'kristal.workspace.json')['state_ref']
            self.assertNotEqual(ref,arketype.read_json(arketype.ROOT/'modeles/taxonomie-classification/kristal.workspace.json')['state_ref'])

if __name__=='__main__':unittest.main()
