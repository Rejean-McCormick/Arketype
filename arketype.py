#!/usr/bin/env python3
"""Arketype — catalogue et instanciation locale.

Metadonnées Arketype = documentation non normative ; création via Authoring Kit fourni.
Ce programme ne publie, ne synchronise ni n'active jamais un Kristal.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / 'catalogue.json'
VALID_SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError(f'Le document doit être un objet JSON : {path}')
    return value


def catalogue() -> list[dict]:
    index = read_json(INDEX)
    results = []
    for entry in index['archetypes']:
        rel = entry['file']
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise ValueError(f'Chemin interdit dans le catalogue : {rel}')
        detail = read_json(ROOT / rel)
        results.append(detail)
    return results


def archetype(slug: str) -> dict:
    match = next((item for item in catalogue() if item['slug'] == slug), None)
    if match is None:
        raise ValueError(f'Archétype inconnu : {slug}. Utiliser `python arketype.py list`.')
    return match


def assemblies() -> list[dict]:
    return [read_json(p) for p in sorted((ROOT / 'assemblages').glob('*.json'))]


def assembly(key: str) -> dict:
    match = next((r for r in assemblies() if r['id'] == key), None)
    if match is None:
        raise ValueError(f'Assemblage inconnu : {key}. Utiliser `python arketype.py recipes`.')
    return match


def normalized(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', str(s)).casefold() if not unicodedata.combining(c))


def search(term: str, family: str = '') -> list[dict]:
    term = normalized(term)
    found = []
    for a in catalogue():
        haystack = ' '.join(str(x) for x in [a['name'],a['slug'],a['description'],a['reference_use_case'],a['integrity_rule'],*a['primitive_candidates'],*a['structural_traits']])
        if (not term or term in normalized(haystack)) and (not family or normalized(a['family']) == normalized(family)):
            found.append(a)
    return found


def render_archetype(a: dict) -> str:
    return '\n'.join([
        f"{a['id']} — {a['name']}",
        f"Famille : {a['family']} | Profil du Local Kit : {a['kit_profile']}",
        f"Intention : {a['description']}",
        f"Primitives candidates : {', '.join(a['primitive_candidates'])}",
        f"Invariance à préserver : {a['integrity_rule']}",
        f"Anti-modèle : {a['antipattern']}",
        f"Question de conception : {a['design_question']}",
        f"Exemple analogique : {a['reference_use_case']}",
        f"Modèle neutre : {a['template_path']}",
        'État : candidat, hors norme, sans assertions métier.'
    ])


def plan_for(primary: str, recipe: str | None = None, additions: list[str] | None = None) -> dict:
    archetype(primary)
    components = []
    guidance = 'Définir les frontières, contrats, références et pertes éventuelles avant d’intégrer.'
    if recipe:
        design = assembly(recipe)
        if design['primary_archetype'] != primary:
            raise ValueError('L’archétype principal ne correspond pas à celui de l’assemblage demandé.')
        components = [dict(c) for c in design['components']]
        guidance = design['guidance']
    for slug in additions or []:
        archetype(slug)
        if slug == primary:
            raise ValueError('Un archétype ne peut pas être ajouté à lui-même.')
        if any(c['archetype'] == slug for c in components):
            continue
        components.append({'archetype':slug, 'relation':'a_decider',
                           'design_note':'Déterminer la frontière et l’ownership avant tout canon.',
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
           dry_run: bool = False) -> Path | dict:
    """Instancie en staging, vérifie avec Local Kit, puis publie dans le dossier local final.

    `publish` ici est *interdit* au sens du Framework : le renommage du dossier
    n'est qu'une opération de filesystem local, pas une publication Kristal.
    """
    a = archetype(type_slug)
    if not VALID_SLUG.fullmatch(slug or '') or len(slug) > 80:
        raise ValueError('Slug attendu : minuscules ASCII, chiffres et tirets (1–80 caractères).')
    if not title or not title.strip() or len(title.strip()) > 250:
        raise ValueError('Titre attendu : 1–250 caractères non blancs.')
    if '\x00' in str(parent):
        raise ValueError('Chemin invalide.')
    parent = Path(parent).expanduser().resolve(strict=True)
    if not parent.is_dir():
        raise ValueError(f'Le dossier parent n’est pas un répertoire : {parent}')
    destination = parent / slug
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Le dossier cible existe déjà : {destination}')
    plan = plan_for(type_slug, recipe, additions)
    if dry_run:
        return {'destination': str(destination), 'archetype': a['id'], 'title':title.strip(),
                'plan':plan,'will_write':False}
    tool = ROOT / 'outils' / 'kristal.py'
    model = ROOT / a['template_path']
    if not tool.is_file() or not model.is_dir():
        raise FileNotFoundError('Local Kit ou modèle de départ introuvable dans cette archive Arketype.')
    with tempfile.TemporaryDirectory(prefix='.arketype-staging-', dir=str(parent)) as td:
        working = Path(td) / 'workspace'
        def run_kit(args: list[str]) -> None:
            p = subprocess.run([sys.executable, str(tool if args[0] == 'init' else working/'tools'/'kristal.py'),
                 *args], capture_output=True,text=True,encoding='utf-8',errors='replace', timeout=120)
            if p.returncode:
                raise RuntimeError('Authoring Kit ('+args[0]+') :\n'+p.stdout+'\n'+p.stderr)
        run_kit(['init',str(working),'--slug',slug,'--title',title.strip(),'--profile',a['kit_profile']])
        ws_file=working/'kristal.workspace.json'
        ws=read_json(ws_file)
        source_ws=read_json(model/'kristal.workspace.json')
        ws['native_model']['kind']=a['native_kind_candidate']
        ws['native_model']['description']='Forme candidate Arketype; connaissance métier et Logical Contract encore à définir.'
        ws['semantic_ownership']=source_ws['semantic_ownership']
        ws_file.write_text(json.dumps(ws,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        (working/'design').mkdir(exist_ok=True)
        for candidate in ('structure-candidate.json', 'fiche-deposition-vierge.json'):
            source = model / 'design' / candidate
            if source.is_file():
                shutil.copyfile(source, working / 'design' / candidate)
        for filename in ('00_INTENT_AND_SCOPE.md','01_SEMANTIC_BOUNDARY.md',
              '02_NATIVE_MODEL.md','03_EPISTEMIC_MODEL.md','ARKETYPE.md'):
            shutil.copyfile(model/'docs'/filename,working/'docs'/filename)
        with (working/'docs'/'ARKETYPE.md').open('a',encoding='utf8') as f:
            f.write(f'\n## Instance locale\n\n- Titre : **{title.strip()}**\n- Slug : `{slug}`\n- État initial : `{ws["state_ref"]}`\n- Contrats et assertions : **à concevoir**.\n')
        (working/'design'/'composition-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n','utf8')
        (working/'arketype.instance.json').write_text(json.dumps({
             'format':'arketype.instance-origin/1.0-non-normatif',
             'library_version':'1.1.0','primary_archetype':type_slug,
             'assembly_recipe':recipe,'additional_archetypes':[p['archetype'] for p in plan['components']],
             'state_ref_at_initialization':ws['state_ref'],
             'authoring_kit_reference':'3.2.4',
             'status':'stub_no_domain_assertions','published':False,
             'authorized_for_publication':False
             },ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        run_kit(['check',str(working)])
        index=read_json(working/'canon'/'state.index.json')
        if index.get('artifacts',[]) or index.get('canonical_artifacts',[]):
            raise ValueError('Le workspace n’est pas vide : instanciation refusée.')
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f'La destination a été créée entretemps : {destination}')
        working.rename(destination)
    return destination


def validate(check_kit: bool = False) -> dict:
    errors=[]
    index=read_json(INDEX)
    if index.get('format')!='arketype.catalog/1.0-non-normatif':
        errors.append('Mauvais format catalogue.')
    types=catalogue()
    if len(types) != len(index['archetypes']): errors.append('Nombre de fiches incohérent.')
    slugs=set();ids=set()
    for i,a in zip(index['archetypes'],types):
        slug=a.get('slug','')
        if slug in slugs: errors.append(f'Slug répété : {slug}')
        slugs.add(slug)
        if a.get('id') in ids: errors.append(f'ID répété : {a.get("id")}')
        ids.add(a.get('id'))
        if (slug,i['id']) != (i['slug'],a.get('id')):
            errors.append(f'Index désaligné : {slug}')
        if not VALID_SLUG.fullmatch(slug): errors.append(f'Slug invalide : {slug}')
        if a.get('family') not in ('Savoir','Composition','Structures','Processus','Sources'):
            errors.append(f'{slug}: famille inconnue')
        for required in ['name','description','family','kit_profile','native_kind_candidate','integrity_rule','template_path','antipattern','design_question']:
            if not a.get(required): errors.append(f'{slug}: champ absent {required}')
        if a.get('kind')!='open_archetype_not_standard' or a.get('canonical_claims_in_template') is not False:
            errors.append(f'{slug}: archétype prétend être une norme ou un corpus.')
        p=ROOT / a['template_path']
        if not p.is_dir():errors.append(f'{slug}: modèle absent');continue
        if p.resolve().parent != (ROOT/'modeles').resolve():errors.append(f'{slug}: chemin modèle interdit')
        try:
            ws=read_json(p/'kristal.workspace.json')
            ca=read_json(p/'canon'/'state.index.json')
            shape=read_json(p/'design'/'structure-candidate.json')
            template_meta=read_json(p/'arketype.template.json')
            if ws['profile'] != a['kit_profile']: errors.append(f'{slug}: profil incohérent')
            if ws['native_model']['kind'] != a['native_kind_candidate']: errors.append(f'{slug}: forme incohérente')
            if ws.get('status') != 'stub':errors.append(f'{slug}: modèle non neutralisé')
            if ca.get('canonical_artifacts',[]) or ca.get('artifacts',[]):errors.append(f'{slug}: canon non vide')
            if shape.get('id_type') != a['id']:errors.append(f'{slug}: design incohérent')
            if template_meta.get('archetype_id')!=a['id']:errors.append(f'{slug}: origine incohérente')
            if template_meta.get('format')!='arketype.template/1.0-non-normatif':
                errors.append(f'{slug}: format modèle inconnu')
            if slug == 'deposition-temoignage':
                dep = read_json(p / 'design' / 'fiche-deposition-vierge.json')
                if dep.get('statut') != 'FORMULAIRE_VIERGE_HORS_CANON_NE_PAS_REMPLIR_DANS_LE_REPO':
                    errors.append('deposition-temoignage: formulaire non neutre')
                if dep.get('evaluation_distincte', {}).get('statut_factuel') != 'non_evalue':
                    errors.append('deposition-temoignage: conclusions factuelles préétablies')
            if check_kit:
                p_check=subprocess.run([sys.executable,str(p/'tools'/'kristal.py'),'check',str(p)],
                         capture_output=True,text=True,timeout=120)
                if p_check.returncode: errors.append(f'{slug}: échec check Local Kit: {p_check.stderr[-300:]}')
        except (OSError,ValueError,KeyError) as exc:
            errors.append(f'{slug}: {exc}')
    recipes=assemblies();recipes_id=set()
    for r in recipes:
        if r['id'] in recipes_id:errors.append('Assemblage répété : '+r['id'])
        recipes_id.add(r['id'])
        if r.get('primary_archetype') not in slugs:errors.append(r['id']+': principal inconnu')
        if r.get('composition_status')!='design_only':errors.append(r['id']+': assemblage prétend être canon')
        if r.get('publication_authorization') is not False:errors.append(r['id']+': autorisation indue')
        for c in r['components']:
            if c['archetype'] not in slugs:errors.append(r['id']+': composant inconnu '+c['archetype'])
            if c['archetype']==r['primary_archetype']:errors.append(r['id']+': auto-composition')
            if c.get('status')!='unresolved':errors.append(r['id']+': lien déclaré résolu sans preuve')
    return {'ok':not errors,'archetype_count':len(types),'recipe_count':len(recipes),
            'local_kit_checks':check_kit,'errors':errors}


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(prog='arketype.py',description='Arketype — bibliothèque d’archétypes Kristal, non normative.')
    commands=parser.add_subparsers(dest='command',required=True)
    ls=commands.add_parser('list',help='Lister les archétypes')
    ls.add_argument('--family',default='',help='Famille : Savoir, Composition, Structures, Processus, Sources')
    sh=commands.add_parser('show',help='Afficher la fiche complète');sh.add_argument('slug')
    se=commands.add_parser('search',help='Rechercher noms, usages et propriétés');se.add_argument('term')
    rec=commands.add_parser('recipes',help='Lister les assemblages documentés')
    rp=commands.add_parser('recipe',help='Afficher un assemblage');rp.add_argument('id')
    v=commands.add_parser('validate',help='Contrôler cohérence Arketype (lecture seule)');v.add_argument('--check-kit',action='store_true')
    for command in ('create','compose'):
        p=commands.add_parser(command,help='Instancier un Kristal local (ou préparer une composition)')
        p.add_argument('--type',help='Archétype principal; facultatif avec --recipe')
        p.add_argument('--recipe',help='Assemblage préétabli')
        p.add_argument('--with',dest='additions',action='append',default=[],metavar='ARCHETYPE',help='Archétype supplémentaire; répéter au besoin')
        p.add_argument('--slug',required=True,help='Identifiant du Kristal à créer')
        p.add_argument('--title',required=True,help='Titre de ce Kristal')
        p.add_argument('--parent',required=True,help='Dossier existant où créer le sous-dossier')
        p.add_argument('--dry-run',action='store_true',help='Prévisualiser sans écrire')
    args=parser.parse_args(argv)
    try:
        if args.command=='list':
            for a in catalogue():
                if not args.family or normalized(args.family)==normalized(a['family']):
                    print(f"{a['id']}  {a['slug']:28} {a['name']} [{a['family']}]")
        elif args.command=='show': print(render_archetype(archetype(args.slug)))
        elif args.command=='search':
            matches=search(args.term)
            for a in matches: print(f"{a['id']}  {a['slug']} — {a['name']}")
            if not matches: print('Aucun archétype trouvé.')
        elif args.command=='recipes':
            for r in assemblies():print(f"{r['id']:25} {r['title']} (principal : {r['primary_archetype']})")
        elif args.command=='recipe':
            print(json.dumps(assembly(args.id),ensure_ascii=False,indent=2))
        elif args.command=='validate':
            report=validate(args.check_kit)
            print(json.dumps(report,ensure_ascii=False,indent=2))
            return 0 if report['ok'] else 1
        elif args.command in ('create','compose'):
            typ=args.type or (assembly(args.recipe)['primary_archetype'] if args.recipe else None)
            if not typ:parser.error('Indiquer --type ou --recipe.')
            if args.command=='compose' and not (args.recipe or args.additions):
                parser.error('compose attend --recipe ou au moins un --with.')
            result=create(typ,args.slug,args.title,args.parent,args.recipe,args.additions,args.dry_run)
            if isinstance(result,dict):print(json.dumps(result,ensure_ascii=False,indent=2))
            else:print('Workspace Arketype neutralisé créé et contrôlé : '+str(result))
        return 0
    except (OSError,ValueError,RuntimeError,KeyError,subprocess.TimeoutExpired) as exc:
        print('ERREUR Arketype : '+str(exc),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(main())
