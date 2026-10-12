# Visual Grammar

Arketype uses a shared set of **10 visual patterns** to help readers recognize the shape of a Kristal. These are diagram conventions, not a mandatory set of classes in the Kristal Framework. A model can have a *primary* pattern and multiple secondary patterns.

| Pattern ID | English name | Sketch | Typical purpose |
| --- | --- | --- | --- |
| `linear` | Linear sequence | `A → B → C` | Steps, learning paths, simple transitions |
| `branching` | Branching sequence | `A → decision → B/C` | Protocols, conditional procedures |
| `hub` | Center and satellites | `observations ↔ problem ↔ tests` | Diagnostics, proof maps |
| `cluster` | Cluster / constellation | interconnected groups | Semantic references, media worlds |
| `tree` | Tree / taxonomy | root → classes → leaves | Natural classification, hierarchies |
| `timeline` | Timeline | `t₁ — t₂ — t₃` | Logs, research history, case follow-up |
| `matrix` | State matrix | systems × attributes | Equipment status, comparison |
| `casefile` | Casefile | case → notes/pieces/actions | Testimony, employee follow-up |
| `multilayer` | Layered model | observations / hypotheses / interpretations | Alternative views or organizational layers |
| `network` | Network / federation | independent nodes with references | Campuses, subsystem federations |

## Illustrative diagrams vs. logical models

Every card in the HTML catalogue can use a **situated diagram** with named nodes, from `inventaires/diagrammes-situes.json`. Its nodes and edges are explicitly illustrative. The layout coordinates are only visual; they are **not** canonical data identifiers or proof relationships.

The diagram format includes a `kind` (`archetype` or `profile`), a `slug`, a `pattern`, labeled `nodes`, `edges`, and a non-canonical status. The renderer creates SVG locally from these JSON objects.

A taxonomy is often a tree, but natural classification can include synonyms, exceptions and cross-links. A troubleshooting model may look like a hub in a summary diagram but include a causal network and chronological observations. **Do not force the underlying data to match a pictogram.**

## How to choose a primary pattern

Choose the pattern that best expresses the **main structural responsibility**, not merely what looks attractive. If the intended primary question is “what happened and when?”, start with a timeline. If it is “which systems have which states?”, start with a matrix. If it is “which class contains this object?”, start with a tree. Other motifs may be secondary projections.

**Sources:** `inventaires/grammaire-visuelle.json`, `inventaires/archetypes-visuels.json`, `inventaires/diagrammes-situes.json`.
