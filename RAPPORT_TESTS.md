# Rapport de vérification — Arketype 1.2.1

## Résultats locaux

- **27/27 tests unitaires réussis** (17 tests historiques de la version 1.1 et 10 contrôles complémentaires).
- `python arketype.py validate --check-kit` : **OK**, 19 modèles vérifiés par l'Authoring Kit 3.2.4.
- **19 identités de workspace distinctes** : `state_ref` et `slug` alignés sur les 19 archétypes.
- **ARK-17, ARK-18, ARK-19 réinitialisés** par `kristal.py init` : `check`, `build-v9`, `check` réussis; reçus locaux alignés sur le `state_ref` et zéro artefact logique métier généré.
- **24 schémas situés** en JSON : 19 archétypes + 5 profils, avec vérification des références de nœuds et du statut `illustration_non_canonique`.
- **HTML généré** à partir des inventaires JSON et fiches de domaine; présence contrôlée du logo SVG, de `#1e6864`, des filtres et des liens de sources.
- **PDF illustré de 13 pages** construit depuis les mêmes inventaires, contrôlé visuellement sur la couverture, des pages d'archétypes et les profils d'usage. Aucune carte n'est divisée entre deux pages dans cette édition.
- Aucun changement GitHub distant, aucune publication, activation ou qualification métier.

## Limites

- Les dix motifs et les 24 diagrammes décrivent des formes de conception, **non des Logical Contracts** ou des preuves d'état.
- Les `check` et `build-v9` sur des workspaces vides vérifient l'enveloppe locale, pas la validité scientifique, juridique ou opérationnelle d'un domaine.
- L'interface Tkinter sous Windows et les rendus dans tous les navigateurs n'ont **pas** été testés ici.
- Le HTML est statique; exécuter `python arketype.py build-html` après une modification des inventaires.
- `python catalogue/creer_pdf.py` exige, pour régénérer le PDF, `reportlab` et `cairosvg` (le PDF est déjà inclus dans le dépôt).
- Les exemples de témoignages, de dossiers d'employés et d'états techniques sont **vierges**. Une application réelle devra définir droits d'accès, conservation, sécurité, responsabilité et autorité des sources.
