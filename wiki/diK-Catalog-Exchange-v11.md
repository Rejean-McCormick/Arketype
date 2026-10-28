# Exchange a diK dictionary catalog with Authoring Kit v11

**Scope:** Arketype 1.6.0 / Framework 11.0.0-draft.4 / Authoring Kit 4.0.0-draft.3 / diK 1.0.0-alpha.7. This is a **separate, opt-in authoring workflow**, not a command exposed by `arketype.py`, and not an automatic synchronization service.

## Who owns what?

| Component | Authority |
| --- | --- |
| Arketype | Design-only archetypes, recipes, blank workspace creation |
| diK | Versioned lexical catalogs, coverage, review proposals and Wikidata import observations |
| Framework v11 | Schemas, namespace and semantic identity contracts, validation rules |
| Authoring Kit | Canonical graph authoring, v9 artifact registration, review-gated catalog promotion and publication workflow |

**KQ/KP/KA/KS are Kristal's namespace-scoped identities. Wikidata Q/P are external.** No matching word or redirection can silently become an accepted semantic identity.

## Recommended workflow

1. **Create an empty v11-ready workspace** with Arketype. `create --authoring v11` produces a new `state_ref`, no domain assertions and no arbitrary Wikidata QIDs.
2. **Prepare and inspect a diK catalog** outside Arketype. diK alpha.7 can import reviewed labels into a new immutable snapshot; existing human-curated layers remain separate. Validate graph, registry, crosswalk, locales and source hashes using the Framework before adoption.
3. **Import as a distinct catalog revision** using the **workspace-local Authoring Kit**, not `arketype.py`:

   ```bash
   python tools/kristal.py import-dik-catalog . \
     --catalog /trusted/dik-snapshots/catalog.json \
     --revision dictionary-review-2026-10-17
   ```

   The Kit also supports `--register` with suitable artifact metadata when the workspace is ready for v9 logical artifact registration. Review `python tools/kristal.py import-dik-catalog --help` and its contracts; import alone does **not** activate the new catalog.
4. **Select explicitly only after validation and registration**, using `select-v11-catalog` with the proper catalog reference, then run `check-v11`, `check` and `coverage-v11` on a fully configured v11 workspace. Do not select before required graph/registry/crosswalk artifacts exist.
5. If registration is interrupted, inspect `recover-v11 --mode status` and only then decide whether authorized recovery should `finish` or `rollback`. Rollback must never delete a canonical artifact that was already committed to `state.index.json`.

## Example: supervised recovery and verification

```bash
# Run these in the created workspace, only after all v11 prerequisites exist.
python tools/kristal.py recover-v11 . --mode status
python tools/kristal.py check-v11 .
python tools/kristal.py coverage-v11 . --locales fr,en,fr-CA
```

**Important:** This Wiki does not claim that a sample catalog has been promoted to production. The 1.6.0 Arketype test suite did not perform a full cross-repository diK alpha.7/Kit draft.3 production qualification.

## Prohibited shortcuts

- No rewriting canonical KQ/KP identifiers from translated labels.
- No implicit crosswalk `exactMatch` from Wikidata Q/P or spelling similarity.
- No overwriting a published catalog or silently replacing the active graph.
- No assuming an imported but not selected catalog becomes active.
- No claiming that a local hash alone authenticates Wikidata provenance.

**See also:** [[Semantic-Authoring-v11]] · [[diK-and-Dictionaries]] · [[Security-and-Boundaries]] · [[Ecosystem-Compatibility]].
