# Data Formats and Inventory Relationships

Arketype's inventories are JSON files under source control. They provide **descriptive design metadata**, not authoritative domain state. The catalogue HTML is generated from these inputs and from the individual archetype files.

## Data layout

```text
Arketype/
├── catalogue.json
├── archetypes/*.json
├── inventaires/
│   ├── archetypes-visuels.json
│   ├── grammaire-visuelle.json
│   ├── diagrammes-situes.json
│   └── profils-usage.json
├── assemblages/*.json
├── modeles/<archetype-slug>/
├── catalogue/index.html
└── wiki/*.md
```

| File | Key fields | Owner of meaning |
| --- | --- | --- |
| `catalogue.json` | `archetypes[]`, `inventories`, `version` | Library index |
| `archetypes/*.json` | `id`, `slug`, `family`, `kit_profile`, `integrity_rule`, `template_path`, `visual_pattern` | Candidate archetype definitions |
| `inventaires/archetypes-visuels.json` | `slug`, `visual_pattern`, `secondary_patterns`, `situational_schema` | Catalogue visual index |
| `inventaires/grammaire-visuelle.json` | `patterns[]` | Standard visualization vocabulary |
| `inventaires/diagrammes-situes.json` | `kind`, `slug`, `pattern`, `nodes[]`, `edges[]`, `status` | Noncanonical example drawings |
| `inventaires/profils-usage.json` | `primary_archetype`, `supporting_archetypes`, `inputs`, `outputs`, `boundaries` | Example application scenarios |
| `assemblages/*.json` | `primary_archetype`, `components`, `composition_status`, `publication_authorization` | Proposed composition design |
| `INVENTAIRE.json` | `path`, `sha256`, `size_bytes` | Archive byte inventory, not a logical commitment |

## Example: a noncanonical visual association

```json
{
  "visual_pattern": "matrix",
  "secondary_patterns": ["timeline"],
  "situational_schema": "Systems compared across dated operational observations"
}
```

This is an **illustrative excerpt**, not a complete validated archetype file. It expresses a presentation choice. The real source data remains in the repository JSON.

## Keeping sources and the HTML aligned

Edit the appropriate JSON file, review the related archetype or use-case profile, run `python arketype.py validate`, then regenerate the HTML with `python arketype.py build-html`. Diagram coordinates and edges in the visual inventory must refer to nodes that exist in that diagram.

An HTML view does **not** automatically refresh when JSON changes and does not gain semantic authority by being published on a website.

## Repository inventory vs. state commitment

`INVENTAIRE.json` describes byte-level files in a distribution. It is not a replacement for source provenance, a pinned external commitment, or a Kristal logical contract. Similarly, the template `build/v9` receipts document local technical generation and do not establish domain truth.

**See also:** [Visual Grammar](Visual-Grammar), [Architecture](Architecture), [Extending Arketype](Extending-Arketype).
