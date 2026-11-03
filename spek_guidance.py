"""Non-normative Arketype→Spek suggestions; never selects facts or a template at runtime."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FORMAT='arketype.spek-rhetorical-guidance/1.0'

class GuidanceError(ValueError): pass


def validate(*, spek_inventory: Path | None = None):
    data=json.loads((ROOT/'contracts/spek-rhetorical-guidance.json').read_text(encoding='utf-8'))
    if (data.get('format')!=FORMAT or data.get('status')!='non_normative_no_fact_selection' or
        data.get('scope')!='structural_hints_only' or not isinstance(data.get('mappings'),list)):
        raise GuidanceError('Contrat de suggestions Arketype invalide')
    known={p.stem for p in (ROOT/'archetypes').glob('*.json')}
    rows=data['mappings']; seen=set()
    for row in rows:
        slug=row.get('arketype_slug') if isinstance(row,dict) else None
        if slug not in known or slug in seen or row.get('semantic_permission')!='none' or row.get('selection_status')!='ai_editorial_choice_required':
            raise GuidanceError('Arketype inconnu ou attribution non permise')
        seen.add(slug)
        refs=row.get('candidate_templates')
        if not isinstance(refs,list) or not refs or len(refs)!=len(set(refs)) or not all(isinstance(r,str) and r.startswith('rhetorical.') and r.endswith('@1.0.0') for r in refs):
            raise GuidanceError('Suggestions Spek non versionnées ou dupliquées')
    if seen != known:
        raise GuidanceError('L’inventaire Arketype n’est pas intégralement couvert')
    if spek_inventory is not None:
        other=json.loads(Path(spek_inventory).read_text(encoding='utf-8'))
        if other.get('format')!='spek.rhetorical-research-inventory/1.0':
            raise GuidanceError('Inventaire rhétorique Spek incompatible')
        available={p['template_ref'] for p in other.get('patterns',[]) if isinstance(p,dict)}
        missing={r for row in rows for r in row['candidate_templates'] if r not in available}
        if missing:
            raise GuidanceError('Suggestions absentes du catalogue Spek versionné')
    return {'format':'arketype.spek-rhetorical-guidance-check/1.0','status':'PASS_NON_NORMATIVE',
            'arketypes':len(seen),'candidate_references':sum(len(row['candidate_templates']) for row in rows),
            'fact_selection':False,'publication_authorized':False}


def main(argv=None):
    import argparse
    p=argparse.ArgumentParser(description='Valider les liens non normatifs entre Arketype et Spek')
    p.add_argument('--spek-inventory',type=Path)
    a=p.parse_args(argv)
    try:
        print(json.dumps(validate(spek_inventory=a.spek_inventory),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as exc:
        p.exit(2,'REFUS : '+str(exc)+'\n')
    return 0


if __name__=='__main__':raise SystemExit(main())
