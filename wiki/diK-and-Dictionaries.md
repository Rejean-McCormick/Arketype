# diK and Multilingual Dictionaries in Arketype

**diK `1.0.0-alpha.7`** is a **separate local CLI** for lexical catalogues, coverage, reconciliation observations and controlled Wikidata snapshot imports. **Arketype 1.6.0 does not bundle or install diK**: it provides a deliberately explicit **read-only coverage bridge** to a trusted local source checkout.

## The supported Arketype command

```bash
python arketype.py dik-coverage \
  --dik-root /trusted/local/diK-v1.0.0-alpha.7 \
  --project /projects/demo/dik.project.json \
  --locales fr,en,fr-CA
```

Both paths are **local**. The project must include its real graph, registry, catalog and crosswalk dependencies. The command runs only the explicitly selected local diK CLI, returns the actual `kristal_dik_coverage_report` and does **not** write to Arketype or modify dictionary data. It does not invent missing labels or establish ownership of those KQ/KP concepts. **Executing a selected local checkout is a trust decision**; review its provenance before supplying `--dik-root`.

## How coverage should be interpreted

For an eligible canonical v11 Kristal, coverage measures KQ entities and KP properties separately:

- **Direct:** label in the requested locale.
- **Fallback:** label accessible only through a declared language fallback, such as `fr-CA → fr`.
- **Missing:** no direct or valid fallback term.
- **Conflicted:** competing observations require review; this is not an accepted equivalence.

A term supplied by a fallback is **not** counted as a direct translation. A legacy word-based graph has no legitimate canonical KQ/KP coverage measure until its identifiers have been reviewed and normalized.

## Dictionaries versus external identity mapping

| | Lexical dictionaries | External crosswalk |
| --- | --- | --- |
| Key | Namespaced KQ/KP and locale | Namespaced KQ/KP linked to external Wikidata Q/P |
| Purpose | Human labels, aliases, search, translation coverage | Reviewed, evidence-backed identity relationship |
| Sources | Curated language layers, imported labels | Versioned review decisions and provenance |
| Boundary | Same spelling may denote different concepts | A word match never proves `exactMatch` |

Framework v11 draft.4 supports catalog SHAs, source snapshots and coverage-report contracts. diK alpha.7 adds **local import with transactional SQLite checkpoints**, along with lexical conciliation and supervised evolution reports. Those features belong to **diK**, not Arketype's read-only bridge. Its large-import path is not yet certified against a production-size Wikidata dump. Arketype never runs it implicitly.

## Adoption and migration are separate steps

The Authoring Kit draft.3 owns **canonical publication** and registration. Its `import-dik-catalog` and `select-v11-catalog` commands support an explicit promotion workflow; `recover-v11` supports supervised recovery of interrupted registrations. [[diK-Catalog-Exchange-v11]] describes it. A normalized label is not a local identifier; reviewed legacy conversion plans do not authorize wholesale string replacement.

**See also:** [[Semantic-Authoring-v11]] · [[Ecosystem-Compatibility]] · [[Security-and-Boundaries]].
