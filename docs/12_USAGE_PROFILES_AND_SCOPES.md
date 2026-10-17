# Design semantics — usage profiles, scope and coverage (v1.4)

Arketype remains a **non-normative design library**. Its archetypes answer *how a Kristal is structured*; its use-case profiles answer *what its intended work is*, with domain, integrations and governance documented independently. These are not verified runtime capabilities.

## Five orthogonal dimensions

| Dimension | Source | Meaning |
|---|---|---|
| Structure | `catalogue.json`, `archetypes/` | Primary and supporting graph, timeline, process, casefile, etc. |
| Usage | `inventaires/profils-usage.json` | Activity family, intended input/output and expected capabilities |
| Domain | `inventaires/taxonomie-usages.json` | Education, math, culture, medical, public safety, etc. |
| Integration | `integration_targets` | Required application boundary or external adapters (Moodle, MediKristal, Formulator...) |
| Authority / data | `boundaries` and `coverage_checks` | Access, authorization, source and temporal validity, uncertainty |

**No inheritance of authority:** alignment to a profile is not a publication license, access grant, clinical validity, proof verification, administrative ruling or guarantee that content exists.

## Recognition

`python arketype.py recognize --path ... [--focus subfolder]` inspects **only file names and small workspace/origin metadata**. It does not inspect large canonical assertions, medical records, student histories, confidential documents or proofs. It provides traceable candidate signals, not a semantic audit. An archive with multiple projects can yield mixed signals; use `--focus`.

## Scope guidance

`python arketype.py scope-guide --profile PROFILE [--path ... --focus ...] [--output NEW_FILE]` produces `arketype.scope-guidance/1.0` with structure, target usage, domain, integration targets, inclusions, exclusions and `coverage_questions`, all initially `not_evaluated`. An output file is not overwritten. A new neutral instance created with `--profile` receives `design/scope-guidance.json` and a noncanonical `arketype.instance.json` origin reference. Its `state_scope` remains under the owning Authoring Kit/workspace process.

## Case families from the supplied snapshots

| Family | Representative supplied artifact | Structural candidates | Limit |
| --- | --- | --- | --- |
| Campus federation | UCKK v9 | Federation / Learning Path | LMS course publication is external |
| Mythologies | Tradition collection | Compilation / Interpretations | Cultural attribution and protected knowledge |
| Social institutions | Ekole human organizations | Multiplex | Contextuality and authority of communities |
| Long math proofs | Grand Challenges / Formulator | Proof landmarks / Research memory | Waypoint is not proof |
| Personal follow-up | Arketype dossier examples | Casefile / Event ledger | Access/retention and legal basis for real dossiers |
| Diagnostic | VehiculeDiag | Causal diagnosis / Multiplex | Vehicle-specific OEM information excluded unless sourced |
| Procedures | PoliceOps / hospital concepts | Protocol / Events | Authorization is external |
| Medical orchestration | MediKristal software | Hybrid / semantic references | Standalone app is not one Kristal |
| School-system mapping | ScolQc | Multiplex / Reference | Actual school admission decisions external |

The inventory `inventaires/cas-reels-usage.json` names sources and paths examined for modeling decisions; it does not import those sources or claim exhaustive verification.

## Extension rules

A new special-purpose use does **not** automatically require a new structural ARK type. Add a profile first, with primary/supporting references, a design-only assembly, expected evidence and status `not_evaluated`. Only add a new structural archetype if the existing nineteen cannot express its native architecture.
