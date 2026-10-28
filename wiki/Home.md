# Arketype — Wiki

<img src="assets/logo-k.svg" alt="Official Kristal logo" width="220">

**Declared release: Arketype `1.6.0`** — a non-normative visual and structural design library for Kristal workspaces. Its optional ecosystem baseline is **Kristal Framework `11.0.0-draft.4`**, bundled **Authoring Kit `4.0.0-draft.3`** for new v11-ready workspaces, and a **separately supplied diK `1.0.0-alpha.7`** CLI. These are draft/alpha dependencies, **not** a claim of full cross-repository qualification.

Arketype answers: **Which structural archetype fits the knowledge you want to preserve?** It does not own the truth of domain facts, allocate semantic identifiers, approve Wikidata mappings, or publish Kristals.

## What ships

| Library component | Count | Meaning |
| --- | ---: | --- |
| Structural archetypes | **19** | Stable source slugs and IDs |
| Neutral historical workspace templates | **19** | Independent `state_ref` identities; legacy Kit 3.2.4 |
| Composition recipes | **23** | Proposals marked `design_only`, not canonical merges |
| Use-case profiles | **21** | Situated design and authority/data constraints |
| Situated visual diagrams | **40** | Illustrative projections, not native Kristal graphs |
| Visual patterns | **10** | Shared reader conventions |

Use `catalogue/index.html` for the offline visual catalogue, or `Lancer_Arketype.pyw` for the optional Windows desktop launcher. This Wiki includes the supplied original SVG (`assets/logo-k.svg`, matching the recorded SHA-256). The **uploaded code snapshot**, however, does not contain the application `assets/` files; their presence in a complete local checkout must be verified.

> **Snapshot verification (27 October 2026):** The uploaded code snapshot identifies itself as Arketype 1.6.0, but it does **not** include `assets/logo-k.svg`, `assets/logo-k-ui.png`, or the 19 `modeles/*/build/v9/build-receipt.json` files. It also still contains `modeles/dossier-suivi/design/fiche-deposition-vierge.json`. Re-running `python -m unittest discover -s tests -q` on this snapshot produced **78 tests: 67 passed, 6 failed, 3 errors, 2 skipped**. `python arketype.py validate --check-kit` did not pass. These results describe the **provided snapshot**, not necessarily an unfiltered local Git checkout. See [[Snapshot-Verification-2026-10-27]] for details.

## Get started

| Goal | Guide |
| --- | --- |
| Explore all forms and profiles | [[Archetype-Catalog]], [[Visual-Grammar]], [[Use-Case-Profiles]] |
| Create an independent empty workspace | [[Getting-Started]], [[CLI-Reference]] |
| Use optional v11 semantic authoring | [[Semantic-Authoring-v11]] |
| Understand diK's role and coverage | [[diK-and-Dictionaries]] |
| Review/pin a diK catalog in the Kit | [[diK-Catalog-Exchange-v11]] |
| Check versions and qualification boundaries | [[Ecosystem-Compatibility]], [[Validation-and-Testing]] |
| Extend noncanonical JSON descriptions | [[Data-Formats]], [[Extending-Arketype]] |
| Publish Wiki changes in its own repository | [[Publishing-the-Wiki]] |

## Crucial distinctions

**Archetype ≠ canonical semantic identity ≠ populated Kristal.** Labels, diagram nodes, recipe IDs and slugs describe designs. If a canonical Framework v11 semantic graph is authored later, its entity/property/assertion/source identifiers are namespace-scoped **KQ/KP/KA/KS**. Display words belong in separate dictionary layers. Wikidata **Q/P** IDs remain external and need independently reviewed `exactMatch` decisions.

`python arketype.py create` defaults to **legacy Kit 3.2.4**. `create --authoring v11` uses the bundled **Kit 4.0.0-draft.3**, but creates only a **blank v11-ready scaffold**. It does not automatically enable strict v11 or invent a KQ, QID, translation or validated semantic claim.

Arketype's own tests validate design consistency and the local scaffold, not factual correctness, legal/clinical suitability, Framework TCK conformance, live Wikidata integration, publication or activation.

**See also:** [[Architecture]] · [[Security-and-Boundaries]] · [[Glossary]] · [[FAQ]] · [[Update-Notes-v1-6]] · [[Snapshot-Verification-2026-10-27]].
