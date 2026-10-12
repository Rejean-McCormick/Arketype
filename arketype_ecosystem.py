"""Read-only interoperability observations for Arketype's v10 design ecosystem.

The module never runs external programs and never contacts an origin or publishes.
A matching version/hash is evidence of local files only, NOT Framework conformance,
independent qualification, authority, synchronization, or activation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parent


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def _json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object.')
    return value


def _result(status: str, details: str, **extra: Any) -> dict:
    return {'status': status, 'details': details, **extra}


def _tool_file(path: str | Path | None) -> Path | None:
    if not path:
        return None
    candidate = Path(path).expanduser()
    return candidate / 'tools' / 'kristal.py' if candidate.is_dir() else candidate


def inspect_kit(root: Path = ROOT, selected: str | Path | None = None) -> dict:
    """Compare an explicitly provided Kit file or folder with the bundled copy."""
    own = root / 'outils' / 'kristal.py'
    try:
        bundled_hash = _sha(own)
        version_match = re.search(r'^KIT_VERSION\s*=\s*[\'"]([^\'"]+)', own.read_text(encoding='utf-8'), re.M)
        bundled_version = version_match.group(1) if version_match else 'unknown'
    except (OSError, UnicodeError) as exc:
        return _result('error', f'Bundled Kit unavailable: {exc}')
    record = {'bundled_version': bundled_version, 'bundled_sha256': bundled_hash}
    if not selected:
        return _result('local_reference', 'Bundled Authoring Kit inspected. No external Kit path supplied; cross-repository equivalence not checked.', **record)
    candidate = _tool_file(selected)
    try:
        if candidate is None or not candidate.is_file():
            return _result('not_found', 'The selected Kit path does not contain tools/kristal.py or a readable file.', **record)
        data = candidate.read_text(encoding='utf-8')
        match = re.search(r'^KIT_VERSION\s*=\s*[\'"]([^\'"]+)', data, re.M)
        version = match.group(1) if match else 'unknown'
        digest = _sha(candidate)
        status = 'identical_bytes' if digest == bundled_hash else 'review_required'
        return _result(status, 'The external Kit is byte-identical to the bundled copy.' if digest == bundled_hash else 'External Kit differs; review compatibility before replacing anything.', external_version=version, external_sha256=digest, **record)
    except (OSError, UnicodeError) as exc:
        return _result('error', f'Unable to inspect selected Kit: {exc}', **record)


def inspect_framework(root: Path, selected: str | Path | None = None) -> dict:
    declared = _json(root / 'catalogue.json')['framework_reference']
    if not selected:
        return _result('not_configured', 'Framework version is a design reference only; choose a local Framework checkout to compare its files.', expected_version=declared)
    location = Path(selected).expanduser()
    try:
        release = _json(location / 'contracts' / 'release.json')
        contract_set = _json(location / 'contracts' / 'contract-set.json')
        lock = _json(location / 'contracts' / 'v10-compatibility-lock.json')
        version = release.get('version')
        agrees = version == declared == contract_set.get('version')
        status = 'declared_version_matches' if agrees else 'review_required'
        return _result(status, ('The release and contract-set declare the expected version. Full TCK and normative lock validation were NOT run.' if agrees else 'Framework release, contract-set, or Arketype design baseline differs.'), expected_version=declared, observed_version=version, release_status=release.get('status'), contract_set_sha256=_sha(location / 'contracts' / 'contract-set.json'), compatibility_lock_release=lock.get('release'))
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
        return _result('not_available', f'No readable Framework release, contract-set and v10 compatibility lock at this path: {exc}', expected_version=declared)


def inspect_templates(root: Path = ROOT) -> dict:
    try:
        records = _json(root / 'catalogue.json')['archetypes']
        identities: list[str] = []
        errors = []
        for item in records:
            workspace = root / 'modeles' / item['slug']
            ws = _json(workspace / 'kristal.workspace.json')
            index = _json(workspace / 'canon' / 'state.index.json')
            identities.append(ws.get('state_ref', ''))
            if ws.get('status') != 'stub' or index.get('canonical_artifacts') != [] or not ws.get('state_ref'):
                errors.append(item['slug'] + ': not a valid empty stub')
            if ws.get('target', {}).get('hosted_network_baseline') != 'kristal.hosting/10.0':
                errors.append(item['slug'] + ': v10 target not declared')
        if len(set(identities)) != len(identities):
            errors.append('Duplicate state_ref in the starter templates')
        return _result('templates_consistent' if not errors else 'review_required', 'Inventory and blank-state structure checked (not a full Authoring Kit validation).', count=len(records), unique_state_refs=len(set(identities)), problems=errors)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return _result('error', f'Could not inspect the template metadata: {exc}')


def inspect_workspace(selected: str | Path | None = None) -> dict:
    if not selected:
        return _result('not_configured', 'No local workspace selected. Its canonical content is never loaded by this diagnostic.')
    directory = Path(selected).expanduser()
    try:
        workspace = _json(directory / 'kristal.workspace.json')
        index_path = directory / 'canon' / 'state.index.json'
        index = _json(index_path) if index_path.is_file() else None
        return _result('metadata_only', 'Workspace metadata inspected, without verifying commitments, domain facts, AI readiness, or any hosted state.', state_ref=workspace.get('state_ref'), workspace_format=workspace.get('format'), hosted_network_baseline=workspace.get('target', {}).get('hosted_network_baseline'), portable_ai_enabled=workspace.get('portable_ai', {}).get('enabled'), registered_artifact_count=(len(index.get('canonical_artifacts', [])) if index else None), ai_entrypoint_present=(directory / 'AI_START_HERE.md').is_file())
    except (OSError, ValueError, TypeError) as exc:
        return _result('not_available', f'Workspace descriptor unavailable: {exc}')


def inspect_manager(selected: str | Path | None = None) -> dict:
    if not selected:
        return _result('not_configured', 'No Manager checkout selected; no claim about its runtime or registry.')
    location = Path(selected).expanduser()
    version = location / 'VERSION'
    package = location / 'kristal_manager' / 'core.py'
    return _result('runtime_source_present' if package.is_file() else 'source_incomplete', 'Source presence check only; no Manager import, sync, qualification or registry exposure executed.', version=(version.read_text(encoding='utf-8').strip() if version.is_file() else None), core_module_present=package.is_file())


def inspect_bootstrap(selected: str | Path | None = None) -> dict:
    if not selected:
        return _result('not_configured', 'No Bootstrap checkout selected; no publishing workflow was run.')
    location = Path(selected).expanduser()
    version = location / 'VERSION'
    engine = location / 'kristal_github_bootstrap' / 'core.py'
    return _result('source_present' if engine.is_file() else 'source_incomplete', 'Source presence check only; doctor, plan, apply and publishing were NOT executed.', version=(version.read_text(encoding='utf-8').strip() if version.is_file() else None), engine_present=engine.is_file())


def inspect_ecosystem(*, root: Path = ROOT, framework: str | Path | None = None,
                      kit: str | Path | None = None, workspace: str | Path | None = None,
                      manager: str | Path | None = None, bootstrap: str | Path | None = None) -> dict:
    """Local source observations, deliberately not a qualification certificate."""
    return {'format': 'arketype.ecosystem-inspection/1.0-non-normative',
            'mode': 'read_only', 'is_qualification': False, 'does_not_publish': True,
            'framework': inspect_framework(root, framework),
            'authoring_kit': inspect_kit(root, kit),
            'templates': inspect_templates(root),
            'workspace': inspect_workspace(workspace),
            'manager': inspect_manager(manager),
            'bootstrap': inspect_bootstrap(bootstrap),
            'limits': ['No remote GitHub checks', 'No C1/C2/C3 verification',
                       'No canonical artifact parsing', 'No publishing, sync or activation',
                       'The Framework baseline is draft; matching versions are not conformance proof']}


def format_ecosystem_report(report: dict) -> str:
    lines = ['ARKETYPE — ECOSYSTEM COMPATIBILITY (READ ONLY)',
             'Local file observations, NOT a qualification or publication receipt.', '']
    for section in ['framework', 'authoring_kit', 'templates', 'workspace', 'manager', 'bootstrap']:
        data = report[section]
        lines += [section.replace('_', ' ').upper() + f' [{data["status"]}]',
                  '  ' + data['details']]
        for key, value in data.items():
            if key not in ('status', 'details'):
                lines.append(f'  {key}: {value}')
        lines.append('')
    lines += ['No network, publication, sync, or activation action performed.']
    return '\n'.join(lines)
