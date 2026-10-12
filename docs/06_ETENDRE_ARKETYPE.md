# Étendre la bibliothèque sans casser les contrats

Si une forme n'entre dans aucun archétype, ajouter une nouvelle fiche et un nouveau workspace neutre plutôt que de forcer une classification. Les **schémas JSON d’Arketype** sont disponibles dans `schemas/`, et restent strictement **non normatifs**.

Procédure proposée :

1. Définir un `slug` unique, un identifiant `ARK-XX` et les axes dominants : structure, ownership, épistémologie, dynamique.
2. Identifier le profil *existant* de l'Authoring Kit qui sert d'amorce; le profil n'a pas à être une catégorie normative.
3. Initialiser avec `outils/kristal.py init`, garder `status: stub`, n'enregistrer aucun artefact métier.
4. Produire `archetypes/<slug>.json` avec rôle, primitives, garde-fou, anti-modèle, question de conception et `template_path`.
5. Ajouter l'entrée correspondante dans `catalogue.json`, créer `modeles/<slug>/arketype.template.json` et `design/structure-candidate.json` explicitement hors canon.
6. S'il y a une composition récurrente, fournir une recette `assemblages/*.json` dont tous les composants sont `unresolved`.
7. Tester : `python arketype.py validate --check-kit` et `python -m unittest discover -s tests -v`.
8. Documenter les changements et les limites. Si un vrai contrat de domaine est souhaité, le faire porter et qualifier par le bon dépôt, **pas** implicitement par Arketype.

Le script `arketype.py` ne contient pas de liste codée en dur des archétypes. Il lit `catalogue.json` et les fiches pour permettre l'extension par métadonnées.

## Règle de version

- Changement documentaire : version mineure ou corrective d’Arketype selon portée.
- Changement de structure des fiches ou d'une recette : documenter migration et tests.
- Changement de Framework / Local Kit : épinglage nouveau après qualification distincte et comparaison des schémas.
- Aucune version Arketype ne change par elle-même le standard Kristal.
