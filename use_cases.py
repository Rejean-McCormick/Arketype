"""Noncanonical profile recognition and scope guidance for local Kristal artifacts.

Read-only metadata inspection; does not traverse canon payloads or perform remote queries.
Recognition is a set of transparent candidate signals, not classification certainty.
"""
from __future__ import annotations
from pathlib import Path
import json
import unicodedata
import zipfile

SCAN_LIMIT = 15000
READ_LIMIT = 256_000
WORKSPACE_LIMIT = 60

# Hints are profile-specific affordances, never proof or a mandatory Kristal type.
HINTS = {
 'troubleshooting-systeme': {'tokens':['troubleshoot','failure analysis','support technique'],'paths':['diagnostic/']},
 'environnement-protocolaire': {'tokens':['protocol','sop','procédure'],'paths':['procedures/']},
 'taxonomie-nature': {'tokens':['taxonom','fauna','flora'],'paths':['taxonomies/']},
 'etat-de-systemes': {'tokens':['observability','system-state','monitoring'],'paths':['metrics/']},
 'suivi-employe': {'tokens':['employee','employé','ressources humaines'],'paths':['hr/']},
 'campus-federe': {'tokens':['uckk','university','université','federated campus'],'paths':['university/state.json','voies/','cours/']},
 'publication-moodle': {'tokens':['moodle','lms integration'],'paths':['moodle/','moodle.yml']},
 'collection-traditions': {'tokens':['traditions ancestrales','mythologies','mythology','religious traditions'],'paths':['kristals/akan-asante/','collection_kristals_traditions']},
 'organisations-sociales': {'tokens':['organisation humaine','organisations humaines','social structure','rôles, tâches'],'native_kinds':['graphe_de_societes_contextualisees_et_regles'],'paths':['modele-organisation-humaine/']},
 'navigation-preuves-longues': {'tokens':['proof landmarks','junction','endpoint','carrefour','math challenges'],'paths':['proof-landmarks.json','map/junctions.json','atlas/math-atlas.json']},
 'recherche-mathematique': {'tokens':['mathematical research','proof obligations','formulator','math research'],'paths':['research/proof-obligations.jsonl','research/active-frontier.json','src/formulator/']},
 'dossier-scolaire': {'tokens':['student file','dossier scolaire','suivi étudiant','suivi eleve'],'paths':['student-records/']},
 'dossier-medical': {'tokens':['medical follow-up','dossier médical','patient record','dossier patient'],'paths':['patient-records/']},
 'dossier-civique': {'tokens':['dossier civique','civic case','administrative case'],'paths':['civil-records/']},
 'diagnostic-vehicule': {'tokens':['vehiclediag','diagnostic automobile','automotive/diagnostics'],'native_kinds':['multiplex_causal_diagnostic_model'],'paths':['vehiclediag.structured-epistemic-state.json','oem-vehicle-scope.template.json']},
 'operations-police': {'tokens':['policeops','police ops','law enforcement procedures'],'paths':['police-procedures/']},
 'operations-hopital': {'tokens':['hospitalops','hospital ops','hospital protocols'],'paths':['hospital-protocols/']},
 'orchestration-medicale': {'tokens':['medikristal','medical-knowledge and diagnostic-pathway orchestration'],'paths':['MediKristal/contracts/','MediKristal/backend/','MediKristal/README.md']},
 'cartographie-scolaire': {'tokens':['scolqc','éducation québec','education-quebec','parcours scolaire et sémantique'],'paths':['education-quebec.structured-epistemic-state.json','knowledge-base/profiles/admission-auditor.json']},
 'referentiel-polyusage': {'tokens':['ekole','multi-usage semantic reference','multiusage'],'paths':['ekole-multiusage/']},
 'temoignages-enquete': {'tokens':['deposition','témoignage','witness statement'],'paths':['depositions/']},
}

