# Arketype 1.6.0 — Rapport de validation

> **Historical release record:** Results and file-presence claims below describe an earlier release validation. They are **not reproduced** by the uploaded 27 October 2026 source snapshot. See [snapshot verification](docs/SNAPSHOT_VERIFICATION_2026-10-27.md) before citing these outcomes.

**Date :** 2026-10-17. **Statut :** bibliothèque de conception locale, non normative; pas de certification de l'écosystème complet.

## Baseline de l'archive reçue

- `python -m unittest discover -s tests -v` : **71 exécutés, 5 échecs, 1 erreur, 2 ignorés**. Problèmes : 19 reçus v9 absents, logo SVG/PNG absent, formulaire de déposition dupliqué dans `dossier-suivi`.
- `python arketype.py validate --check-kit` : **échec** ; 19 reçus absents et logo manquant.

## Résultats de cette livraison

- `python -m unittest discover -s tests -q` : **78 tests exécutés, 0 échec, 0 erreur, 2 ignorés**. Les deux ignorés exigent une copie locale externe de diK et de Framework au chemin de test explicitement configuré. Tous les tests réellement exécutés réussissent.
- `python arketype.py validate --check-kit` : **PASS**, 19 archétypes, 23 assemblages, 21 profils, 40 diagrammes.
- Les **19 reçus `build/v9`** ont été reconstruits par les outils Kit 3.2.4 déjà embarqués. Ils ont `generated_logical_artifacts=0`; les `state_ref` et `canon/state.index.json` restent inchangés.
- Le **SVG utilisateur est conservé octet pour octet** sous `assets/logo-k.svg`, SHA-256 `6b02eaf8ab47803f58e8fd56c942c9438639c7a303fdb6a5ba4c5a3f9e137b28`. `logo-k-ui.png` est un dérivé technique de ce SVG.
- `outils/authoring_v11`: **11 fichiers** du Kit 4.0.0-draft.3 copiés exactement depuis l'archive fournie, avec hash SHA-256 et tailles; l'inspection des pins est `vendored_source_verified`.
- La création réelle `--authoring v11` réussit : nouvel état vide, baseline Framework draft.4, Kit draft.3 et aucune identité Wikidata ou KQ inventée; aucune publication.
- La lecture de `contracts/release.json` et `contracts/contract-set.json` du Framework draft.4 fourni renvoie `declared_version_matches` **sans exécuter la TCK entière**.

## Compatibilité diK : portée exacte

La commande `dik-coverage` garde son comportement **lecture seule** et n'est exécutée que si l'opérateur fournit `--dik-root` et un projet diK local. La CLI attend une réponse `kristal_dik_coverage_report`. La version documentaire est actualisée à diK **1.0.0-alpha.7**. Le dépôt source exact de diK alpha.7 n'était pas présent localement lors des tests d'intégration de cette livraison : **aucune qualification croisée d'exécution avec diK alpha.7 n'est revendiquée**.

Le nouvel Authoring Kit 4.0.0-draft.3 embarqué inclut les commandes `import-dik-catalog`, `select-v11-catalog` et `recover-v11`; celles-ci n'ont pas été utilisées pour adopter une donnée de production dans Arketype. Les anciennes sources Framework draft.3 et nouvelles sources Framework draft.4 déclarent une compatibilité de schémas v11; Arketype ne modifie pas les contrats normatifs.

## Non effectué / travaux externes

- Test GUI sur Windows natif (la présence du PNG et le chemin de chargement sont vérifiés, mais Windows et son presse-papiers ne sont pas testés ici).
- Test sur un vrai dump Wikidata et sur des dictionnaires massifs, signatures de réviseurs et processus d'activation.
- Qualification complète TCK Framework, autorisation de publier une instance Kristal, ou déploiement sur GitHub.

Le manifeste de fichiers `INVENTAIRE.json` décrit les octets de la livraison; ce n'est pas un engagement sémantique Kristal.
