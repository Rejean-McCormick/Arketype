# Forme native candidate

**Archétype Arketype :** ARK-03 — Carte de jalons et de preuves

Carte de carrefours, frontières atteintes et extrémités; références vers les preuves déjà faites ailleurs.

## Primitives envisagées

- `carrefours`
- `points_terminaux`
- `frontieres_atteintes`
- `arcs_resume`
- `references_de_preuve`
- `points_arrimage`
- `obligations_ouvertes`

## Invariant d’intégrité conceptuelle

Un arc abrégé n’équivaut pas à une preuve: lien vers preuve exacte, portée et statut de validation requis.

## Fichier candidat

`design/structure-candidate.json` est une **aide**, pas une source de vérité et pas un contrat logique v9 enregistré. Avant toute utilisation, décider les primitives réelles, réduire/étendre la forme, documenter ce qui serait perdu lors d’une conversion et définir les Logical Contracts exacts.
