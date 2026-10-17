#!/usr/bin/env python3
"""Arketype — local cataloguing and workspace instantiation.

Arketype metadata is non-normative documentation; local creation uses the bundled Authoring Kit.
This program never publishes, synchronizes, or activates a Kristal.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from use_cases import inspect_local, recognize, scope_guidance

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / 'catalogue.json'
VISUAL_INDEX = ROOT / 'inventaires' / 'grammaire-visuelle.json'
PROFILE_INDEX = ROOT / 'inventaires' / 'profils-usage.json'
VALID_SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError(f'Expected a JSON object : {path}')
    return value


def visual_grammar() -> dict:
    return read_json(VISUAL_INDEX)


def catalogue_index() -> dict:
    return read_json(INDEX)


def catalogue() -> list[dict]:
    index = catalogue_index()
    results = []
    for entry in index['archetypes']:
        rel = entry['file']
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise ValueError(f'Disallowed catalogue path : {rel}')
        results.append(read_json(ROOT / rel))
    return results


def archetype(slug: str) -> dict:
    match = next((item for item in catalogue() if item['slug'] == slug), None)
    if match is None:
        raise ValueError(f'Unknown archetype : {slug}. Use `python arketype.py list`.')
    return match


def assemblies() -> list[dict]:
    return [read_json(p) for p in sorted((ROOT / 'assemblages').glob('*.json'))]


def assembly(key: str) -> dict:
    match = next((r for r in assemblies() if r['id'] == key), None)
    if match is None:
        raise ValueError(f'Unknown assembly : {key}. Use `python arketype.py recipes`.')
    return match


def use_case_profiles() -> list[dict]:
    return read_json(PROFILE_INDEX)['profiles']


def use_case_profile(slug: str) -> dict:
    match = next((item for item in use_case_profiles() if item['slug'] == slug), None)
    if match is None:
        raise ValueError(f'Unknown use-case profile : {slug}. Use `python arketype.py profiles`.')
    return match


def normalized(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', str(s)).casefold() if not unicodedata.combining(c))


def search(term: str, family: str = '') -> list[dict]:
    term = normalized(term)
    found = []
    for a in catalogue():
        haystack = ' '.join(str(x) for x in [a['name'], a['slug'], a['description'], a['reference_use_case'], a['integrity_rule'], a.get('situational_schema',''), *a.get('canonical_use_cases', []), *a['primitive_candidates'], *a['structural_traits']])
        if (not term or term in normalized(haystack)) and (not family or normalized(a['family']) == normalized(family)):
            found.append(a)
    return found


def render_archetype(a: dict) -> str:
    return '\n'.join([
        f"{a['id']} — {a['name']}",
        f"Family: {a['family']} | Local Kit profile: {a['kit_profile']}",
        f"Purpose: {a['description']}",
        f"Visual pattern: {a.get('visual_pattern','')} / {a.get('structure_label','')}",
        f"Situated structure: {a.get('situational_schema','')}",
        f"Use cases: {', '.join(a.get('canonical_use_cases', []))}",
        f"Candidate primitives: {', '.join(a['primitive_candidates'])}",
        f"Integrity rule: {a['integrity_rule']}",
        f"Anti-pattern: {a['antipattern']}",
        f"Design question: {a['design_question']}",
        f"Reference example: {a['reference_use_case']}",
        f"Neutral template: {a['template_path']}",
        'Status: candidate, non-normative, with no domain assertions.'
    ])


def render_profile(p: dict) -> str:
    return '\n'.join([
        f"{p['id']} — {p['name']}",
        f"Primary archetype: {p['primary_archetype']}",
        f"Supporting archetypes: {', '.join(p['supporting_archetypes'])}",
        f"Visual pattern: {p['visual_pattern']}",
        f"Summary: {p['summary']}",
        f"Situated structure: {p['situational_schema']}",
        f"Use cases: {', '.join(p['use_cases'])}",
        f"Boundaries: {' | '.join(p['boundaries'])}",
        f"Usage: {p['usage_family']} | Domain: {p['domain']}",
        f"Integration targets: {', '.join(p['integration_targets']) or 'none specified'}",
        f"Coverage questions: {'; '.join(c['label'] for c in p['coverage_checks'])}",
        f"Assembly: {p['assemblage_reference']}"
    ])


def plan_for(primary: str, recipe: str | None = None, additions: list[str] | None = None) -> dict:
    archetype(primary)
    components = []
    guidance = 'Define boundaries, contracts, references and potential information loss before integration.'
    if recipe:
        design = assembly(recipe)
        if design['primary_archetype'] != primary:
            raise ValueError('Primary archetype does not match the requested assembly.')
        components = [dict(c) for c in design['components']]
        guidance = design['guidance']
    for slug in additions or []:
        archetype(slug)
        if slug == primary:
            raise ValueError('An archetype cannot be added to itself.')
        if any(c['archetype'] == slug for c in components):
            continue
        components.append({'archetype':slug, 'relation':'a_decider',
                           'design_note':'Determine semantic ownership boundaries before admitting any canonical content.',
                           'status':'unresolved'})
    return {'format':'arketype.composition-plan/1.0-non-normatif',
            'primary_archetype':primary,'recipe':recipe,
            'components':components,'guidance':guidance,
            'status':'unresolved_design_not_canonical',
            'ownership': 'to_define', 'references_pinned':[],
            'logical_contracts':'to_define',
            'publication_authorized':False,'activation_authorized':False,
            'not_registered_as_logical_artifact':True}


def create(type_slug: str, slug: str, title: str, parent: str | Path,
           recipe: str | None = None, additions: list[str] | None = None,
           dry_run: bool = False, usage_profile: str | None = None,
           authoring: str = "legacy") -> Path | dict:
    a = archetype(type_slug)
    if authoring not in ('legacy', 'v11'):
        raise ValueError('Supported authoring modes: legacy, v11.')
    if not VALID_SLUG.fullmatch(slug or '') or len(slug) > 80:
        raise ValueError('Expected slug: lowercase ASCII letters, digits and hyphens (1–80 characters).')
    if not title or not title.strip() or len(title.strip()) > 250:
        raise ValueError('Expected a nonblank title of 1–250 characters.')
    if '\x00' in str(parent):
        raise ValueError('Invalid path.')
    parent = Path(parent).expanduser().resolve(strict=True)
    if not parent.is_dir():
        raise ValueError(f'Parent path is not a directory : {parent}')
    destination = parent / slug
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Destination already exists : {destination}')
    use_profile = use_case_profile(usage_profile) if usage_profile else None
    if use_profile and use_profile['primary_archetype'] != type_slug:
        raise ValueError('Usage profile primary archetype does not match requested type.')
    if use_profile and recipe and recipe != use_profile['assemblage_reference']:
        raise ValueError('Usage profile and assembly recipe disagree.')
    if use_profile and not recipe: recipe = use_profile['assemblage_reference']
    plan = plan_for(type_slug, recipe, additions)
    if dry_run:
        return {'destination': str(destination), 'archetype': a['id'], 'title':title.strip(),
                'plan':plan,'usage_profile':usage_profile,'authoring_mode':authoring,
                'strict_v11_enabled':False,'will_write':False}
    tool = (ROOT / 'outils/authoring_v11/tools/kristal.py' if authoring == 'v11'
            else ROOT / 'outils/kristal.py')
    model = ROOT / a['template_path']
    if not tool.is_file() or not model.is_dir():
        raise FileNotFoundError('Bundled Authoring Kit or archetype template is missing from this Arketype archive.')
    with tempfile.TemporaryDirectory(prefix='.arketype-staging-', dir=str(parent)) as td:
        working = Path(td) / 'workspace'
        def run_kit(args: list[str]) -> None:
            p = subprocess.run([sys.executable, str(tool if args[0] == 'init' else working/'tools'/'kristal.py'), *args], capture_output=True,text=True,encoding='utf-8',errors='replace', timeout=120)
            if p.returncode:
                raise RuntimeError('Authoring Kit ('+args[0]+') :\n'+p.stdout+'\n'+p.stderr)
        run_kit(['init',str(working),'--slug',slug,'--title',title.strip(),'--profile',a['kit_profile']])
        ws_file=working/'kristal.workspace.json'
        ws=read_json(ws_file)
        source_ws=read_json(model/'kristal.workspace.json')
        ws['native_model']['kind']=a['native_kind_candidate']
        ws['native_model']['description']='Arketype candidate structure; domain knowledge and Logical Contract remain undefined.'
        ws['semantic_ownership']=source_ws['semantic_ownership']
        ws_file.write_text(json.dumps(ws,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        (working/'design').mkdir(exist_ok=True)
        for candidate in ('structure-candidate.json', 'fiche-deposition-vierge.json', 'fiche-suivi-vierge.json', 'matrice-etat-vierge.json'):
            source = model / 'design' / candidate
            if source.is_file():
                shutil.copyfile(source, working / 'design' / candidate)
        for filename in ('00_INTENT_AND_SCOPE.md','01_SEMANTIC_BOUNDARY.md','02_NATIVE_MODEL.md','03_EPISTEMIC_MODEL.md','ARKETYPE.md'):
            source = model/'docs'/filename
            if source.is_file():
                shutil.copyfile(source,working/'docs'/filename)
        with (working/'docs'/'ARKETYPE.md').open('a',encoding='utf8') as f:
            f.write(f'\n## Local instance\n\n- Title: **{title.strip()}**\n- Slug : `{slug}`\n- Initial state: `{ws["state_ref"]}`\n- Contracts and assertions: **not yet defined**.\n')
        if use_profile:
            (working/'design'/'scope-guidance.json').write_text(json.dumps(scope_guidance(use_profile),ensure_ascii=False,indent=2)+'\n','utf8')
        (working/'design'/'composition-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n','utf8')
        (working/'arketype.instance.json').write_text(json.dumps({
             'format':'arketype.instance-origin/1.0-non-normatif',
             'library_version':'1.6.0','primary_archetype':type_slug,
             'use_case_profile':usage_profile,
             'assembly_recipe':recipe,'additional_archetypes':[p['archetype'] for p in plan['components']],
             'state_ref_at_initialization':ws['state_ref'],
             'authoring_kit_reference':'4.0.0-draft.3' if authoring == 'v11' else '3.2.4',
             'v11_readiness':'identity_registry_and_graph_not_created' if authoring == 'v11' else 'legacy_template',
             'status':'stub_no_domain_assertions','published':False,
             'authorized_for_publication':False
             },ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        if authoring == 'v11':
            # No invented KQ, KP, Wikidata Q, default language or bogus claims.
            # Authoring v4 can check v11 ONLY after actual identities and v9
            # registered artifacts exist; creation is still an empty v9 stub.
            note = working/'design'/'v11-semantic-readiness.json'
            note.write_text(json.dumps({
                'format':'arketype.v11-readiness/1.0-non-canonical',
                'framework_baseline':'11.0.0-draft.4',
                'authoring_kit_baseline':'4.0.0-draft.3',
                'state':'pending_identity_allocation_and_review',
                'strict_v11_enabled':False,
                'no_provisional_wikidata_qids':True,
                'do_not_infer_identity_from_words':True,
                'steps':[
                    'Allocate namespace-scoped KQ/KP/KA/KS through an authorized identity registry.',
                    'Prepare strict v11 canonical graph, distinct lexical catalog and reviewed Wikidata crosswalk.',
                    'Register graph/registry/crosswalk/catalog as new v9 logical artifacts.',
                    'Run tools/kristal.py enable-v11 with registered paths, then check-v11, check and build-v9.',
                    'Use diK for separately versioned lexical completeness reports and reviewed conversion plans.'
                ],
                'publication_authorized':False
            }, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
        run_kit(['check',str(working)])
        index=read_json(working/'canon'/'state.index.json')
        if index.get('artifacts',[]) or index.get('canonical_artifacts',[]):
            raise ValueError('Workspace is not empty; refusing to initialize.')
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f'Destination appeared during initialization : {destination}')
        working.rename(destination)
    return destination


def _diagram_svg(pattern: str) -> str:
    if pattern == 'linear':
        return '<svg viewBox="0 0 220 70" class="diag"><rect x="10" y="20" width="35" height="24" rx="4"/><rect x="65" y="20" width="35" height="24" rx="4"/><rect x="120" y="20" width="35" height="24" rx="4"/><rect x="175" y="20" width="35" height="24" rx="4"/><path d="M45 32 H65 M100 32 H120 M155 32 H175"/></svg>'
    if pattern == 'branching':
        return '<svg viewBox="0 0 240 100" class="diag"><rect x="10" y="38" width="35" height="24" rx="4"/><rect x="70" y="38" width="35" height="24" rx="4"/><rect x="130" y="10" width="35" height="24" rx="4"/><rect x="130" y="66" width="35" height="24" rx="4"/><rect x="190" y="38" width="35" height="24" rx="4"/><path d="M45 50 H70 M105 50 L130 22 M105 50 L130 78 M165 22 L190 50 M165 78 L190 50"/></svg>'
    if pattern == 'hub':
        return '<svg viewBox="0 0 200 150" class="diag"><rect x="80" y="60" width="40" height="28" rx="4"/><rect x="80" y="10" width="40" height="24" rx="4"/><rect x="15" y="60" width="40" height="24" rx="4"/><rect x="145" y="60" width="40" height="24" rx="4"/><rect x="80" y="115" width="40" height="24" rx="4"/><path d="M100 34 V60 M55 72 H80 M120 72 H145 M100 88 V115"/></svg>'
    if pattern == 'cluster':
        return '<svg viewBox="0 0 220 130" class="diag"><circle cx="40" cy="45" r="16"/><circle cx="85" cy="30" r="16"/><circle cx="95" cy="80" r="16"/><circle cx="145" cy="55" r="16"/><circle cx="185" cy="80" r="16"/><path d="M54 41 L69 34 M53 52 L80 72 M101 34 L129 50 M110 78 L169 80 M111 69 L130 60"/></svg>'
    if pattern == 'tree':
        return '<svg viewBox="0 0 220 140" class="diag"><rect x="90" y="8" width="40" height="24" rx="4"/><rect x="35" y="58" width="40" height="24" rx="4"/><rect x="145" y="58" width="40" height="24" rx="4"/><rect x="10" y="108" width="40" height="24" rx="4"/><rect x="65" y="108" width="40" height="24" rx="4"/><rect x="145" y="108" width="40" height="24" rx="4"/><path d="M110 32 V45 H55 V58 M110 45 H165 V58 M55 82 V95 H30 V108 M55 95 H85 V108 M165 82 V108"/></svg>'
    if pattern == 'timeline':
        return '<svg viewBox="0 0 240 70" class="diag"><line x1="20" y1="35" x2="220" y2="35"/><circle cx="40" cy="35" r="8"/><circle cx="95" cy="35" r="8"/><circle cx="150" cy="35" r="8"/><circle cx="205" cy="35" r="8"/></svg>'
    if pattern == 'matrix':
        return '<svg viewBox="0 0 220 120" class="diag"><rect x="50" y="20" width="130" height="80" rx="2"/><line x1="50" y1="46" x2="180" y2="46"/><line x1="50" y1="72" x2="180" y2="72"/><line x1="93" y1="20" x2="93" y2="100"/><line x1="136" y1="20" x2="136" y2="100"/><circle cx="115" cy="59" r="5"/><circle cx="158" cy="85" r="5"/><circle cx="72" cy="85" r="5"/></svg>'
    if pattern == 'casefile':
        return '<svg viewBox="0 0 220 130" class="diag"><rect x="18" y="15" width="80" height="100" rx="4"/><rect x="122" y="20" width="70" height="20" rx="4"/><rect x="122" y="52" width="70" height="20" rx="4"/><rect x="122" y="84" width="70" height="20" rx="4"/><path d="M98 35 H122 M98 65 H122 M98 95 H122"/></svg>'
    if pattern == 'multilayer':
        return '<svg viewBox="0 0 220 120" class="diag"><rect x="40" y="10" width="140" height="24" rx="4"/><rect x="40" y="48" width="140" height="24" rx="4"/><rect x="40" y="86" width="140" height="24" rx="4"/></svg>'
    if pattern == 'network':
        return '<svg viewBox="0 0 220 140" class="diag"><circle cx="40" cy="30" r="14"/><circle cx="180" cy="30" r="14"/><circle cx="40" cy="110" r="14"/><circle cx="180" cy="110" r="14"/><circle cx="110" cy="70" r="16"/><path d="M53 37 L96 61 M167 37 L124 61 M53 103 L96 79 M167 103 L124 79 M54 30 H166 M54 110 H166"/></svg>'
    return '<svg viewBox="0 0 220 70" class="diag"></svg>'


def generate_html_catalog(output_path: Path | None = None) -> Path:
    """Render the JSON inventories as a self-contained offline HTML catalogue."""
    from catalogue.renderer import build
    return build(ROOT, output_path)


def validate(check_kit: bool = False) -> dict:
    errors=[]
    index=catalogue_index()
    if index.get('format')!='arketype.catalog/1.0-non-normatif':
        errors.append('Invalid catalogue format.')
    types=catalogue()
    if len(types) != len(index['archetypes']): errors.append('Archetype index and records have different counts.')
    allowed_patterns = {p['id'] for p in visual_grammar()['patterns']}
    slugs=set();ids=set();state_refs=set()
    for i,a in zip(index['archetypes'],types):
        slug=a.get('slug','')
        if slug in slugs: errors.append(f'Duplicate slug : {slug}')
        slugs.add(slug)
        if a.get('id') in ids: errors.append(f'Duplicate ID : {a.get("id")}')
        ids.add(a.get('id'))
        if (slug,i['id']) != (i['slug'],a.get('id')):
            errors.append(f'Catalogue index mismatch : {slug}')
        if not VALID_SLUG.fullmatch(slug): errors.append(f'Invalid slug : {slug}')
        if a.get('family') not in ('Knowledge','Composition','Structures','Processes','Sources'):
            errors.append(f'{slug}: unknown family')
        for required in ['name','description','family','kit_profile','native_kind_candidate','integrity_rule','template_path','antipattern','design_question','visual_pattern','situational_schema','structure_label']:
            if not a.get(required): errors.append(f'{slug}: missing required field {required}')
        if a.get('visual_pattern') not in allowed_patterns: errors.append(f'{slug}: unknown visual pattern')
        if a.get('kind')!='open_archetype_not_standard' or a.get('canonical_claims_in_template') is not False:
            errors.append(f'{slug}: archetype incorrectly claims normative status or preloaded domain data.')
        p=ROOT / a['template_path']
        if not p.is_dir():errors.append(f'{slug}: template missing');continue
        if p.resolve().parent != (ROOT/'modeles').resolve():errors.append(f'{slug}: disallowed template path')
        try:
            ws=read_json(p/'kristal.workspace.json')
            ca=read_json(p/'canon'/'state.index.json')
            shape=read_json(p/'design'/'structure-candidate.json')
            template_meta=read_json(p/'arketype.template.json')
            if ws.get('slug') != 'tpl-'+slug: errors.append(f'{slug}: template slug mismatch')
            if ws.get('state_ref') != 'urn:kristal:state:tpl-'+slug: errors.append(f'{slug}: template state_ref mismatch')
            if ws.get('state_ref') in state_refs: errors.append(f'{slug}: duplicate state_ref')
            state_refs.add(ws.get('state_ref'))
            receipt=read_json(p/'build/v9/build-receipt.json')
            if receipt.get('state_ref') != ws.get('state_ref'): errors.append(f'{slug}: build-v9 receipt mismatch')
            if receipt.get('generated_logical_artifacts') != 0: errors.append(f'{slug}: receipt contains generated domain artifacts')
            if ws['profile'] != a['kit_profile']: errors.append(f'{slug}: profile mismatch')
            if ws['native_model']['kind'] != a['native_kind_candidate']: errors.append(f'{slug}: native kind mismatch')
            if ws.get('status') != 'stub':errors.append(f'{slug}: template is not a neutral stub')
            if ca.get('canonical_artifacts',[]) or ca.get('artifacts',[]):errors.append(f'{slug}: canon non vide')
            if shape.get('id_type') != a['id']:errors.append(f'{slug}: design scaffold mismatch')
            if template_meta.get('archetype_id')!=a['id']:errors.append(f'{slug}: template origin mismatch')
            if template_meta.get('format')!='arketype.template/1.0-non-normatif':
                errors.append(f'{slug}: unknown template metadata format')
            if slug == 'deposition-temoignage':
                dep = read_json(p / 'design' / 'fiche-deposition-vierge.json')
                if dep.get('statut') != 'FORMULAIRE_VIERGE_HORS_CANON_NE_PAS_REMPLIR_DANS_LE_REPO':
                    errors.append('deposition-temoignage: non-neutral blank form')
                if dep.get('evaluation_distincte', {}).get('statut_factuel') != 'non_evalue':
                    errors.append('deposition-temoignage: preset factual conclusions')
            if slug == 'dossier-suivi':
                if (p/'design'/'fiche-deposition-vierge.json').exists():
                    errors.append('dossier-suivi: copied deposition form')
                form = read_json(p/'design'/'fiche-suivi-vierge.json')
                if form.get('evaluation',{}).get('statut') != 'non_evalue':
                    errors.append('dossier-suivi: non-neutral assessment')
            if slug == 'etat-systemes':
                form = read_json(p/'design'/'matrice-etat-vierge.json')
                if not form.get('dimensions'):
                    errors.append('etat-systemes: matrix has no dimensions')
            if check_kit:
                p_check=subprocess.run([sys.executable,str(p/'tools'/'kristal.py'),'check',str(p)], capture_output=True,text=True,timeout=120)
                if p_check.returncode: errors.append(f'{slug}: Authoring Kit check failed: {p_check.stderr[-300:]}')
        except (OSError,ValueError,KeyError) as exc:
            errors.append(f'{slug}: {exc}')
    recipes=assemblies();recipes_id=set()
    for r in recipes:
        if r['id'] in recipes_id:errors.append('Duplicate assembly : '+r['id'])
        recipes_id.add(r['id'])
        if r.get('primary_archetype') not in slugs:errors.append(r['id']+': unknown primary archetype')
        if r.get('composition_status')!='design_only':errors.append(r['id']+': assembly incorrectly claims canonical status')
        if r.get('publication_authorization') is not False:errors.append(r['id']+': unauthorized publication permission')
        for c in r['components']:
            if c['archetype'] not in slugs:errors.append(r['id']+': unknown component '+c['archetype'])
            if c['archetype']==r['primary_archetype']:errors.append(r['id']+': self-composition')
            if c.get('status')!='unresolved':errors.append(r['id']+': link marked resolved without evidence')
    profs=use_case_profiles(); profile_ids=set(); profile_slugs=set()
    for p in profs:
        if p['id'] in profile_ids: errors.append('Duplicate profile : '+p['id'])
        profile_ids.add(p['id'])
        if p['slug'] in profile_slugs: errors.append('Duplicate profile slug: '+p['slug'])
        profile_slugs.add(p['slug'])
        if p.get('profile_status') != 'design_guidance_only': errors.append(p['slug']+': unsafe profile status')
        if not p.get('coverage_checks'):errors.append(p['slug']+': missing coverage checks')
        if any(c.get('status')!='not_evaluated' or c.get('evaluation')!='manual_evidence_required' for c in p.get('coverage_checks',[])):errors.append(p['slug']+': cannot pre-qualify coverage')
        if not p.get('usage_family') or not p.get('domain') or not isinstance(p.get('integration_targets'),list):errors.append(p['slug']+': incomplete use-case dimensions')
        try:
            plan = assembly(p['assemblage_reference'])
            if plan['primary_archetype'] != p['primary_archetype']:errors.append(p['slug']+': inconsistent assembly primary archetype')
        except ValueError as exc: errors.append(str(exc))
        if p.get('primary_archetype') not in slugs: errors.append(p['slug']+': unknown primary archetype')
        for s in p.get('supporting_archetypes',[]):
            if s not in slugs: errors.append(p['slug']+': unknown supporting archetype '+s)
        if p.get('visual_pattern') not in allowed_patterns: errors.append(p['slug']+': unknown visual pattern')
    # Graphs: each archetype and profile has a valid, noncanonical situated diagram.
    diagrams=read_json(ROOT/'inventaires'/'diagrammes-situes.json')['diagrams']
    visual_index=read_json(ROOT/'inventaires'/'archetypes-visuels.json')['archetypes']
    if len(visual_index)!=len(types): errors.append('Visual inventory: record count mismatch')
    if {(a['slug'],a['visual_pattern']) for a in visual_index} != {(a['slug'],a['visual_pattern']) for a in types}:
        errors.append('Inventaire visuel : alignement incorrect')
    expected={('archetype',a['slug'],a['visual_pattern']) for a in types} | {('profile',p['slug'],p['visual_pattern']) for p in profs}
    actual={(d['kind'],d['slug'],d['pattern']) for d in diagrams}
    if actual!=expected or len(diagrams)!=len(expected): errors.append('Situated diagrams: identity or coverage mismatch')
    for d in diagrams:
        if d.get('status')!='illustration_non_canonique': errors.append(d['slug']+': diagram incorrectly marked canonical')
        labels={n['id'] for n in d['nodes']}
        if len(labels)!=len(d['nodes']): errors.append(d['slug']+': duplicate nodes')
        if not labels or any(not n.get('label') for n in d['nodes']): errors.append(d['slug']+': unlabeled nodes')
        if any(e.get('from') not in labels or e.get('to') not in labels for e in d['edges']): errors.append(d['slug']+': edge references an unknown node')
    taxonomy=read_json(ROOT/'inventaires/taxonomie-usages.json')
    known_usage=set(taxonomy['axes']['usage_family']['values'])
    known_domains=set(taxonomy['axes']['domain']['values'])
    for p in profs:
        if p.get('usage_family') not in known_usage or p.get('domain') not in known_domains:errors.append(p['slug']+': taxonomy mismatch')
    if not (ROOT/'schemas/use-case-profile.schema.json').is_file() or not (ROOT/'schemas/arketype.scope-guidance.schema.json').is_file():errors.append('Missing use-case contracts')
    if not (ROOT/'assets/logo-k.svg').is_file(): errors.append('Logo SVG absent')
    return {'ok':not errors,'archetype_count':len(types),'recipe_count':len(recipes),'profile_count':len(profs),'situated_diagrams':len(diagrams),'local_kit_checks':check_kit,'errors':errors}


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(prog='arketype.py',description='Arketype — non-normative Kristal archetype library.')
    commands=parser.add_subparsers(dest='command',required=True)
    ls=commands.add_parser('list',help='List archetypes')
    ls.add_argument('--family',default='',help='Family: Knowledge, Composition, Structures, Processes, Sources')
    sh=commands.add_parser('show',help='Show archetype details');sh.add_argument('slug')
    se=commands.add_parser('search',help='Search names, use cases and properties');se.add_argument('term')
    rec=commands.add_parser('recipes',help='List design-only assemblies')
    rp=commands.add_parser('recipe',help='Show assembly details');rp.add_argument('id')
    pr=commands.add_parser('profiles',help='List use-case profiles')
    pf=commands.add_parser('profile',help='Show a use-case profile');pf.add_argument('slug')
    us=commands.add_parser('uses',help='List use-case family and domain dimensions')
    rco=commands.add_parser('recognize',help='Read-only profile suggestions from local directory or ZIP metadata')
    rco.add_argument('--path',required=True);rco.add_argument('--focus',default='',help='Optional ZIP-internal subproject prefix');rco.add_argument('--limit',type=int,default=6)
    guide=commands.add_parser('scope-guide',help='Generate noncanonical scope guidance (not an injection payload)')
    guide.add_argument('--profile',required=True);guide.add_argument('--path',default='');guide.add_argument('--focus',default='');guide.add_argument('--output',default='')
    bh=commands.add_parser('build-html',help='Generate the offline HTML catalogue');bh.add_argument('--output',default='')
    v=commands.add_parser('validate',help='Check Arketype consistency (read-only)');v.add_argument('--check-kit',action='store_true')
    for command in ('create','compose'):
        p=commands.add_parser(command,help='Create a local Kristal or prepare a composition')
        p.add_argument('--type',help='Primary archetype; optional with --recipe or --profile')
        p.add_argument('--profile',help='Optional use-case profile to attach to the neutral workspace')
        p.add_argument('--recipe',help='Predefined assembly')
        p.add_argument('--with',dest='additions',action='append',default=[],metavar='ARCHETYPE',help='Additional archetype; repeat if needed')
        p.add_argument('--slug',required=True,help='Slug for the new Kristal')
        p.add_argument('--title',required=True,help='Title for the new Kristal')
        p.add_argument('--parent',required=True,help='Existing parent directory for new workspace')
        p.add_argument('--dry-run',action='store_true',help='Preview without writing')
        p.add_argument('--authoring', choices=['legacy','v11'], default='legacy', help='v11: new blank Kit 4 draft workspace + KQ/KP readiness guidance; does NOT mint IDs or enable strict v11')
    s = commands.add_parser('semantic-status',help='Read-only v11 readiness from local workspace metadata; never claims domain qualification')
    s.add_argument('--path',required=True)
    s = commands.add_parser('dik-coverage',help='Run the explicitly selected local diK CLI in read-only coverage mode')
    s.add_argument('--project',required=True)
    s.add_argument('--dik-root',required=True,help='Explicit local diK source checkout, not downloaded or executed implicitly')
    s.add_argument('--locales',help='Comma-separated list of selected catalog locales')
    args=parser.parse_args(argv)
    try:
        if args.command=='list':
            for a in catalogue():
                if not args.family or normalized(args.family)==normalized(a['family']):
                    print(f"{a['id']}  {a['slug']:28} {a['name']} [{a['family']}]")
        elif args.command=='show':
            print(render_archetype(archetype(args.slug)))
        elif args.command=='search':
            matches=search(args.term)
            for a in matches: print(f"{a['id']}  {a['slug']} — {a['name']}")
            if not matches: print('No matching archetypes found.')
        elif args.command=='recipes':
            for r in assemblies():print(f"{r['id']:25} {r['title']} (primary: {r['primary_archetype']})")
        elif args.command=='recipe':
            print(json.dumps(assembly(args.id),ensure_ascii=False,indent=2))
        elif args.command=='profiles':
            for p in use_case_profiles(): print(f"{p['id']:8} {p['slug']:28} {p['name']} -> {p['primary_archetype']}")
        elif args.command=='profile':
            print(render_profile(use_case_profile(args.slug)))
        elif args.command=='uses':
            print(json.dumps(read_json(ROOT/'inventaires/taxonomie-usages.json'),ensure_ascii=False,indent=2))
        elif args.command=='recognize':
            print(json.dumps(recognize(inspect_local(args.path,args.focus),use_case_profiles(),args.limit),ensure_ascii=False,indent=2))
        elif args.command=='scope-guide':
            data=scope_guidance(use_case_profile(args.profile),inspect_local(args.path,args.focus) if args.path else None)
            text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
            if args.output:
                dest=Path(args.output).expanduser().resolve()
                if dest.exists():raise FileExistsError('Output already exists; cannot overwrite.')
                if not dest.parent.is_dir(): raise ValueError('Output parent directory does not exist.')
                dest.write_text(text,encoding='utf-8')
                print(str(dest))
            else:print(text,end='')
        elif args.command=='semantic-status':
            from arketype_semantic import semantic_status
            print(json.dumps(semantic_status(Path(args.path)),ensure_ascii=False,indent=2))
        elif args.command=='dik-coverage':
            from arketype_semantic import run_dik_coverage
            print(run_dik_coverage(Path(args.dik_root),Path(args.project),args.locales),end='')
        elif args.command=='build-html':
            out = Path(args.output).expanduser() if args.output else None
            print(str(generate_html_catalog(out)))
        elif args.command=='validate':
            report=validate(args.check_kit)
            print(json.dumps(report,ensure_ascii=False,indent=2))
            return 0 if report['ok'] else 1
        elif args.command in ('create','compose'):
            typ=args.type or (assembly(args.recipe)['primary_archetype'] if args.recipe else None) or (use_case_profile(args.profile)['primary_archetype'] if args.profile else None)
            if not typ:parser.error('Provide --type, --recipe or --profile.')
            if args.command=='compose' and not (args.recipe or args.additions or args.profile):
                parser.error('compose requires --recipe or at least one --with.')
            result=create(typ,args.slug,args.title,args.parent,args.recipe,args.additions,args.dry_run,args.profile,args.authoring)
            if isinstance(result,dict):print(json.dumps(result,ensure_ascii=False,indent=2))
            else:print('Neutral Arketype workspace created and checked : '+str(result))
        return 0
    except (OSError,ValueError,RuntimeError,KeyError,subprocess.TimeoutExpired) as exc:
        print('Arketype ERROR : '+str(exc),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(main())
