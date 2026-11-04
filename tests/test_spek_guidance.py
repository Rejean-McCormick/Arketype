from pathlib import Path
from spek_guidance import validate

def test_all_arketype_suggestions_have_no_fact_authority():
    report=validate()
    assert report['arketypes']==19
    assert report['fact_selection'] is False
    assert report['publication_authorized'] is False


def test_spek_inventory_symlink_is_refused(tmp_path):
    import pytest
    from spek_guidance import GuidanceError
    target=tmp_path/'inventory.json'
    target.write_text('{}',encoding='utf-8')
    link=tmp_path/'redirect.json'
    try:
        link.symlink_to(target)
    except (OSError,NotImplementedError):
        pytest.skip('Symbolic links require privileges on this Windows host')
    with pytest.raises(GuidanceError,match='symbolique'):
        validate(spek_inventory=link)
