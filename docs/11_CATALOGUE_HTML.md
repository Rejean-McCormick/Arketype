# Catalogue HTML · Arketype 1.2.1

`catalogue/index.html` utilise les données des inventaires JSON et les fiches descriptives pour produire 19 cartes d’archétypes et 5 profils d’usage.

- Mode hors ligne, sans dépendance réseau. Logo SVG fourni dans `assets/logo-k.svg`.
- Couleur principale : `#1E6864`.
- Recherche locale, filtre par famille, filtre par motif.
- Schémas SVG **situés**, sérialisés dans `inventaires/diagrammes-situes.json`.
- Liens relatifs vers les fichiers JSON après extraction.
- CSS d’impression A4, avec cartes non divisées et détails dépliés.
- PDF statique de référence dans `catalogue/Arketype_Catalogue_Visuel_v1.2.1.pdf`.

Regénérer : `python arketype.py build-html`. Ce fichier généré **n’est pas un runtime live** ni une publication Kristal. Les schémas sont des illustrations non canoniques.

Pour régénérer le PDF : `python catalogue/creer_pdf.py` (nécessite les bibliothèques Python `reportlab` et `cairosvg`).
