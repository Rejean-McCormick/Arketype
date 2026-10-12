# Extending Arketype

1. Decide whether the proposed idea is a **new structural archetype**, a **situated profile**, or simply an **assembly** of existing forms.
2. Give new archetypes stable IDs and slugs; preserve existing identifiers that may be referenced by other users.
3. Write the metadata record in `archetypes/` and add it to `catalogue.json`.
4. Describe the visual pattern and situated reader diagram in `inventaires/`; every new archetype should have a labeled illustration.
5. Initialize a **new independent** stub via the bundled Authoring Kit. Never duplicate another workspace's `state_ref` or its build receipt.
6. Add noncanonical design candidates, provenance considerations, integrity rules and English documentation.
7. Run the full library tests, `validate --check-kit`, and `build-v9` for any newly initialized template.
8. Regenerate the HTML and optional PDF and refresh `INVENTAIRE.json`.

The repository intentionally keeps technical slugs and schema keys stable. Translate reader-facing prose without renaming machine identifiers in place.
