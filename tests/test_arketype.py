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
        self.assertEqual(r['archetype_count'],16)
        self.assertEqual(r['recipe_count'],9)
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

if __name__=='__main__':unittest.main()
