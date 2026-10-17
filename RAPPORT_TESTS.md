# Arketype 1.4.0 — validation de la bibliothèque d'usages

**Date : 13 octobre 2026** · **Livraison locale sans publication**

## Résultat

- **55/55 tests Python** réussis (`python -m unittest discover -s tests -q`).
- **19/19 modèles** reconnus et vérifiés par les commandes `check` du Local Authoring Kit (`python arketype.py validate --check-kit`).
- **19 archétypes ARK** existants préservés, **21 profils PRF**, **23 recettes de composition**, **40 diagrammes**, **10 motifs visuels**.
- Interface de bureau vérifiée sous Xvfb Linux avec 21 profils, y compris sélection du profil scolaire; vérification native Windows non effectuée.
- Projection HTML générée; catalogue PDF 1.4.0 de **21 pages**, contrôles visuels effectués sur les pages de couverture et de fin.
- Reconnaissance heuristique exercée sur les archives exemples UCKK, collection de traditions, Ekole, Grand Challenges, Formulator, VehiculeDiag, ScolQc et MediKristal. Une archive multi-projet exige `--focus` pour isoler le cas.
- Aucun projet d'exemple externe, état canonique, logiciel médical, cours Moodle ou dossier personnel n'a été modifié.

## Limites

- La reconnaissance n'inspecte que chemins de fichiers et métadonnées bornées. Elle n'évalue pas le contenu intégral ni la validité des preuves, des protocoles et des sources métier.
- Les questions de couverture sont toutes `not_evaluated` par conception.
- `arketype.scope-guidance/1.0` ne peut pas être injecté directement comme `state_scope`. Une application telle que Skope doit créer une proposition compatible avec son propre contrat, contrôler les empreintes et demander l'autorisation du propriétaire du workspace.
- Aucun test Windows natif, aucune validation clinique, juridique, culturelle ou pédagogique de terrain.

## Commandes de revalidation

```sh
python -m unittest discover -s tests -q
python arketype.py validate --check-kit
python arketype.py build-html
python catalogue/creer_pdf.py
```
