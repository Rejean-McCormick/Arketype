# Getting Started

Start from a **local copy** of the full Arketype repository. Python **3.10 or later** is recommended; basic browsing and the included HTML catalogue do **not** require Python, internet access, or a database.

## 1. Browse the visual catalogue

Open `catalogue/index.html` from the extracted repository. Search by keyword, filter by family or structural pattern, and inspect the labeled diagrams. Each archetype card links to a descriptive JSON file; use-case cards link to their proposed composition recipes. The catalogue is an offline generated projection.

A printable edition is included as `catalogue/Arketype_Visual_Catalogue_v1.2.2.pdf`. It is optional: HTML is the primary interface.

## 2. Inspect the library

From the repository root:

```bash
python arketype.py list
python arketype.py search "protocol"
python arketype.py show procedure-protocole
python arketype.py profiles
python arketype.py profile suivi-employe
python arketype.py recipes
python arketype.py recipe troubleshooting-systeme
```

The CLI uses stable *slugs* (for example `etat-systemes` and `dossier-suivi`). Reader-facing text is in English. Existing French-derived slugs and machine property names are retained as stable identifiers to preserve compatibility.

## 3. Preview an instantiation

```bash
python arketype.py create   --type diagnostic-causal   --slug lab-diagnostics   --title "Lab Diagnostics"   --parent .   --dry-run
```

The dry run reports the intended destination, archetype and design plan. It writes nothing.

## 4. Create a new, blank Kristal

Run the same command without `--dry-run`. Arketype asks the bundled Authoring Kit to initialize an independent workspace; it copies optional structure proposals into `design/`, verifies the local workspace, and refuses to overwrite an existing destination.

The generated template is **empty**, not a populated diagnostic knowledge base. Before adding real data, define domain identity, provenance, privacy constraints, semantic ownership, logical contracts and validation criteria.

## 5. Preview a composition proposal

```bash
python arketype.py compose   --recipe troubleshooting-systeme   --slug diagnostics-plan   --title "Diagnostics Plan"   --parent .   --dry-run
```

This produces a preview of components and unresolved responsibilities. It never fuses independently owned canonical states.

## 6. Validate

```bash
python -m unittest discover -s tests -v
python arketype.py validate --check-kit
```

To regenerate the HTML after updating source JSON:

```bash
python arketype.py build-html
```

For the optional GUI on Windows, launch `Lancer_Arketype.pyw` with Python/Tkinter. Its supplied logo and the `#1E6864` brand color appear in the UI; the GUI remains optional and has not been tested on every Windows configuration.

**Next:** [Working with Templates](Working-with-Templates) · [CLI Reference](CLI-Reference) · [Security and Boundaries](Security-and-Boundaries)
