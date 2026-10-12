# Instructions de travail — Arketype

Arketype est une bibliothèque de conception, **pas** une autorité canonique ni un nouveau Framework.

- Préserver strictement le format de workspace du Local Kit 3.2.4; ne pas modifier les commandes de l’outil propriétaire.
- Les fichiers `archetypes/`, `assemblages/`, `design/`, `arketype.template.json` sont descriptifs et **non canoniques**.
- Toute instanciation crée un **nouveau** slug et `state_ref`; vérifier leur unicité à l’échelle du projet.
- Jamais de publication, activation, validation de faits, exécution de protocole ni données confidentielles par défaut.
- Ne jamais recopier un état engagé au lieu de le référencer avec son engagement exact.
- Aucun assemblage n’est automatiquement incorporé au canon. Documenter l’ownership avant de register-artifact.
- Exécuter les tests d’Arketype et, pour les workspaces, les vérifications `check` du Local Kit.
- Toute modification de modèle conceptuel doit modifier fiche, exemple et tests si applicable.
