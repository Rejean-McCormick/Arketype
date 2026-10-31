"""Arketype structural observation v0.1: optional, non normative, read-only.

This is NOT a Framework conformance checker. It counts observed JSON structural
markers and compares them to the three advisory facets of each Arketype profile.
Never infers semantic identity, validates KQ mappings or approves an archetype.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import unicodedata

FORMAT = 'arketype.structural-observation/0.1'
MAX_FILES = 500
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_NODES = 120000


def normalized(value):
    value = unicodedata.normalize('NFKD', str(value))
    value = ''.join(ch for ch in value if not unicodedata.combining(ch))
    return '_'.join(x for x in re.split('[^a-z0-9]+', value.casefold()) if x)


def read_profiles(arketype_root=None):
    root = Path(arketype_root) if arketype_root is not None else Path(__file__).resolve().parent.parent
    location = root / 'arketype' / 'contracts' / 'structural-profiles.json'
    if not location.is_file():
        raise FileNotFoundError(f'Catalogue de profils ARK introuvable : {location}')
    obj = json.loads(location.read_text(encoding='utf-8'))
    if obj.get('format') != 'arketype.structural-profiles/0.1':
        raise ValueError('Format de profils structuraux inconnu')
    return obj


def _observe(root):
    # Select *canonical* JSON only; no builds, snapshots, derived projections or docs.
    base = root / 'canon'
    markers = defaultdict(list)
    levels = Counter()
    repetitions = Counter()
    counted = {'files': 0, 'objects': 0, 'arrays': 0, 'scalars': 0, 'nodes': 0}
    skipped = []
    if not base.is_dir():
        return {'markers': {}, 'counts': counted, 'repetitions': [], 'files': [],
                'skipped': ['canon/ absent'], 'complete': False}
    files = []
    for path in sorted(base.rglob('*.json')):
        # The state index is a manifest of artifacts, not the Kristal's domain shape.
        if path.relative_to(base).as_posix() == 'state.index.json':
            continue
        if len(files) >= MAX_FILES:
            skipped.append('file_limit'); break
        if path.is_symlink() or not path.is_file():
            skipped.append(path.relative_to(root).as_posix() + ': symlink/non-fichier'); continue
        rel = path.relative_to(root).as_posix()
        if path.stat().st_size > MAX_FILE_BYTES:
            skipped.append(rel + ': trop volumineux'); continue
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, ValueError):
            skipped.append(rel + ': JSON illisible'); continue
        files.append(rel)
        counted['files'] += 1
        # File/path names are advisory structural evidence, not semantic values.
        for term in [normalized(path.stem), normalized(path.parent.name)]:
            if term and len(markers[term]) < 5: markers[term].append(rel + ' [chemin]')
        stack = [(data, '$', 0)]
        while stack and counted['nodes'] < MAX_NODES:
            value, json_path, depth = stack.pop()
            counted['nodes'] += 1
            levels[depth] += 1
            if isinstance(value, dict):
                counted['objects'] += 1
                for key, child in value.items():
                    token = normalized(key)
                    if token and len(markers[token]) < 5:
                        markers[token].append(rel + ' ' + json_path + '.' + str(key))
                    if depth < 24:stack.append((child, json_path+'.'+str(key), depth+1))
            elif isinstance(value, list):
                counted['arrays'] += 1
                if len(value) > 1: repetitions[(rel, json_path)] += len(value)
                if depth < 24:
                    # Count all elements up to node budget, no dependence on values.
                    for child in reversed(value):
                        stack.append((child, json_path+'[]', depth+1))
            else:
                counted['scalars'] += 1
        if counted['nodes'] >= MAX_NODES:
            skipped.append('node_limit'); break
    counted['distinct_fields'] = len(markers)
    return {'markers': dict(markers), 'counts': dict(counted), 'files': files,
            'fields': [{'key': k, 'examples': v[:2]} for k,v in sorted(markers.items())[:120]],
            'branches': dict(Counter(path.split('/')[1] if '/' in path else 'root' for path in files)),
            'repetitions': [{'path': a+' '+b, 'instances': n} for (a,b),n in repetitions.most_common(25)],
            'depth': max(levels,default=0), 'skipped': skipped, 'complete': not skipped}


def _match(markers, terms):
    # Exact normalized token or full word-group boundaries; never inspect free-text values.
    results=[]
    for term in terms:
        term = normalized(term)
        if not term:continue
        for key, locations in markers.items():
            if key == term or ('_'+term+'_') in ('_'+key+'_'):
                for loc in locations:
                    if loc not in results:results.append(loc)
            if len(results)>=5: return results[:5]
    return results


def _declaration(workspace):
    clas = workspace.get('classification') if isinstance(workspace,dict) else None
    clas = clas if isinstance(clas,dict) else {}
    return {'primary_archetype': clas.get('primary_archetype') if isinstance(clas.get('primary_archetype'),str) else None,
            'structure_mode': clas.get('structure_mode') if clas.get('structure_mode') in ('archetype','hybrid','free') else None,
            'supporting_archetypes': clas.get('supporting_archetypes') if isinstance(clas.get('supporting_archetypes'),list) else [],
            'variant_description': clas.get('variant_description') if isinstance(clas.get('variant_description'),str) else None}


def inspect(workspace_root, arketype_root=None):
    root=Path(workspace_root).expanduser().resolve()
    path=root/'kristal.workspace.json'
    if not path.is_file(): raise FileNotFoundError(f'Workspace absent : {path}')
    workspace=json.loads(path.read_text(encoding='utf-8'))
    profiles=read_profiles(arketype_root)
    obs=_observe(root)
    decl=_declaration(workspace)
    scored=[]
    for p in profiles['profiles']:
        facets=[]
        for f in p['facets']:
            evidence=_match(obs['markers'],f['markers'])
            facets.append({'criterion':f['id'],'label':f['label'],
                           'observed':bool(evidence),'evidence':evidence})
        score=sum(int(f['observed']) for f in facets)
        scored.append({'id':p['id'],'name':p['name'],'points':score,'out_of':3,
                       'level':f'{score}/3' if obs['files'] else 'indetermine',
                       'facets':facets})
    scored.sort(key=lambda p:(-p['points'],p['id']))
    declared=next((r for r in scored if r['id']==decl['primary_archetype']),None)
    if decl['structure_mode']=='free':
        comparison='LIBRE_DECLARE';level='libre'
    elif decl['primary_archetype'] and not declared:
        comparison='ARCHETYPE_INCONNU';level='indetermine'
    elif not decl['primary_archetype']:
        comparison='NON_DECLARE';level='indetermine'
    elif not obs['files']:
        comparison='PREUVE_INSUFFISANTE';level='indetermine'
    else:
        comparison={0:'CORRESPONDANCE_NON_OBSERVEE',1:'BASE_INSPIREE_1_SUR_3',
                    2:'STRUCTURE_ADAPTEE_2_SUR_3',3:'CORRESPONDANCE_OBSERVEE_3_SUR_3'}[declared['points']]
        level=declared['level']
    # Suggestions, never auto-declared nor accepted. Tie means ambiguity.
    top = [r for r in scored if r['points'] >= 2 and r['points'] == scored[0]['points']][:5]
    return {'format':FORMAT, 'project':root.name, 'path':str(root),
            'state_ref':workspace.get('state_ref'), 'declaration':decl,
            'comparison':comparison,'declared_level':level,
            'declared_evidence':declared,
            'suggestions':[{'id':r['id'],'name':r['name'],'score':r['level']} for r in top],
            'ambiguity':'PLUSIEURS_CANDIDATS' if len(top)>1 else ('CANDIDAT_NON_VALIDE' if top else 'AUCUN_CANDIDAT_PROBANT'),
            'structure':{'files':obs['files'],'counts':obs['counts'],'depth':obs['depth'],
                         'repetitions':obs['repetitions'],'skipped':obs['skipped'],
                         'observation_complete':obs['complete']},
            'limits':['Mesure indicative sur 3 critères de reconnaissance, pas conformité normative.',
                      'Uniquement les noms de champs et chemins canoniques JSON, jamais le sens des valeurs.',
                      'Une absence observée peut refléter une couverture partielle du lecteur.',
                      'Ne valide ni KQ/KP/KA/KS, ni Arketype, ni Framework C1/C2/C3.']}


def inspect_many(parent, arketype_root=None):
    base=Path(parent)
    roots=[base] if (base/'kristal.workspace.json').is_file() else sorted(p for p in base.iterdir() if p.is_dir() and (p/'kristal.workspace.json').is_file())
    results=[];errors=[]
    for p in roots:
        try:
            results.append(inspect(p,arketype_root=arketype_root))
        except (OSError, ValueError, TypeError, UnicodeError) as exc:
            errors.append({'project':p.name,'path':str(p),'error':str(exc)})
    return {'format':'arketype.structural-batch/0.1','results':results,'errors':errors}
