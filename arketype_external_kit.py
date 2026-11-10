"""Read-only, explicitly selected Authoring Kit draft.4 provenance preflight.

Arketype continues to ship its original draft.3 Kit for historical template
reproducibility. A current draft.4 Kit can be used only with the caller's
separately supplied Framework source, whose pinned bytes are verified before
an opt-in empty workspace is generated. No graph is admitted or activated.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
KIT_VERSION = '4.0.0-draft.4'
FRAMEWORK_VERSION = '11.0.0-draft.4'
PIN_PROFILE = 'kristal-integration-framework-pin/v11.0-draft.4'


def _hash(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def preflight_external_v11_kit(kit: str | Path, framework: str | Path) -> dict:
    """Prove local pinned-source compatibility, not semantic/release validity.

    Refuses aliases, embedded vendors, obsolete drafts and modified Framework
    sources. Results refer to verified local bytes only (not GitHub or a TCK).
    """
    if not kit or not framework:
        raise ValueError('External Kit requires both --external-kit and --framework')
    selected = Path(kit).expanduser().resolve()
    script = selected if selected.name == 'kristal.py' else selected / 'tools' / 'kristal.py'
    if script.name != 'kristal.py' or script.parent.name != 'tools':
        raise ValueError('Expected Authoring Kit root or its tools/kristal.py')
    kit_root = script.parent.parent
    if kit_root.is_relative_to(ROOT):
        raise ValueError('External Kit must be separate from the Arketype repository')
    if not script.is_file():
        raise FileNotFoundError(f'Missing external Kit tool: {script}')
    version_file = kit_root / 'VERSION'
    pin_file = kit_root / 'contracts/v11-framework-pin.json'
    if not version_file.is_file() or not pin_file.is_file():
        raise ValueError('External Kit is incomplete (VERSION or Framework pin absent)')
    if version_file.read_text(encoding='utf-8-sig').strip() != KIT_VERSION:
        raise ValueError(f'Only explicitly tested Kit {KIT_VERSION} is supported')
    match = re.search(r'^KIT_VERSION\s*=\s*[\'\"]([^\'\"]+)[\'\"]',script.read_text(encoding='utf-8-sig'),re.M)
    if not match or match.group(1) != KIT_VERSION:
        raise ValueError('External Kit version disagrees with tools/kristal.py')
    pin = json.loads(pin_file.read_text(encoding='utf-8'))
    if pin.get('profile') != PIN_PROFILE or pin.get('version') != FRAMEWORK_VERSION:
        raise ValueError('External Kit Framework profile/version is not the adopted draft.4 pin')
    files = pin.get('files')
    if not isinstance(files,dict) or len(files) < 13:
        raise ValueError('Missing pinned Framework source files')
    fw = Path(framework).expanduser().resolve()
    if not (fw/'VERSION').is_file() or (fw/'VERSION').read_text(encoding='utf-8').strip() != FRAMEWORK_VERSION:
        raise ValueError('Selected Framework has wrong version or is missing')
    for name, expected in files.items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name:
            raise ValueError('Unsafe Framework pin path')
        target = (fw/relative).resolve()
        if (not target.is_relative_to(fw) or not target.is_file() or
            not re.fullmatch('[a-f0-9]{64}',str(expected)) or _hash(target) != expected):
            raise ValueError('Framework source drift or invalid pin: '+name)
    return {'script':str(script),'kit_version':KIT_VERSION,'framework_version':FRAMEWORK_VERSION,
            'kit_source_sha256':_hash(script),'pin_sha256':_hash(pin_file),
            'framework_pin_checked':True,'semantic_state_authorized':False,
            'publish_or_activate_authorized':False}
