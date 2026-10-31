"""Independent tests: structural observation never writes and never certifies."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ENGINE=Path(__file__).resolve().parents[1]/'structural_observer.py'
spec=importlib.util.spec_from_file_location('structural_observer',ENGINE)
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)

class StructureTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'demo';self.root.mkdir()
        (self.root/'canon'/'domain').mkdir(parents=True)
        self.metadata={'format':'kristal.local-workspace/3.2.0','state_ref':'urn:kristal:state:demo','classification':{'primary_archetype':'ARK-08','structure_mode':'archetype'}}
        (self.root/'kristal.workspace.json').write_text(json.dumps(self.metadata))
    def tearDown(self): self.temp.cleanup()
    def test_three_criteria_and_no_changes(self):
        f=self.root/'canon'/'domain'/'diagnostic.json'
        f.write_text(json.dumps({'symptoms':[], 'hypotheses':{},'tests':[{'measurement':1},{'measurement':2}]}))
        before=(f.read_bytes(),(self.root/'kristal.workspace.json').read_bytes())
        output=engine.inspect(self.root)
        self.assertEqual(output['declared_level'],'3/3')
        self.assertEqual(output['comparison'],'CORRESPONDANCE_OBSERVEE_3_SUR_3')
        self.assertTrue(output['declared_evidence']['facets'][0]['evidence'])
        self.assertEqual((f.read_bytes(),(self.root/'kristal.workspace.json').read_bytes()),before)
        self.assertFalse((self.root/'derived').exists())
    def test_declared_free_is_not_error(self):
        self.metadata['classification']={'structure_mode':'free','variant_description':'forme originale'}
        (self.root/'kristal.workspace.json').write_text(json.dumps(self.metadata))
        output=engine.inspect(self.root)
        self.assertEqual(output['declared_level'],'libre')
        self.assertEqual(output['comparison'],'LIBRE_DECLARE')
    def test_no_canon_is_indeterminate(self):
        output=engine.inspect(self.root)
        self.assertEqual(output['declared_level'],'indetermine')
    def test_no_free_text_false_positive(self):
        (self.root/'canon'/'domain'/'data.json').write_text(json.dumps({'description':'symptoms hypotheses tests'}))
        output=engine.inspect(self.root)
        self.assertEqual(output['declared_level'],'0/3')
    def test_profiles_are_complete(self):
        profiles=engine.read_profiles()['profiles']
        self.assertEqual(len(profiles),19)
        self.assertEqual(sorted(p['id'] for p in profiles),[f'ARK-{i:02d}' for i in range(1,20)])

if __name__=='__main__':unittest.main()
