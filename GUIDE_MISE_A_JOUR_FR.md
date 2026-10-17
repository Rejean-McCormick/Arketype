# Mise à jour Arketype 1.6.0 (17 octobre 2026)

**Mise à jour technique, sans changement des contrats KQ/KP.** Le snapshot Arketype 1.5.0 conservait les 19 structures originales, mais certains artefacts du packaging avaient été exclus du ZIP.

## Installation et contrôle

1. Extraire l'archive Arketype 1.6.0 dans un dossier vierge.
2. Lancer `python -m unittest discover -s tests -v` et `python arketype.py validate --check-kit`.
3. Sous Windows, lancer `Lancer_Arketype.pyw`. Le logo SVG original fourni est maintenant dans `assets/logo-k.svg`, avec son PNG de présentation pour Tkinter.
4. Pour une nouvelle instance v11, choisir explicitement `--authoring v11`. Le nouvel espace est **vide** et utilise le Kit 4.0.0-draft.3; son catalogue de dictionnaires et son graphe doivent être créés/révisés séparément.
5. Si diK alpha.7 est disponible localement, utiliser `dik-coverage --dik-root ... --project ...` **en lecture seule**. Aucun script distant n'est téléchargé automatiquement.

## Corrections principales

- Reçus techniques v9 régénérés sans modifier les 19 identités `state_ref`.
- Formulaire de déposition séparé du dossier de suivi.
- Logo utilisateur SVG conservé tel quel et rasterisé uniquement pour la GUI.
- Pointeurs Framework `11.0.0-draft.4`, Authoring Kit `4.0.0-draft.3` et diK `1.0.0-alpha.7` actualisés.
- Source du Kit 4 épinglée avec SHA-256 et commandes de récupération / promotion diK incluses.

**Voir `VALIDATION_160.md` et `docs/15_MISE_A_JOUR_ARKETYPE_160.md`.**

---

# Arketype 1.5.0 — actualisation Framework v11 et diK

Nouveau mode de création `--authoring v11` (Authoring Kit 4.0.0-draft.1)
qui produit **un Kristal vide** avec une liste de préparation des identités
KQ/KP/KA/KS. Il ne forge pas de Q Wikidata, ne crée pas de traduction et
n'active pas le profil v11 sans registre/graphe/crosswalk/catalogue valides.

`python arketype.py semantic-status --path /chemin/kristal` examine l'état
local sans certifier la complétude.

`python arketype.py dik-coverage --dik-root /chemin/diK-v0.1.0 \n --project /chemin/dik.project.json --locales fr,en,fr-CA` utilise **explicitement**
la source locale de diK en lecture seule, sans requête réseau.

Le mode par défaut reste `legacy` avec le Kit 3.2.4. Les 19 modèles
historiques, leurs `state_ref` et les domaines canoniques d'origine sont
préservés. Les réceptions de build v9 manquantes ont été régénérées à partir
des modèles vides. Voir `docs/14_FRAMEWORK_V11_ET_DIK.md`.

La version ZIP reçue ne contenait pas le vrai logo : le dossier `assets/`
contient des **substituts minimalistes** clairement identifiés.

---

# Arketype 1.4.0 — guide de la mise à jour

Cette archive fait évoluer la bibliothèque Arketype 1.3.0 vers une bibliothèque de **structures et d'usages**. Elle conserve les **19 archétypes**, leurs identifiants ARK, leurs espaces de travail neutres et le Local Authoring Kit. Elle ajoute **16 nouveaux profils** (21 au total), **9 recettes** (23 au total), une typologie à plusieurs dimensions et un catalogue visuel mis à jour.

## Usages modélisés

- UCKK : fédération institution / voies / cours, intégration Moodle distincte.
- Mythologies : collection de traditions et comparaison attribuée.
- Ekole : cartographie d'organisations sociales contextualisées.
- Math : carrefours, endpoints, atlas de navigation et obligations de preuves.
- Dossiers individuels : scolaire, médical, civique, suivi d'employé.
- VehiculeDiag : diagnostic causal et mesures/tests de panne.
- PoliceOps et HospitalOps : procédures et autorisation externe.
- MediKristal : orchestration logicielle de bases de connaissances, non fusionnée en un Kristal.
- ScolQc : règles du système scolaire, selon juridiction et dates.

## Utilisation (depuis le dossier Arketype)

```bash
python arketype.py profiles
python arketype.py profile dossier-medical
python arketype.py recognize --path "C:/chemin/UCKK.zip"
python arketype.py recognize --path "C:/chemin/mes-kristals.zip" --focus A-Kristal-VehiculeDiag
python arketype.py scope-guide --profile navigation-preuves-longues --output guide-proposition.json
python arketype.py create --profile dossier-scolaire --slug exemple-scolaire --title "Dossier scolaire neutre" --parent . --dry-run
python arketype.py validate --check-kit
```

Le fichier `arketype.instance.json` d'un nouveau Kristal peut déclarer son profil d'usage. Un document `design/scope-guidance.json` y est ajouté **hors canon**. Le champ `state_scope` n'est pas injecté automatiquement.

## Sécurité, limites et Skope

La reconnaissance lit uniquement les noms de fichiers et des métadonnées bornées de workspaces. Les correspondances sont heuristiques, pas des certifications. Le guide de scope n'est pas directement compatible avec le contrat d'injection Skope v0.3 : Skope doit inspecter le workspace exact, établir les empreintes, vérifier les droits et demander une approbation avant toute injection. Aucun Kristal fourni en exemple n'est modifié. Les dossiers personnels réels ne doivent pas être ajoutés à cette bibliothèque publique.

Voir `docs/12_USAGE_PROFILES_AND_SCOPES.md`, `docs/13_SKOPE_COMPATIBILITY.md`, le Wiki et les schémas JSON.
