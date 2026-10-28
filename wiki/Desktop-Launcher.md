# Desktop Launcher

Arketype 1.6.0 declares a single Windows desktop entrypoint: **`Lancer_Arketype.pyw`**, requiring Python 3.10+ with Tkinter. In a complete installation, the UI references `assets/logo-k.svg` and `assets/logo-k-ui.png` with brand color `#1E6864`. **Neither application image file is present in the uploaded code snapshot.** Check the complete checkout before relying on the logo or declaring the Windows package validated. The Wiki has its own independently copied SVG.

## Four screens, three workflows

- **Home:** a clear starting screen, with links to the three work areas.
- **Catalogue:** a searchable list of all 19 archetypes and 21 use-case profiles, with family/pattern filters. Select an entry to inspect its description; choose **Use selected archetype** to prefill the creation form. **Open full visual catalogue** opens the included HTML with its situated diagrams.
- **Create Kristal:** human-readable archetype names, relevant design-only assemblies, slug, title and parent directory; **Preview** checks the intended plan without writing; **Create Kristal** creates a neutral local workspace with its own identity; the v11-ready authoring option, if selected, does not enable strict v11 automatically.
- **Developer Ops:** a local console for approved Arketype CLI and test commands, with output logs and a command history. It does not offer an arbitrary operating-system shell.

## Usage boundaries

No UI action publishes, synchronizes, activates, or authorizes an operational response. All composition recipes remain design-only. A workspace starts with no canonical domain content. GUI operations are local. The historical 1.6.0 report describes Linux virtual-display testing, but those packaging checks fail against the provided code snapshot because image assets are missing. A native Windows machine test remains outstanding. See [[Snapshot-Verification-2026-10-27]].

**Next:** [Developer Ops](Developer-Ops) · [Working with Templates](Working-with-Templates) · [Visual Grammar](Visual-Grammar)
