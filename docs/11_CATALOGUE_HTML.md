# Offline visual catalogue

The offline catalogue is a generated projection of Arketype 1.6.0 inventories: **19 archetypes**, **21 use-case profiles**, **23 composition recipes**, **10 visual patterns** and **40 situated diagrams**. Its visual illustrations are noncanonical.

```bash
python arketype.py build-html
python catalogue/creer_pdf.py
```

The second command requires `reportlab` and `cairosvg`; the v1.4.0 PDF is included. In `inventaires/profils-usage.json`, profile dimensions and coverage questions are separate from the archetype shape and its visual pattern. See `docs/12_USAGE_PROFILES_AND_SCOPES.md`. No real personal data or adjudicated claims are bundled.
