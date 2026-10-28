# Semantic Authoring with Framework v11

**Applies to:** Arketype **1.6.0**, optional bundled Authoring Kit **4.0.0-draft.3**, design baseline Framework **11.0.0-draft.4**. The Framework v11 semantic schemas remain compatible with draft.3 in the provided release; neither Arketype nor diK owns the canonical semantic contract.

## Why this is opt-in

The **19 historical models** retain their Kit **3.2.4** origin, existing independent `state_ref` identities and v9/v10 contracts. New `--authoring v11` workspaces use Kit draft.3. Arketype does **not** convert historical templates, allocate KQ/KP/KA/KS, infer identities from words, create external Wikidata QIDs or activate strict v11.

```bash
python arketype.py create \
  --type referentiel-semantique --slug essai-v11 \
  --title 'Référentiel de démonstration' --parent . \
  --authoring v11 --dry-run

python arketype.py create \
  --type referentiel-semantique --slug essai-v11 \
  --title 'Référentiel de démonstration' --parent . \
  --authoring v11

python arketype.py semantic-status --path ./essai-v11
```

The new workspace contains an **empty canonical state**, a new `state_ref`, the draft.3 Kit and noncanonical guidance in `design/v11-semantic-readiness.json`. `semantic-status` reads local readiness metadata, **not** an independently qualified graph.

## From blank scaffold to a valid v11 graph

The authorized workspace owner must:

1. Allocate namespace-scoped **KQ** (entities), **KP** (properties), **KA** (assertions) and **KS** (sources) through the identity registry; `Q8018` never replaces a Kristal `KQ…`.
2. Author the **language-neutral graph**. Text literals remain valid only in fields where the schema permits them; labels must not substitute for semantic identifiers.
3. Maintain versioned dictionaries separately, with locale layers, SHAs and declared fallback rules.
4. Supply a reviewed external crosswalk. `accepted + exactMatch` requires evidence and provenance; unmatched Kristal concepts need not be mapped.
5. Register the graph, registry, crosswalk and catalog as the appropriate **v9 Logical Artifacts** in the Authoring Kit.
6. Explicitly enable v11 and run the Kit's `check-v11`, `check` and `build-v9`. A build is **not** publication or activation.

The Kit draft.3 additionally offers `import-dik-catalog`, `select-v11-catalog`, `recover-v11`, `qualify-v11`, `coverage-v11`, `check-v11-plan` and `apply-v11-plan`; these are **Kit commands**, not `arketype.py` commands. [[diK-Catalog-Exchange-v11]] explains the guarded handoff.

## Legacy mode remains available

```bash
python arketype.py create \
  --type referentiel-semantique --slug essai-legacy \
  --title 'Exemple historique' --parent .
```

This remains the bundled historical Kit 3.2.4 path. Reusing a template's `state_ref` or its receipts to represent a new workspace is forbidden.

## Boundaries

Arketype itself never creates domain facts, allocates arbitrary KQ/KP identifiers, approves a Wikidata mapping, downloads Wikidata, rewrites legacy texts or publishes a Kristal. Source migration is a reviewed operation of an authorized producer; the diK CLI provides lexical analysis and proposals, not canonical graph authority.

**See also:** [[Getting-Started]] · [[diK-and-Dictionaries]] · [[diK-Catalog-Exchange-v11]] · [[Validation-and-Testing]].
