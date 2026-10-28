# Arketype 1.6.0 — supplied snapshot verification (2026-10-27)

## Scope

This report concerns the **uploaded code snapshot** `arketype_Code_snapshot(2).zip` (803 indexed source files), not a fresh clone of the author's full Git repository, the independently stored GitHub Wiki, or any production Kristal. Generated/untracked artifacts might have been excluded by the snapshot tool. No code, data, or canonical state has been changed.

## Identified references

The snapshot declares release `1.6.0` in `README.md` and `catalogue.json`. `outils/authoring_v11/VERSION` and `VENDOR_PIN.json` declare an opt-in bundled Authoring Kit `4.0.0-draft.3` and Framework `11.0.0-draft.4`. Documentation references separately supplied diK `1.0.0-alpha.7` (not bundled). The source inventories contain 19 structural archetypes, 23 assembly recipes, 21 use-case profiles and 40 situated diagrams.

## Direct verification

Commands executed on a clean extraction of this supplied snapshot (Python 3.13 on Linux):

```bash
python -m unittest discover -s tests -q
python arketype.py validate --check-kit
```

**Observed result:** 78 tests executed: **67 passed, 6 failed, 3 errors, 2 skipped**. The `validate --check-kit` command returned `ok: false`.

Problems attributable to this snapshot's filesystem:

1. **Missing application logo files.** `assets/logo-k.svg` and `assets/logo-k-ui.png` are absent. Logo-related checks error/fail, and the repository's GUI/HTML references do not make the assets exist. The separate *wiki* copy of the SVG is available, but was not installed into application `assets/` by this documentation update.
2. **Missing historical receipts.** None of the 19 `modeles/*/build/v9/build-receipt.json` files is present. The regression and Kit-validation checks expect them; do not mark those checks as passing for this snapshot.
3. **Misplaced deposition form.** `modeles/dossier-suivi/design/fiche-deposition-vierge.json` is present, despite the 1.6.0 report and tests requiring it to be absent. `modeles/dossier-suivi/design/fiche-suivi-vierge.json` and the proper deposition template under `modeles/deposition-temoignage` are present. This is a source-tree discrepancy, not something to silently fix by editing a Wiki.

The historical `VALIDATION_160.md` and `test-results.json` record **76 passed, 2 skipped and no failures/errors** for a previous distribution. Those figures have not been reproduced on the uploaded snapshot and **must not be repeated as the current snapshot result**. They can remain historical records, with this note linked from the README and Wiki.

## Recommended next steps in the complete checkout

- Confirm whether the snapshot collector omitted `assets/` and `build/v9/`. If those files are present in the full repo, regenerate an inclusive snapshot and rerun tests instead of making claims based on an incomplete archive.
- If absent in the actual repository, restore the approved SVG/derived PNG **from verified original assets** and regenerate the 19 receipts using the repository's documented Authoring Kit workflow, without changing any committed canonical state or `state_ref`.
- Review the extra dossier/deposition design file. Delete or relocate it only through an authorized code change and rerun the regression suite.
- Re-run `python -m unittest discover -s tests -q` and `python arketype.py validate --check-kit` on the **actual checkout** before reporting release packaging or GUI validation as passed.
- Independently run external Framework/diK integration and native Windows tests where required. The code snapshot alone is insufficient to assert end-to-end interoperability.

## Documentation policy

The README and GitHub Wiki use English. Historical version notes may remain for traceability, but their conclusions are not treated as current pass/fail evidence. The Wiki is a separate Git repository: updating `wiki/` in the source repository does not automatically publish it.
