# Working with Templates

Every folder under `modeles/` is an **empty, independent workspace scaffold** based on the bundled Kristal Authoring Kit. The templates demonstrate a prospective native model kind; they are not real domain knowledge stores.

## Inspect a template

For example, `modeles/dossier-suivi/` contains a workspace definition, an empty canonical index, descriptive documents, and design-only examples such as a blank follow-up form.

| Path | Role |
| --- | --- |
| `kristal.workspace.json` | Local workspace identity and candidate native model |
| `canon/state.index.json` | Empty canonical artifact index |
| `design/structure-candidate.json` | Noncanonical illustration of candidate primitives |
| `design/fiche-suivi-vierge.json` | Blank example for case follow-up (where applicable) |
| `arketype.template.json` | Descriptive origin record for the archetype |
| `tools/kristal.py` | Bundled Authoring Kit Local Kit |

## Instantiate; do not copy an identity

The **recommended** workflow is `python arketype.py create`. It asks the Authoring Kit to run `init`, copies optional design scaffolds outside the canon, checks the new workspace, and gives the instance its **own** state identity.

Avoid copying a template directory and treating its `state_ref`, receipts, or artifacts as the identity of a separate Kristal. The template files are examples, not transferable provenance for your new instance.

## Optional v11-ready creation

The 19 supplied historical templates remain on their original Kit 3.2.4 profile. To initialize a **new** blank Kit 4.0.0-draft.3 scaffold, use `create --authoring v11`; this creates `design/v11-semantic-readiness.json` but no canonical KQ/KP, valid dictionary or live Framework qualification. See [[Semantic-Authoring-v11]] and [[diK-Catalog-Exchange-v11]].

## What creation does *not* do

- It does not generate domain facts, validated causal relationships, official procedures, or proofs.
- It does not register domain artifacts or resolve a logical contract.
- It does not resolve rights, retention, consent, ownership or external references.
- It does not publish, synchronize, activate or execute anything.

## Snapshot packaging caveat

The snapshot is missing the 19 historical `build/v9` receipts required by local validation. These files may have been filtered by the dump process. See [[Snapshot-Verification-2026-10-27]].

## Optional design forms

`deposition-temoignage` includes a blank testimony/deposition form in `design/`. `dossier-suivi` has its own blank follow-up form, but **the supplied snapshot also contains an unwanted deposition form in that dossier template**, contrary to the tests and release notes. It should be removed through a reviewed source change after verifying the full checkout; documentation edits do not fix the template. `etat-systemes` provides a blank system-state matrix example. Do not populate these public repository templates with real identifying or sensitive information.

**Next:** [CLI Reference](CLI-Reference) · [Data Formats](Data-Formats) · [Security and Boundaries](Security-and-Boundaries)
