# Sources, compatibilité et provenance

Arketype a été construit **localement à partir des archives remises par l'utilisateur**, pas à partir d’une branche distante vérifiée :

- `Typotheque_Kristal_v0.1.zip` : seize workspaces neutres et premier classement; base conservée et renommée dans Arketype.
- `znapshot_Kristal-Authoring-Kit_10112137.zip` : outils et profils **3.2.4** (copiés sous `outils/` et déjà présents dans les modèles); source technique de `init`, `check` et `build-v9`.
- `znapshot_Kristal-Framework_10112137.zip` : baseline **10.0.0-draft.3.1**, invariants et responsabilités sémantiques.
- `UCKK-Kristal-v9(2).zip` ; `ekole.zip` ; `Ekole_Kristal_Organisations_Humaines_Autochtones_Europeens_Quebec_v1(3).zip` : topologies et usages éducatifs.
- `SmartSnap(20261012-013829).zip` ; `BU-10-Kristaux-Custom-Depart.zip` : patterns MediKristal, diagnostic, œuvres et autres formes.
- `KRISTAL_ECOSYSTEME_INSTRUCTIONS_IA(3).md` et `SYSTEME_KRISTAL_KOA_CONTEXTE_IA_2026-10-09(2).md` : rôles et limites des applications.

**Limites de provenance** : ces fichiers ne prouvent ni l’état actuel du dépôt distant, ni les licences de distribution du kit, ni des tests E2E avec les applications. La redistribution de Arketype incluant une copie du Local Kit doit être vérifiée auprès du propriétaire des droits avant diffusion externe; aucun nouvel octroi de licence n'est affirmé ici. La copie est livrée pour l'usage local demandé.

## Passage à la version 1.1.0 et changement de nom

- La bibliothèque de modèles est désormais diffusée sous le nom **Arketype**.
- Les identifiants `TK-01..TK-15` sont conservés comme `legacy_id`; les fiches Arketype portent `ARK-01..ARK-15`.
- Les workspaces d’origine sont conservés, sans réécriture de leur `state_ref`, car ce sont des templates distincts et neutralisés.
- Les nouvelles instances sont initialisées par le Local Kit, avec nouveau slug/`state_ref` selon le slug; contrôler les collisions de noms dans un catalogue global en cas de déploiement distribué.
- Les propositions de structure et d'assemblage n’ont **jamais** le statut de Logical Artifact engagé.

- La version 1.1.0 ajoute `ARK-16` et un 9e assemblage; elle modifie les espaces de noms de métadonnées non normatifs et les noms des outils (`arketype.py`). Ce changement **ne migre aucun état canonique Kristal**.
- Les fichiers de modèles et données sources existants restent indépendants du dépôt renommé.
