# Arketype 1.6.0 — mise à jour d'écosystème et du logo

> **Historical release record:** Results and file-presence claims below describe an earlier release validation. They are **not reproduced** by the uploaded 27 October 2026 source snapshot. See [snapshot verification](SNAPSHOT_VERIFICATION_2026-10-27.md) before citing these outcomes.

## État de la livraison

Bibliothèque de conception **non normative**. Arketype propose 19 archétypes, 23 assemblages, 21 profils d'usage et 40 illustrations. Les stubs historiques gardent leurs `state_ref`, leurs formes et les outils d'Authoring Kit **3.2.4**.

### Logo fourni et non transformé

Le SVG original fourni par l'utilisateur a été conservé octet pour octet sous `assets/logo-k.svg` (SHA-256 `6b02eaf8ab47803f58e8fd56c942c9438639c7a303fdb6a5ba4c5a3f9e137b28`). Le fichier `assets/logo-k-ui.png` est une simple rasterisation pour l'application Tkinter, pas une refonte artistique du logo. Les deux surfaces existantes l'utilisent : catalogue HTML hors ligne et lanceur GUI.

### Réparations du packaging

- 19 reçus de build v9 régénérés via le Kit historique de chaque modèle et conservés sous `modeles/*/build/v9/`. Ils sont des **reçus de génération technique**, pas des preuves d'assertions du domaine ni de publication.
- `modeles/dossier-suivi/design/fiche-deposition-vierge.json` : duplication incorrecte supprimée. La bonne fiche de suivi est conservée; la fiche de déposition demeure sous `deposition-temoignage`.
- Le catalogue HTML est régénéré depuis les inventaires et référence directement le logo approuvé.

### Références synchronisées

- **Framework 11.0.0-draft.4** : référence du design; les schémas v11 demeurent compatibles avec draft.3 selon le rapport de qualification du Framework, mais Arketype ne certifie pas le Framework ni n'altère ses schémas.
- **Authoring Kit 4.0.0-draft.3** : 11 fichiers `tools` et `templates` repris à l'identique depuis l'archive fournie, inventoriés et épinglés par SHA-256. Le mode `--authoring v11` crée un nouvel état **vide**, sans KQ/KP/Wikidata inventés ni activation automatique. Les nouvelles fonctions du Kit (`import-dik-catalog`, `select-v11-catalog`, `recover-v11`) sont présentes dans les nouveaux espaces de travail.
- **diK 1.0.0-alpha.7** : chemin de source locale fourni explicitement pour la commande `dik-coverage`, en lecture seule. diK n'est pas installé ni invoqué implicitement; les fonctions de curation et d'import sont propres à diK et au Kit, pas à Arketype.

### Limites

1. Les tests du mode diK alpha.7 contre le code source exact de cette version dépendent de la disponibilité de son dépôt séparé; aucun résultat ne doit être annoncé comme une qualification croisée sans ce test.
2. Arketype n'a aucune autorité sur les identités KQ/KP et ne délivre aucune approbation Wikidata.
3. Aucun workflow ne migre automatiquement les 19 modèles historiques en v11. Tout projet demande un nouveau registre, un graphe et un crosswalk validés puis une activation explicitement autorisée.
4. Le catalogue PDF historique n'est pas reconstruit si son fichier source n'est pas présent; le HTML reste l'interface documentaire complète.
5. Le PNG dérivé dépend de la conversion SVG effectuée pendant cette livraison; l'application distribuée peut l'afficher sans bibliothèque SVG additionnelle.

## Validation

```bash
python -m unittest discover -s tests -v
python arketype.py validate --check-kit
python arketype.py create --type taxonomie-classification --slug exemple-v11 \
  --title "Exemple v11" --parent . --authoring v11 --dry-run
```

Tous les résultats effectifs sont résumés dans `VALIDATION_160.md` à la racine.
