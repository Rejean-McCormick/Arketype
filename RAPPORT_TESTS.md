# Arketype 1.3.0 — Unified desktop launcher verification

## Scope

The repository contains **19 neutral Kristal templates** with distinct `state_ref` identities, **14 design-only compositions**, **5 situated use-case profiles**, **10 visual patterns**, and **24 situated diagram records**. The former creation-only Tkinter window has been replaced by a desktop launcher with Home, Catalogue, Create Kristal and Developer Ops. The provided logo and brand color `#1E6864` appear in the UIs, not the README.

## Verification performed

- **43/43 Python tests passed** on the extracted repository, including the existing Authoring Kit checks and new launcher command parsing, rejection, and hash-verification tests.
- The new launcher was instantiated and navigated under `xvfb-run` on Linux: all four pages opened; the catalogue exposed 19 archetypes and five profiles; profile-to-creator handoff selected the intended primary archetype and composition recipe.
- Console commands use a fixed allowlist, separate subprocess arguments (`shell=False`) and background execution; no arbitrary shell, publishing, synchronization or activation command is offered.
- The catalogue HTML and **13-page A4 PDF** were regenerated from the English JSON source and the PDF was rendered for visual inspection.
- GitHub Wiki sources now document the new launcher and Developer Ops in English; the repository README remains English and contains no logo.
- The supplied Authoring Kit executable remains unmodified, and technical identifiers remain stable.

## Qualification limits

The desktop UI has **not been tested on an actual Windows computer**; only a virtual-display Linux smoke test was performed. Passing local `check` and `build-v9` on empty templates does not validate real domain knowledge. There is no remote publication/activation and no real HR, testimony, or sensitive data in the templates.
