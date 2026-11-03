from pathlib import Path
from spek_guidance import validate

def test_all_arketype_suggestions_have_no_fact_authority():
    report=validate()
    assert report['arketypes']==19
    assert report['fact_selection'] is False
    assert report['publication_authorized'] is False
