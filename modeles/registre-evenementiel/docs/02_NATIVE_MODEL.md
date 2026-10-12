# Forme native candidate

**Archétype Arketype :** ARK-11 — Registre événementiel / chronologie

Événements successifs, révisions, validités temporelles et relations historiques.

## Primitives envisagées

- `evenements`
- `acteurs`
- `horodatages`
- `validites`
- `liens_causaux_hypotheses`
- `versions`

## Invariant d’intégrité conceptuelle

Distinguer date des faits, date d’enregistrement et ordre de saisie; ne pas effacer les corrections.

## Fichier candidat

`design/structure-candidate.json` est une **aide**, pas une source de vérité et pas un contrat logique v9 enregistré. Avant toute utilisation, décider les primitives réelles, réduire/étendre la forme, documenter ce qui serait perdu lors d’une conversion et définir les Logical Contracts exacts.
