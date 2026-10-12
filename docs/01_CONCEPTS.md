# Concepts et vocabulaire

**Arketype** : bibliothèque d'archétypes indépendante du standard Kristal; elle ne définit aucune nouvelle identité sémantique, aucune action automatique et aucun nouveau `Logical Commitment`.

- **Archétype** : pattern de structure native et de responsabilité. Il décrit les informations que pourrait posséder un Kristal, ses obligations de preuve, sa frontière et ses anti-modèles.
- **Modèle de départ (template)** : workspace techniquement initialisé par le Local Kit, de statut `stub`. Il ne possède aucun artefact canonique métier.
- **Instance** : nouveau workspace doté du slug choisi et du `state_ref` généré par le Local Kit. L'unicité globale des slugs reste la responsabilité du propriétaire; deux machines pourraient choisir le même slug.
- **Composition** : relation de conception entre plusieurs archétypes, pouvant aboutir à des artefacts au sein d'un Kristal, à plusieurs Kristals référencés, à une vue dérivée ou à un processus externe. Arketype ne décide pas à leur place.
- **Profil de destination** : école, musée, recherche, répertoire, loisir, formation, application clinique, etc. Aucun profil d'usage n'impose une forme native.
- **Plan de composition** : document `design/` qui liste des liens non résolus, sans engagement ni autorisation.

Le mot **conforme** ne qualifie jamais automatiquement un Kristal obtenu depuis Arketype. La validité d’un workspace au regard de `check` signifie que l'enveloppe est cohérente, pas que les assertions sont vraies, utiles, légalement publiables ou intégrées à un système.

## Distinctions essentielles

| Élément | Responsable |
|---|---|
| Ontologie, état, engagements v9/v10 | Kristal Framework et propriétaire du Kristal |
| Initialisation, édition, check, build | Kristal Authoring Kit |
| Classement, aide à la sélection, modèles neutres | Arketype |
| Inventaire et synchro de surface | Manager |
| Qualification, publication, activation | Qualificateurs + Bootstrap/Setup, avec autorisation |
| Lecture contextualisée | Kompiler |
| Affichage et navigation | Konstellation |
| Exécution des tâches métier | Applications concernées, jamais déduite du canon |

Principe : **source ≠ preuve de vérité ≠ engagement logique ≠ autorité ≠ droit d'agir ≠ publication**.
