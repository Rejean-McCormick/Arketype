# Arketype Wiki — 1.6.0 update notes

**17 October 2026.** The separate Wiki is aligned with the **Arketype 1.6.0** release distributed locally. The source snapshot was the user's `Arketype.wiki(1).zip`; this update applies to the **Wiki**, not to the Arketype application itself.

## Changes

- Updated the current baselines to **Framework 11.0.0-draft.4**, **Authoring Kit 4.0.0-draft.3** and separately supplied **diK 1.0.0-alpha.7**.
- Explained that Arketype uses Kit **3.2.4** for its 19 historical neutral templates and Kit **draft.3** only for new, blank `--authoring v11` workspaces.
- Corrected diK's read-only bridge to use an explicitly selected local checkout; added [[diK-Catalog-Exchange-v11]] for the separate Kit catalog import, registration, selection and recovery commands.
- Recorded the **historical release report** result of **78 executed; 76 passed, 2 skipped, 0 errors/failures**. This is **not reproduced** on the uploaded 27 October source snapshot; consult [[Snapshot-Verification-2026-10-27]] for the actual rerun.
- Included the **approved SVG byte-for-byte** as Wiki `assets/logo-k.svg`; application logo assets are absent from the uploaded code snapshot.
- Preserved the **19 archetypes**, **23 recipes**, **21 profiles**, **40 diagrams**, historical pages, stable page slugs and the original `GitSink.bat` and `ZmartZnap.pyw` attachments.
- Updated sidebar navigation and checked all intra-Wiki links and Markdown syntax in the packaged files.

> **Later verification (2026-10-27):** The source snapshot is missing the 19 v9 receipts and the app SVG/PNG and still includes the extra casefile deposition form; 78 tests ran, with 6 failures, 3 errors and 2 skips. Details: [[Snapshot-Verification-2026-10-27]].

## What was not done

- No code changes to Arketype itself, Framework, Authoring Kit or diK.
- No GitHub push, no production Kristal mutation, and no network/real Wikidata benchmark.
- This Wiki revision is documentation alignment; independent execution of every external TCK and native Windows smoke tests remain outside its scope.

**Earlier context:** [[Update-Notes-v1-5]] is retained as a historical record, not the current release note. **Validation:** [[Validation-and-Testing]].
