"""Allowlisted operations for the desktop Arketype Developer Ops console.

No shell, network, remote publication, activation, or arbitrary Python execution.
Both parsing and execution are independently usable and testable without Tkinter.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

HELP = """Arketype Developer Ops — allowed commands

  help                 Show available commands
  status               Summarize the local repository
  list                 List all archetypes
  search WORDS         Search archetypes
  show SLUG            Inspect an archetype (stable slug)
  profiles             List use-case profiles
  profile SLUG         Inspect a use-case profile
  recipes              List composition recipes
  recipe ID            Inspect a composition recipe
  validate             Check catalogue, templates and links
  validate --check-kit Also run the bundled Authoring Kit checks
  test                 Run the Python unittest suite
  inventory            Verify local file-inventory hashes
  build-html           Regenerate the local visual HTML catalogue
  open-catalogue       Open the offline HTML catalogue in your browser
  clear                Clear this console's output

Use the Create Kristal page for workspace creation. No shell commands,
remote publishing, activation, or arbitrary execution are supported.
"""


class OperationError(ValueError):
    """A console command was rejected without execution."""


@dataclass(frozen=True)
class Operation:
    name: str
    kind: str  # local | cli | tests | open | clear
    argv: tuple[str, ...] = ()
    changes_files: bool = False


def parse_operation(command: str) -> Operation:
    try:
        tokens = shlex.split(command.strip())
    except ValueError as exc:
        raise OperationError(f'Invalid command syntax: {exc}') from exc
    if not tokens:
        raise OperationError('Enter a command or type help.')
    action, *args = tokens
    no_args = {'help', 'status', 'list', 'profiles', 'recipes', 'test',
               'inventory', 'build-html', 'open-catalogue', 'clear'}
    if action in no_args:
        if args:
            raise OperationError(f'{action} takes no arguments.')
        if action in {'help', 'status', 'inventory'}:
            return Operation(action, 'local')
        if action in {'open-catalogue', 'clear'}:
            return Operation(action, 'open' if action == 'open-catalogue' else 'clear')
        if action == 'test':
            return Operation(action, 'tests')
        return Operation(action, 'cli', (action,), changes_files=action == 'build-html')
    if action == 'validate':
        if args not in ([], ['--check-kit']):
            raise OperationError('Use validate or validate --check-kit.')
        return Operation(action, 'cli', ('validate', *args))
    if action in {'show', 'profile', 'recipe'}:
        if len(args) != 1 or args[0].startswith('-'):
            raise OperationError(f'Use {action} SLUG (exactly one identifier).')
        return Operation(action, 'cli', (action, args[0]))
    if action == 'search':
        if not args or any(a.startswith('--') for a in args):
            raise OperationError('Use search WORDS (one or more search terms).')
        return Operation(action, 'cli', ('search', ' '.join(args)))
    raise OperationError(f'Unsupported operation: {action}. Type help for the allowlist.')


def inventory_report(root: Path = ROOT) -> str:
    doc = json.loads((root / 'INVENTAIRE.json').read_text(encoding='utf-8'))
    errors = []
    entries = doc['files']
    for entry in entries:
        path = Path(entry['path'])
        if path.is_absolute() or '..' in path.parts:
            errors.append(f'Unsafe path: {entry["path"]}')
            continue
        file = root / path
        if not file.is_file():
            errors.append(f'Missing: {entry["path"]}')
            continue
        content = file.read_bytes()
        if hashlib.sha256(content).hexdigest() != entry['sha256'] or len(content) != entry['size_bytes']:
            errors.append(f'Changed: {entry["path"]}')
    header = f"Inventory: {len(entries)} tracked files | {len(errors)} discrepancies"
    return header + ("\n" + '\n'.join(errors[:40]) if errors else '\nAll tracked files match.')


def run_operation(op: Operation, root: Path = ROOT, timeout: int = 240) -> tuple[int, str]:
    """Return (exit_code, text) with command arguments kept separate (shell=False)."""
    if op.kind == 'local':
        if op.name == 'help':
            return 0, HELP
        if op.name == 'inventory':
            result = inventory_report(root)
            return (0 if result.endswith('All tracked files match.') else 1), result
        if op.name == 'status':
            from arketype import catalogue, assemblies, use_case_profiles
            return 0, ('Arketype local repository\n'
                       f'Root: {root}\n'
                       f'Archetypes: {len(catalogue())}\n'
                       f'Composition recipes: {len(assemblies())}\n'
                       f'Use-case profiles: {len(use_case_profiles())}\n'
                       'Mode: local design library; no publication or activation.\n')
        raise OperationError(f'Unknown local operation: {op.name}')
    if op.kind in {'clear', 'open'}:
        raise OperationError('This operation must be performed by the graphical interface.')
    if op.kind == 'cli':
        args = [sys.executable, str(root / 'arketype.py'), *op.argv]
    elif op.kind == 'tests':
        args = [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v']
    else:
        raise OperationError('Unsupported operation kind.')
    try:
        done = subprocess.run(args, cwd=root, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=timeout,
                              shell=False)
        text = (done.stdout + (('\n' if done.stdout else '') + done.stderr if done.stderr else '')).strip()
        return done.returncode, text or '(No output.)'
    except subprocess.TimeoutExpired:
        return 124, f'Operation timed out after {timeout} seconds.'
