# Rapport des contrôles — Arketype 1.1.0

**Contexte :** copie locale du dépôt, sans accès réseau ni publication.
**Kit de création utilisé :** Kristal Authoring Kit 3.2.4 livré dans les archives du projet.
**Standard de référence documentaire :** Kristal Framework 10.0.0-draft.3.1.

## Résultats observés

| Contrôle | Résultat |
|---|---|
| Fiches de définition des archétypes | **16/16** présentes, catalogue cohérent |
| Modèles neutres (workspaces locaux) | **16/16** avec canon vide |
| Assemblages de conception | **9/9** cohérents, non canoniques |
| Validation JSON Schema descriptive | **16/16** fiches et **9/9** assemblages |
| `python arketype.py validate --check-kit` | **Réussi**, 16 modèles vérifiés par le Local Kit |
| `build-v9` sur les modèles neutres | **16/16** réussis, **0 membre logique** dans chacun |
| Tests standard library, y compris instanciations réelles locales | **17/17 réussis** |
| Compilation syntaxique `arketype.py`, `Lancer_Arketype.pyw`, tests | **Réussie** |
| Recherche du nom et sigle retirés dans le dépôt | **Aucune occurrence** dans les fichiers contrôlés |
| Description GitHub en anglais | **332 caractères**, sous 350 |
| Exécution graphique de l'interface Tkinter sous Windows | **Non testée** |
| Opérations de recueil réel de dépositions | **Non implémentées** |
| Autorisation, qualification juridique, confidentialité opérationnelle | **Non qualifiées** |
| Publication réseau, activation et intégration E2E | **Non réalisées** |

## Modèle ARK-16 : dépositions / témoignages

- `modeles/deposition-temoignage/kristal.workspace.json` : initialisé par le Local Kit, statut `stub`.
- `canon/state.index.json` : **aucun artefact canonique**.
- `design/structure-candidate.json` : structure candidate **hors canon**.
- `design/fiche-deposition-vierge.json` : modèle de recueil **vierge**, non sécurisé et **hors canon**.
- `assemblages/dossier-depositions.json` : plan sans composition canonique ni autorisation de publication.
- L'instanciation de test crée un nouveau `state_ref` et conserve le formulaire vide.

## Rejouer les tests

```bash
python arketype.py validate --check-kit
python -m unittest discover -s tests -v
python modeles/deposition-temoignage/tools/kristal.py build-v9 modeles/deposition-temoignage
```

Résultats par modèle : `test-results.json`.

**Portée de la qualification :** ces vérifications portent sur la structure des workspaces et la logique de création de la bibliothèque. Elles ne prouvent ni la justesse de futurs témoignages ni la conformité à une procédure d'audition ou à une règle de confidentialité.
