# Parcours de travail pour un Kristal réel

## Choisir

1. Expliquer en une phrase ce que l’état logique portera *réellement*.
2. Séparer savoir propre, références externes, décisions d'usage, matériel source et système transactionnel.
3. Interroger le catalogue (par ex. `python arketype.py search "chronologie"`) ; lire les fiches détaillées.
4. Choisir **l’archétype principal**, puis, si nécessaire, une recette d’assemblage ou `--with`.

## Créer et inventorier

1. Utiliser l’interface `Lancer_Arketype.pyw` ou la CLI `arketype.py create/compose`.
2. Le dossier créé a une configuration `kristal.workspace.json` propre à son slug, l’identité initialisée par le Local Kit, les docs de frontière, un plan de composition non canonique et un canon vide.
3. Avant de partager le dossier, vérifier si le nom choisi entre en collision avec des `state_ref` d’autres Kristals.
4. Conserver `arketype.instance.json` comme provenance descriptive, sans l’assimiler à un manifeste de publication.

## Développer

1. Établir la portée, les interlocuteurs, les usages et les régimes de preuve.
2. Résoudre les composants de `design/composition-plan.json` : champ `relation`, source, état exact, droits, pertes éventuelles et décideur.
3. Créer **seulement les vrais artefacts métier** dans `canon/domain/`, avec des contrats et sources enregistrés dans le workspace selon le Local Kit.
4. Exécuter le `check` puis le `build-v9` du Local Kit; consigner les preuves de tests. Ne pas prendre le build pour une publication ni pour une validation scientifique.

## Publier seulement si autorisé

Toute qualification, synchronisation, publication ou activation doit emprunter les outils et politiques propriétaires de l’écosystème. Arketype n'a pas de bouton « publier », y compris dans son interface graphique.

## Travailler sur la carte de preuves

La carte n’encode pas toutes les étapes internes. Elle peut contenir :

- `carrefours` : bifurcations ou convergences à valeur de navigation et de raisonnement.
- `extremites` : frontières connues d'une exploration, terminus réussis ou points arrêtés, avec statut explicite.
- `arcs_resume` : relations abrégées, accompagnées de la référence exact d’une preuve quand cette preuve existe.
- `preuves_referencees` : référence vers l’artefact, l’état, le commitment et la portée de la démonstration propriétaire.
- `points_arrimage` : points prévus pour raccorder d'autres formalismes ou Kristals.
- `obligations_ouvertes` : liens qui ne peuvent pas encore être promus au rang de démonstration.

La forme candidate est dans `modeles/carte-jalons-preuves/design/structure-candidate.json`. Elle n'est **pas** encore un contrat de domaine, et n'a aucun contenu prouvé prérempli.
