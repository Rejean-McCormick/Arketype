# Concepts and terminology

Arketype is a **non-normative structural archetype library** for Kristals. It does not create new Framework commitments, domain facts, permissions or an operational control plane.

- **Archetype:** a proposed structural and responsibility pattern, including candidate primitives, integrity obligations, anti-patterns and semantic ownership boundaries.
- **Template:** an initialized `stub` workspace with an empty domain canon, using the bundled Local Authoring Kit.
- **Instance:** a new workspace with a separately generated `state_ref` and a chosen slug. Cross-repository slug uniqueness remains the owner's responsibility.
- **Composition:** a design relationship among independently owned structures. It might later become cross-Kristal references, a derived view, a logical artifact or an external process, but is not automatically any of those.
- **Use-case profile:** a situated example such as a university, museum, troubleshooting workflow or casefile. An intended use does not dictate a unique native form.
- **Composition plan:** an unresolved, design-only record stored outside canonical artifacts.

Passing `check` means that the local envelope passed specified technical checks. It does **not** establish scientific truth, legal validity, data disclosure rights or permission to publish.

## Responsibilities

| Concern | Responsible component |
| --- | --- |
| Knowledge state, identity, commitments | Kristal Framework and the state owner |
| Workspace initialization, checking, builds | Kristal Authoring Kit |
| Archetype classification, selection and blank templates | Arketype |
| Inventory and reading-surface synchronization | Kristal Manager |
| Qualification, publication, activation | Dedicated, separately authorized workflows |
| Contextual reading | Kompiler |
| Reader visualization and navigation | Konstellation |
| Operational actions | Domain application, not inferred from a knowledge artifact |

**Source ≠ verified truth ≠ logical commitment ≠ authority ≠ permission to act ≠ publication.**
