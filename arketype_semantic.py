"""Read-only Kristal v11 readiness and opt-in diK alpha.7 report adapter.

No network, no identity allocation, no claims of Wikidata equivalence, no
semantic migration, no silent publication.  Arketype remains design-only.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys


def semantic_status(path: Path) -> dict:
    root=path.expanduser().resolve()
    if not root.is_dir():
        raise ValueError('Workspace directory not found')
    workspace=root/'kristal.workspace.json'
    if not workspace.is_file():
        raise ValueError('Missing workspace descriptor')
    doc=json.loads(workspace.read_text(encoding='utf8'))
    if not isinstance(doc,dict):raise ValueError('Invalid workspace descriptor')
    profile=root/'.kristal/v11/authoring.json'
    readiness=root/'design/v11-semantic-readiness.json'
    flags={
        'workspace_exists':True,
        'v11_authoring_profile_present':profile.is_file(),
        'v11_readiness_plan_present':readiness.is_file(),
        'v11_strict_validation_performed':False,
    }
    info=None
    if profile.is_file():
        data=json.loads(profile.read_text(encoding='utf8'))
        if not isinstance(data,dict):raise ValueError('Invalid v11 profile')
        info={'semantic_profile':data.get('semantic_profile'),
              'registry':data.get('registry'),'graph':data.get('graph'),
              'crosswalk':data.get('crosswalk'),'catalog':data.get('catalog')}
    kit=root/'tools/kristal.py'
    version=None
    if kit.is_file():
        import re
        m=re.search(r'^KIT_VERSION\s*=\s*[\'\"]([^\'\"]+)',kit.read_text(encoding='utf8'),re.M)
        version=m.group(1) if m else 'unknown'
    return {'format':'arketype.semantic-readiness/1.0-non-normative',
            'mode':'metadata_only', 'state_ref':doc.get('state_ref'),
            'bundled_workspace_kit_version':version,
            'flags':flags,'active_v11_profile':info,
            'semantic_completeness':'unknown_not_evaluated',
            'wikidata_mapping_quality':'not_evaluated',
            'publication_authorized':False,
            'next_step':('Run workspace tools/kristal.py check-v11, then check and build-v9' if profile.is_file()
                         else 'Register valid identity/graph/crosswalk/catalog first; then enable-v11; do not mint fake QIDs.')}


def run_dik_coverage(dik_root: Path, project_path: Path, locales: str|None = None) -> str:
    """Execute local diK from explicitly selected checkout in coverage READ mode."""
    d=dik_root.expanduser().resolve(strict=True)
    if not (d/'src/dik/__main__.py').is_file():
        raise ValueError('Select a diK source root containing src/dik/__main__.py')
    p=project_path.expanduser().resolve(strict=True)
    if not p.is_file():raise ValueError('diK project manifest missing')
    args=[sys.executable,'-m','dik','coverage','report','--project',str(p)]
    if locales:args+=['--locales',locales]
    env=os.environ.copy()
    env['PYTHONPATH']=str(d/'src')  # execute only explicitly selected local source
    finished=subprocess.run(args,cwd=d,env=env,text=True,capture_output=True,
                            encoding='utf8',errors='replace',timeout=120,check=False)
    if finished.returncode:
        raise RuntimeError('Local diK coverage rejected inputs: '+finished.stderr[-1500:])
    parsed=json.loads(finished.stdout)
    if parsed.get('artifact_type')!='kristal_dik_coverage_report':
        raise ValueError('External diK response is not a v11 coverage report')
    return json.dumps(parsed,ensure_ascii=False,indent=2)+'\n'
