# Forme native candidate

**Archétype Arketype :** ARK-02 — Fédération / topologie

Parent, enfants et frontières d’ownership avec états référencés.

## Primitives envisagées

- `noeuds`
- `liens_parent_enfant`
- `scopes`
- `references_epinglees`
- `statuts_de_cristallisation`

## Invariant d’intégrité conceptuelle

Le parent référence des engagements d’enfants; il ne s’approprie ni ne copie leur contenu.

## Fichier candidat

`design/structure-candidate.json` est une **aide**, pas une source de vérité et pas un contrat logique v9 enregistré. Avant toute utilisation, décider les primitives réelles, réduire/étendre la forme, documenter ce qui serait perdu lors d’une conversion et définir les Logical Contracts exacts.