def _norm(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD',str(s)).casefold() if not unicodedata.combining(c))

def _json_partial(content: bytes) -> dict:
    if len(content)>READ_LIMIT:
        return {}
    try:
        obj=json.loads(content.decode('utf-8-sig'))
        return obj if isinstance(obj,dict) else {}
    except (UnicodeDecodeError,json.JSONDecodeError):
        return {}

def inspect_local(path: str | Path, focus: str = '') -> dict:
    """Read file names and bounded workspace/origin metadata, never canonical knowledge records."""
    path=Path(path).expanduser().resolve(strict=True)
    if not (path.is_dir() or (path.is_file() and path.suffix.lower()=='.zip')):
        raise ValueError('Expected a local directory or ZIP archive.')
    focus=focus.replace('\\','/').strip('/')
    if focus and (focus.startswith('/') or '..' in focus.split('/')):
        raise ValueError('Unsafe focus prefix.')
    files=[]; ws=[]; origins=[]; skipped=0
    if path.is_dir():
        candidates=(p for p in path.rglob('*') if p.is_file() and not any(x in {'.git','.venv','node_modules','__pycache__'} for x in p.relative_to(path).parts))
        for f in candidates:
            if len(files)>=SCAN_LIMIT: skipped+=1;break
            name=f.relative_to(path).as_posix()
            if focus and not (name==focus or name.startswith(focus+'/')):continue
            files.append(name)
            if (f.name=='kristal.workspace.json' and len(ws)<WORKSPACE_LIMIT) or (f.name=='arketype.instance.json' and len(origins)<WORKSPACE_LIMIT):
                if f.stat().st_size<=READ_LIMIT:
                    d=_json_partial(f.read_bytes())
                    (ws if f.name=='kristal.workspace.json' else origins).append((name,d))
    else:
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():continue
                if len(files)>=SCAN_LIMIT:skipped+=1;break
                name=info.filename.replace('\\','/')
                if name.startswith('/') or any(part=='..' for part in name.split('/')): continue
                if focus and not (name==focus or name.startswith(focus+'/')):continue
                files.append(name)
                basename=name.rsplit('/',1)[-1]
                if ((basename=='kristal.workspace.json' and len(ws)<WORKSPACE_LIMIT) or (basename=='arketype.instance.json' and len(origins)<WORKSPACE_LIMIT)) and info.file_size<=READ_LIMIT:
                    d=_json_partial(z.read(info))
                    (ws if basename=='kristal.workspace.json' else origins).append((name,d))
    # Deliberately omit personal data or user-asserted full semantic content from observations.
    metadata=[]
    for name,d in ws:
        nm=d.get('native_model') or {}; subj=d.get('subject') or {}; sc=d.get('state_scope') or {}
        if not isinstance(nm,dict):nm={}
        if not isinstance(subj,dict):subj={}
        if not isinstance(sc,dict):sc={}
        metadata.append({'path':name,'format':d.get('format',''),'slug':d.get('slug',''),'title':d.get('title',''),'native_kind':nm.get('kind',''),'subject_label':subj.get('label',''), 'scope_domain':sc.get('domain',''),'scope_subdomain':sc.get('subdomain','')})
    return {'format':'arketype.local-observation/1.0','path':str(path),'target_type':'zip' if path.is_file() else 'directory','focus':focus or None, 'file_count_inspected':len(files),'possibly_more_files':bool(skipped),'workspace_metadata':metadata,'explicit_origins':[{'path':name,'profile':d.get('use_case_profile'),'archetype':d.get('primary_archetype'),'library_version':d.get('library_version')} for name,d in origins],'filenames':files}

def recognize(observation: dict, profiles: list[dict], limit: int=5) -> dict:
    files=observation['filenames']
    joined=_norm(' '.join(' '.join([str(w.get(k,'')) for k in ('slug','title','native_kind','subject_label','scope_domain','scope_subdomain')]) for w in observation['workspace_metadata']))
    basename=_norm(Path(observation['path']).name)
    matches=[]
    for p in profiles:
        signals=[];score=0; hints=HINTS.get(p['slug'],{})
        for x in hints.get('native_kinds',[]):
            if _norm(x) in joined:signals.append({'type':'native_kind','indicator':x,'score':6});score+=6
        for x in hints.get('tokens',[]):
            key=_norm(x)
            if key in joined:
                signals.append({'type':'workspace_metadata','indicator':x,'score':3});score+=3
            elif key in basename:
                signals.append({'type':'archive_or_directory_name','indicator':x,'score':1});score+=1
        for pattern in hints.get('paths',[]):
            if any(_norm(pattern) in _norm(n) for n in files):
                signals.append({'type':'file_path_signature','indicator':pattern,'score':4});score+=4
        for x in observation['explicit_origins']:
            if x.get('profile')==p['slug']:
                signals.append({'type':'explicit_instance_origin','indicator':p['slug'],'score':12});score+=12
        if score>=3:
            matches.append({'profile_slug':p['slug'],'name':p['name'],'primary_archetype':p['primary_archetype'],'score':score,'strength':'strong_indication' if score>=9 else 'suggestion' if score>=5 else 'weak_indication','signals':signals})
    matches.sort(key=lambda x:(-x['score'],x['profile_slug']))
    if len(observation['workspace_metadata'])>1 and not observation.get('focus'):
        note='Multiple workspaces detected: recommendations may represent different Kristals; inspect individually or use --focus.'
    else:note=None
    return {'format':'arketype.profile-recognition/1.0','status':'heuristic_candidates_not_classification','input':{'path':observation['path'],'type':observation['target_type'],'inspected_files':observation['file_count_inspected'],'workspaces':len(observation['workspace_metadata']),'truncated':observation['possibly_more_files']},'candidates':matches[:max(0,limit)],'candidate_count':len(matches),'warnings':([note] if note else [])+['Metadata/path matching is not proof of use, archetype origin or completeness.','No canonical claims, content, private casefile data or clinical records were inspected.']}

def scope_guidance(profile:dict, observation:dict|None=None) -> dict:
    return {'format':'arketype.scope-guidance/1.0','status':'draft_requires_review','profile_slug':profile['slug'],'profile_id':profile['id'],'structure':{'primary_archetype':profile['primary_archetype'],'supporting_archetypes':profile['supporting_archetypes'],'provenance':'candidate_from_design_catalog'},'dimensions':{'usage_family':profile['usage_family'],'domain':profile['domain'],'integration_targets':profile['integration_targets'],'authority':'external_required','data_access':'not_granted'},'inclusions':profile['scope_guidance']['include_candidates'],'exclusions':profile['scope_guidance']['exclude_candidates'],'coverage_questions':[{'question':c['label'],'status':'not_evaluated','evidence':'not_inspected'} for c in profile['coverage_checks']],'local_observation':{'path':observation['path'],'workspaces':observation['workspace_metadata'],'files_inspected':observation['file_count_inspected']} if observation else None,'limitations':['A suggested usage is not a verified description of any real state.','Scope needs owner review before mapping to the Skope proposal and injection contract.','No operational, medical, legal, access or publication authority is conferred.'],'publication_authorized':False,'activation_authorized':False}
