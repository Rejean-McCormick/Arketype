# Offline visual catalogue

`catalogue/index.html` is a generated, standalone HTML reader view with the supplied logo and the **#1E6864** brand palette. It presents 19 archetypes, 5 situated profiles, 10 graphical patterns and 24 labeled diagrams.

The cards are generated from the source JSON inventories and linked archetype records, rather than from a hidden or separately maintained HTML model.

Regenerate after editing source files:

```bash
python arketype.py build-html
python catalogue/creer_pdf.py
```

The second command requires `reportlab` and `cairosvg`. The printable PDF is included in the repository as `catalogue/Arketype_Visual_Catalogue_v1.4.0.pdf`.

Reader illustrations contain no actual employee data, testimony, system secrets or operational approvals.
