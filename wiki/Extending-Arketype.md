# Extending Arketype

New archetypes should add genuinely useful structural distinctions instead of duplicating an existing archetype for every business use case. Use a **profile** when an application can be expressed as an existing form or composition; add a new archetype when the underlying structure has a different responsibility, epistemic model or integrity rules.

## Suggested workflow

1. Identify the central structural question and primary visual pattern.
2. Define the ownership boundary, epistemic status types, candidate primitives, invariant and anti-pattern.
3. Decide whether a new archetype is needed, or whether a new use-case profile is sufficient.
4. If new, create a new `archetypes/<slug>.json` and add its entry to `catalogue.json`.
5. Initialize a **new and distinct** neutral workspace using the bundled Authoring Kit; never clone a prior workspace's identity or build receipt.
6. Write noncanonical shape proposals in `modeles/<slug>/design/`, not committed domain facts in its `canon/`.
7. Add or update `inventaires/archetypes-visuels.json`, `inventaires/diagrammes-situes.json`, and relevant profile and composition inventories.
8. Add tests for referential integrity, identity uniqueness, and all new constraints. Run the Local Kit and full test suite.
9. Regenerate `catalogue/index.html`. Update these wiki pages when the conceptual library changes.

## Archetype design questions

- What does this structure *own* that another does not?
- Does it preserve attributed statements, observations, hypotheses, rules, events, references, or proofs?
- Is the native model a hierarchy, sparse graph, sequence, matrix, casefile, federation, or something else?
- Which relationships are references rather than incorporated content?
- Which summaries are derived and may lose information?
- Which permissions, validations and logical contracts must a real implementation add?

Arketype metadata uses its existing descriptive JSON format and English Wiki naming; avoid inventing alternate canonical Kristal schemas under the guise of a new archetype.

**See also:** [Archetype Catalog](Archetype-Catalog), [Data Formats](Data-Formats), [Validation and Testing](Validation-and-Testing).
