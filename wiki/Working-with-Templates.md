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

## What creation does *not* do

- It does not generate domain facts, validated causal relationships, official procedures, or proofs.
- It does not register domain artifacts or resolve a logical contract.
- It does not resolve rights, retention, consent, ownership or external references.
- It does not publish, synchronize, activate or execute anything.

## Optional design forms

`deposition-temoignage` includes a blank testimony/deposition form in `design/`. `dossier-suivi` includes a separate blank casefile form; these forms are intentionally not interchangeable. `etat-systemes` provides a blank system-state matrix example. Do not populate these public repository templates with real identifying or sensitive information.

**Next:** [CLI Reference](CLI-Reference) · [Data Formats](Data-Formats) · [Security and Boundaries](Security-and-Boundaries)
