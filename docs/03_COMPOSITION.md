# Composition without loss of authority

A composition recipe indicates which archetypes might collaborate in a specific use case, but it is always **`design_only`** and its links remain **`unresolved`**.

Before implementing a composition, decide the semantic owner of each claim, the references to exact external commitments, the logical interface boundaries, the appropriate validation, access controls and any information loss caused by projections.

- **Reference, do not silently duplicate.** A federation may link child Kristals without owning their complete content.
- **Keep operational systems separate.** A protocol document and a real-world execution engine have different permissions and failure modes.
- **Do not promote derived outputs.** Search indexes, summaries, AI analyses and HTML diagrams remain reader representations unless explicitly admitted under a defined contract.
- **Preserve provenance.** Proof maps, testimony dossiers, chronological records and derived interpretations must remain distinguishable.

Use `python arketype.py recipes` to inspect proposed combinations and `python arketype.py compose --recipe ... --dry-run` to review the design without writing a workspace.
