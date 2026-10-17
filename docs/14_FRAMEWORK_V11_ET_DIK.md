# Framework v11, KQ/KP et diK — Arketype 1.6.0

## Design is not identity

Arketype's **19 structural archetypes**, diagrams, composition plans, scenario labels and neutral fixtures are *design descriptions*, not canonical semantic graphs. Therefore their plain-language labels are legitimate **outside** the graph canon. An actual canonical Framework v11 graph, by contrast, uses opaque and namespaced KQ entity IDs, KP properties, KA assertions and KS sources, with words in separate dictionary layers. No language strings should be used as predicate IDs.

Wikidata `Q`/`P` IDs are **external**, not synonyms for Kristal `KQ`/`KP`. A reviewed and provenance-backed crosswalk supplies alignment. diK serves lexical dictionaries and reports per-language direct / fallback / missing / conflicting labels, not identity authority.

## Creation workflows

### Legacy (fully preserved)

`python arketype.py create --type referentiel-semantique --slug demo --title Demo --parent .` still uses the legacy bundled Kit 3.2.4 with v9 semantic state and v10 hosted-network targets. The 19 source templates stay unchanged. No automatic conversion or reuse of another instance's `state_ref`.

### v11-ready (opt-in)

`python arketype.py create --type referentiel-semantique --slug demo-v11 --title 'Demo v11' --parent . --authoring v11`

This uses Kit 4.0.0-draft.3 and creates `design/v11-semantic-readiness.json`. The workspace is intentionally empty: `canon/state.index.json` has no admitted domain Logical Artifacts. **Strict v11 is NOT enabled.** Only after allocating genuinely validated namespaced identity records (KQ/KP/KA/KS), creating a graph, catalog and reviewed crosswalk and registering all four v9 logical artifacts can the owner invoke `tools/kristal.py enable-v11 …`, `check-v11`, `check`, `build-v9`.

The readiness file is **noncanonical** and should not be registered as semantic truth. No automatic QID minting, word-to-ID conversion or translation is offered here. The authoring process must preserve the state-ref isolation of each newly created workspace.

## Read-only inspections

`python arketype.py semantic-status --path /path/to/workspace` reads only local metadata; an existing profile means **configuration exists**, not certified semantic completeness.

`python arketype.py dik-coverage --dik-root /trusted/local/diK-v1.0.0-alpha.7 --project /project/dik.project.json --locales fr,en,fr-CA` executes that **explicitly chosen local diK package** in report mode, without changing Arketype or the project. It requires the diK checkout, the project and its files to be present locally. It returns the actual `kristal_dik_coverage_report` and never constructs missing labels.

`compat --framework PATH --dik PATH` in Developer Ops only inspects the local source metadata; this is not a cross-repository certification or a remote GitHub status check.

## How to handle historical Kristals with words

Inventoried text identifiers are **migration candidates**, not automatic KQ mappings. Submit ambiguities to diK for interpretation and reviewed plans; only an authorized Authoring Kit migration pipeline may create a new canonical graph while preserving historical sources, v9 commitments, literal text and provenance. No global string replacement. A legacy corpus with unresolved identity paths does **not** have a meaningful '100% KQ/KP coverage' figure.

## What v1.5 does NOT do

- Does not automatically migrate the existing nineteen templates or any archived Kristal.
- Does not bundle a complete Wikidata mirror or scrape/download entities.
- Does not implement a local dictionary server or replace diK's manager.
- Does not claim the Draft.3 Framework is final or that v11 tools are independently certified.
- Does not publish, activate, synchronize, or grant operational/data access.

**References:** `docs/ECOSYSTEM_ALIGNMENT.md`, `catalogue.json` and the bundled read-only Kit4 tools. Source archives received: `Kristal-Framework-v11.0.0-draft.4`, `diK-v1.0.0-alpha.7`, `Kristal-Authoring-Kit-4.0.0-draft.3` (from earlier conversation). For canonical contracts use Framework schemas/TCK, not Arketype design diagrams.
