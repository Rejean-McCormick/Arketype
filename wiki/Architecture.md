# Architecture

Arketype describes **structural families**, not a single universal Kristal schema. A usable knowledge state may be linear, branching, hierarchical, clustered, event-based, layered, or composed across separately owned states.

## Four different responsibilities

| Responsibility | Files | What they control |
| --- | --- | --- |
| Classification and discovery | `catalogue.json`, `archetypes/`, `inventaires/` | Candidate forms, intended uses, diagrams and boundaries |
| Local template initialization | `modeles/`, `outils/kristal.py`, `arketype.py` | Creation of neutral workspaces with new identities |
| Composition planning | `assemblages/`, `design/composition-plan.json` | Proposed relationships that are explicitly unresolved |
| Reader presentations | `catalogue/index.html`, optional PDF, GUI | Human-readable projections and navigation |

**Source of authority:** Arketype's JSON describes *Arketype*. It is not an authority over the truth of the domain content of an instance. A diagram is not an artifact commitment, and a reader projection is not the native Kristal model.

## Boundary rules

1. **Native knowledge vs. presentation:** a convenient tree or network rendering may omit information and must not silently replace the native structure.
2. **Identity vs. content:** each new local workspace receives its own `state_ref`; cloning another workspace's identity is not instantiation.
3. **References vs. ownership:** a link to another Kristal does not transfer ownership or materialize its canonical content.
4. **Facts vs. statements:** attribution, observation, hypothesis, proof status and interpretation are separate epistemic roles.
5. **Design vs. execution:** a procedural archetype can describe a protocol without providing an authorized operational workflow.
6. **Lifecycle separation:** build, qualification, synchronization, publication and activation are different activities.

## What the library ships

The repository contains **19** independently identifiable neutral Authoring Kit v9 template workspaces. The conceptual profiles and recipes do not create extra canonical states. They describe combinations that may be implemented after their logical contracts are designed.

Arketype currently references Authoring Kit **3.2.4** and Kristal Framework **10.0.0-draft.3.1** as design context. It does not claim to implement the full Framework by itself.

## Example: a non-destructive troubleshooting composition

```text
       [Causal diagnostics]
        /       |        \
 [Incident log] [State matrix] [Subsystem map]
        \        |        /
        unresolved references and ownership
```

Each component retains its own semantic purpose. The composition recipe is a proposal; no automatic canonical merge occurs.

**See also:** [Data Formats](Data-Formats), [Composition Recipes](Composition-Recipes), [Security and Boundaries](Security-and-Boundaries).
