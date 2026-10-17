# Interoperability with Skope and local Kristal workspaces

Arketype 1.6.0 publishes **design guidance**, never an injection command. It does not modify external Kristals when recognizing profiles or drafting scopes.

## Contract boundary

1. Arketype profile: `inventaires/profils-usage.json` (noncanonical).
2. Arketype scope guidance: `arketype.scope-guidance/1.0` validated by `schemas/arketype.scope-guidance.schema.json`.
3. Skope proposal: `skope.kristal-scope-proposal/1.0` is a *different* format; Skope v0.3 expects `workspace`, fingerprint, inspected file fingerprints and `proposed_state_scope`.
4. Skope (or another host) must independently inspect the actual workspace, preserve its existing scope and generate an approved proposal in its **own** validated contract before any write. Do **not** inject the Arketype design JSON as `state_scope`.
5. The Authoring Kit remains the build/check owner; `build-v9` does not publish or certify domain truth.

## Recommended integration fields

For a *new neutral* Kristal created by Arketype, `arketype.instance.json` now optionally records `use_case_profile`. This is descriptive origin metadata and can be read by Skope. An imported/legacy Kristal may have no such metadata, or have a candidate but unconfirmed match. The recognition CLI emits transparent evidence and does not silently invent an Arketype origin.

**Read-only by default:** `recognize` and `scope-guide` do not write inside input archives, access remote services or inspect canonical sensitive data. No backfill into user projects is performed by this release.
