# Validation and Testing

Arketype 1.6.0 uses the standard-library `unittest` suite and bundled Authoring Kit tools to validate its **local design library and workspace scaffolds**.

## Supplied code snapshot (27 October 2026): reproduced results

I ran the standard unit-test and Kit-validation commands against the uploaded code snapshot. **78 tests ran: 67 passed, 6 failed, 3 errors, 2 skipped.** `validate --check-kit` reported **`ok: false`**.

Failures and errors arise because the snapshot lacks application `assets/logo-k.svg` / `assets/logo-k-ui.png`, lacks all 19 expected `build/v9/build-receipt.json` files, and includes `modeles/dossier-suivi/design/fiche-deposition-vierge.json` contrary to the tests. Generated or untracked files may have been excluded by the snapshot collector: **this is not proof that a complete local checkout has the same omissions**.

The historical `VALIDATION_160.md` and `test-results.json` record an earlier **76 passed, 2 skipped, 0 failures/errors** result. Those recorded release figures are **not** a substitute for testing the specific snapshot or the repository checkout. See [[Snapshot-Verification-2026-10-27]].

The two skipped tests depend on exact external Framework/diK checkouts. Neither this run nor the historical reports certify full Framework conformance, a production-size Wikidata load, or native Windows deployment.

## Run locally from the Arketype repository root

```bash
python -m unittest discover -s tests -v
python arketype.py validate
python arketype.py validate --check-kit
```

The source repository's GitHub Actions workflow can run unit tests and local workspace checks after hosting/configuration. The Wiki itself is a separate documentation repository and does not execute these tests when published.

## What checks cover

- The **19** archetypes, source slugs, families, identities and neutral workspaces.
- The **23** `design_only` recipes, **21** profiles and **40** situated diagrams.
- Distinct `state_ref` values and no claims of populated canonical domain truth.
- The **expected** 19 historical v9 receipts (missing in the supplied code snapshot).
- Correct separation of deposition and casefile forms (the supplied snapshot still contains an extra deposition form under `dossier-suivi`).
- Presence/hash of the application SVG and PNG (both application assets are absent in the supplied snapshot; the Wiki SVG is available separately).
- Bundled Kit **4.0.0-draft.3** vendor-file pins and opt-in v11 empty creation; read-only diK references.
- HTML catalogue generation and local CLI/GUI smoke checks in the stated environments.

## What it does **not** prove

Technical `check` ≠ semantic qualification ≠ `build-v9` ≠ publication ≠ activation. No validation establishes factual correctness, clinical/legal suitability, production privacy, live network reachability, TCK completion, or integrity of an arbitrary user's Wikidata mirror.

**References:** `VALIDATION_160.md`, `RAPPORT_TESTS.md`, `docs/15_MISE_A_JOUR_ARKETYPE_160.md`, and the new `docs/SNAPSHOT_VERIFICATION_2026-10-27.md`. **See also:** [[Security-and-Boundaries]] · [[diK-Catalog-Exchange-v11]] · [[Update-Notes-v1-6]].
