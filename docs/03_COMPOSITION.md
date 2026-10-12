# Composition — règles et frontières

Les fichiers `assemblages/*.json` sont des **recettes non normatives**. Leur statut `design_only` et le statut `unresolved` de chaque composant sont obligatoires. L'outil `arketype.py compose` crée **un seul workspace primaire** et y dépose un **plan non canonique** `design/composition-plan.json`. Il ne crée pas les sous-Kristals, ne les fusionne pas, et n’enregistre aucun artéfact.

## Relations de conception

| Relation | Sens | Travail à faire |
|---|---|---|
| `reference_externe` | Un état/artefact d’un autre Kristal serait référencé | Définir cible, contrat, état et engagement exact; ACL et couverture |
| `projection_ou_reference` | Vue ou membre lié à un autre domaine | Choisir et documenter les pertes / frontières de représentation |
| `projection_derivee` | Une vue calculée ou une simulation est envisagée | Conserver provenances et hypothèses; pas de canon indu |
| `couche_candidate` | Structure native potentiellement interne | Vérifier compatibilité, contrat et propriété du domaine |
| `sous_modele_candidate` | Sous-modèle du système hybride envisagé | Définir domaine, limites, contrats et décideurs indépendants |
| `a_decider` | Ajout libre par l'auteur | Ne rien promettre avant la décision de frontière |

## Invariants de composition

1. Référence ≠ transfert d'ownership. Un parent UCKK conserve sa topologie, pas les connaissances d’un cours.
2. Vue Moodle ≠ état canonique du contenu d'enseignement. De même une vue muséale Ekole n'est pas une deuxième source de vérité.
3. Un arc résumant une démonstration doit citer une **preuve exacte à portée vérifiable**; sans cela c'est de la navigation/hypothèse.
4. Une procédure connue n'accorde aucune permission d'exécution; un modèle de diagnostic ne prend pas la responsabilité d'une décision médicale ou policière.
5. Les entrées d’une compilation ne changent ni auteur ni droits ni vérité par leur inclusion.
6. Aucun fichier Arketype ne remplace la procédure du Local Kit pour créer les Logical Artifacts et leurs engagements.
7. Le modèle reste extensible : la découverte d’une structure inconnue peut justifier un nouvel archétype.

## Exemple : plan de carte de preuves

```
carrefour A ----(référence de preuve épinglée)----> carrefour B
     |                                                   |
  arrimage X                                           terminal
     \________________ obligation encore ouverte _______/
```

**Les traits du diagramme sont conceptuels et n’affirment pas des preuves effectives.** Les étapes internes déjà prouvées ailleurs ne sont pas recopiées; la carte ne garde que les points d'articulation, le bord atteint et les références de preuve.
