# Arketype 1.4.0 — v10 ecosystem compatibility release report

## What changed in the uploaded source archive

- Added **Developer Ops > Ecosystem Compatibility** with explicitly selected paths for local Framework, Authoring Kit, Kristal workspace, Manager and Bootstrap checkouts. All checks are read-only; no external command is executed by the inspector.
- Added allowlisted `compat` command, static file inspections, byte hashes, and clear `not_configured`, `review_required`, `declared_version_matches`, `metadata_only` and `identical_bytes` statuses.
- Added ecosystem boundaries and usage documentation in English, including GitHub Wiki and README; retained supplied logo exclusively in HTML and desktop interfaces and brand color `#1E6864`.
- Preserved 19 empty workspaces, 14 design-only assemblies, 5 use-case profiles, 10 visual motifs and 24 situated diagrams. Their original technical IDs, state_refs and the bundled Authoring Kit 3.2.4 are not changed.
- Fixed a **pre-existing regression in the uploaded 1.3.0 repository**: the `dossier-suivi` blank template contained an extra `design/fiche-deposition-vierge.json` that its own validator forbids. Removed only this inappropriate noncanonical copy; the original blank form remains in `deposition-temoignage`.
- Added a two-platform (Windows and Ubuntu), Python 3.11/3.12, read-only test matrix and `permissions: contents: read`. Repository actions are still tag-based and **immutable pin verification** remains a GitHub maintainer follow-up.
- Regenerated the offline HTML and **13-page A4 PDF** from the English JSON sources. Removed stale PDF versions and `.git` metadata from the distributable ZIP.

## Tests and inspection

- **51/51 Python unittest tests passed** on the extracted local repository, including 8 new ecosystem tests.
- `python arketype.py validate --check-kit`: **PASS**, 19 archetypes, 14 recipes, 5 profiles and 24 diagrams, all 19 local Kit checks.
- Linux virtual-display Tkinter smoke: **PASS** for the four launcher pages, `Ecosystem Compatibility` refresh/output, and selecting a use-case profile into the Create Kristal form.
- Printable PDF generated as `catalogue/Arketype_Visual_Catalogue_v1.4.0.pdf` and its English A4 cover visually inspected.
- Source ZIP CRC and every file-inventory SHA-256 verified at packaging.

## Deliberate evidence limitations

- A Framework `10.0.0-draft.3.1` label is a **declared design baseline**, not proof of Framework conformance or an approved GitHub commit SHA.
- Local file byte identity proves only identity of bytes, not a qualified logical commitment or current remote HEAD.
- The inspector does not run the Framework TCK, Manager runtime, Bootstrap doctor/plan/apply, KristalDiag/C1, C2 grants, C3 publishing, GitHub networking, or AI/domain builds on selected workspaces.
- Manager source availability, GitHub collection readiness and Windows-native GUI testing remain separate tasks.
- **No GitHub repository was changed, pushed, qualified, synchronized, published or activated.** This is a complete updated local source distribution for review/commit.
