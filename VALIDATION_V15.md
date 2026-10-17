# Arketype v1.5.0 — local validation and scope

**Release state:** additive local update from user snapshot `znapshot_arketype_10161402.zip`. Non-normative design software. No GitHub push or semantic domain certification.

## Source and identity preservation

- All **95** `modeles/*/canon/*` and `modeles/*/kristal.workspace.json` source files in the original ZIP were compared byte-for-byte and **none were modified**.
- The 19 historical templates retain Authoring Kit **3.2.4** and their original `state_ref`, stub status and empty domain canon. They remain in the default `legacy` creation mode.
- Missing **derived** v9 build receipts were generated from those empty models (19 neutral receipts). No domain assertions were added.
- A misplaced `design/fiche-deposition-vierge.json` under `modeles/dossier-suivi` was removed to satisfy the existing declared casefile boundary. The intended deposition example remains in `modeles/deposition-temoignage`.
- The original logo SVG/PNG was absent from the uploaded snapshot. Minimal `assets/logo-k.*` **fallbacks** have been generated to repair HTML/GUI links; they are NOT the original supplied brand artwork.

## v11 and diK features

- Bundled Authoring Kit **4.0.0-draft.1**, `tools/kristal.py`, `kristal_v11_core.py` and Kit templates, verified by SHA-256 pins (11 source files); **opt-in only** via `create --authoring v11`.
- New workspace has `design/v11-semantic-readiness.json`, an **empty** canon, separate new `state_ref` and **strict v11 disabled**. Arketype neither allocates KQ/KP/KA/KS IDs nor invents Wikidata Q/P IDs.
- `semantic-status` reads only workspace metadata; presence of a profile is NOT strict validation.
- `dik-coverage` executes **only** an explicitly selected local diK source path and reads a `dik.project.json` manifest; does not download sources or modify dictionaries/graph.
- Ecosystem inspections are metadata-only; Framework/Kit source validation and runtime qualification are separate processes.

## Evidence of local tests

- `python -m unittest discover -s tests -q`: **71 tests passed** with user-supplied diK and Framework checkouts exposed via the two `ARKETYPE_TEST_*` environment variables. Without checkouts, cross-repo tests skip instead of failing.
- `python arketype.py validate --check-kit`: **PASS**, all 19 neutral models, 19 archetypes, 23 recipes, 21 profiles and 40 situated diagrams.
- Framework v11 draft.3 reference `tools/v11/validate_v11.py`: **PASS** on its local fixtures. This is not full normative certification of Arketype.
- Kit 4's supplied v11 demo workspace `tools/kristal.py check-v11`: **PASS** (separate external reference).
- `python arketype.py dik-coverage` run with the user-supplied diK v0.1.0 sample project: **PASS**, returns typed `kristal_dik_coverage_report`.
- `INVENTAIRE.json` is regenerated from the shipped sources and is locally SHA-256-verified.

## Not covered / remaining work

- No migration of existing populated historical Kristals, no bulk Wikidata download or allocation of production identities.
- No `enable-v11` in a newly created *empty* workspace: activation must happen only after real graph/registry/crosswalk/catalog construction and v9 artifact registration.
- No live diK service, external GitHub or hosted activation tests, no native Windows desktop GUI end-to-end qualification, and no verified original logo assets.
- The current Framework and Kit remain **draft** versions; independent cross-repo TCK qualification is still needed for a production milestone.
