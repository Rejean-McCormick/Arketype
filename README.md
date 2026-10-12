# Arketype

![Symbole K fourni](assets/logo-k.svg)

**Couleur de marque : `#1E6864`**

**Version 1.2.1 — Bibliothèque d’archétypes, profils d’usage et catalogue visuel pour Kristal**

Arketype répertorie des formes de Kristals, leurs propriétés, leurs structures candidates, des **workspaces neutralisés**, des compositions guidées, des **profils d’usage situés** et un **catalogue HTML** généré depuis des inventaires JSON.

Le dépôt contient **19 archétypes**, **19 modèles locaux vides**, **14 assemblages de conception** et **5 profils d’usage**. Les modèles ne contiennent aucun fait métier, aucune donnée réelle et **ne créent aucune autorité ni permission de publier**.

## Nouveau dans cette version

- **catalogue HTML** : `catalogue/index.html`
- **grammaire visuelle standardisée** : linéaire, embranchements, hub, grappe, arbre, timeline, matrice, casefile, multicouche, réseau
- **inventaires JSON liés** : `inventaires/grammaire-visuelle.json`, `inventaires/archetypes-visuels.json`, `inventaires/profils-usage.json`
- **nouveaux archétypes** :
  - **ARK-17** — Taxonomie / classification naturelle
  - **ARK-18** — État de systèmes / parc technique
  - **ARK-19** — Dossier de suivi / casefile
- **nouveaux profils d’usage** : troubleshooting de système, environnement protocolaire, taxonomie de la nature, état de systèmes, suivi d’employé

## Démarrer

```bash
python arketype.py list
python arketype.py profiles
python arketype.py profile troubleshooting-systeme
python arketype.py build-html
python arketype.py validate --check-kit
```

Le catalogue HTML généré se trouve par défaut dans `catalogue/index.html`.

## Catalogue visuel et impression

Ouvrir **`catalogue/index.html`** après extraction de l'archive. Aucune connexion n'est nécessaire.
Rechercher par mot-clé et filtrer par famille ou motif. Chaque carte comprend un diagramme **situé avec nœuds nommés** et un lien vers sa fiche JSON.
Pour régénérer le catalogue après modification des inventaires :

```bash
python arketype.py build-html
```

Un exemple PDF est également fourni dans `catalogue/Arketype_Catalogue_Visuel_v1.2.1.pdf`. Pour imprimer depuis Chrome/Edge, utiliser Imprimer → PDF (les cartes et diagrammes disposent d'une mise en page dédiée).

**Sources :** `catalogue.json`, `archetypes/*.json`, `inventaires/archetypes-visuels.json`, `inventaires/grammaire-visuelle.json`, `inventaires/profils-usage.json` et `inventaires/diagrammes-situes.json`. L'HTML est une projection générée et non une vue synchronisée en temps réel; la commande `build-html` effectue sa mise à jour.

**Identité et sécurité :** chaque modèle neutre doit posséder un `state_ref` propre. Les reçus `build-v9` sont des preuves d'exécution technique locale, **pas** une qualification sémantique. Pour les témoignages et dossiers d'employés, ne pas saisir de données sensibles dans les modèles publics : les politiques d'accès, de conservation et de consentement restent à concevoir.
