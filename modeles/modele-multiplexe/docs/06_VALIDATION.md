# Validation considerations

1. Identify the actual semantic owner and sources.
2. Define the candidate native schema and applicable Logical Contract.
3. Preserve provenance and versioning as required by the domain.
4. Confirm the integrity condition: Avoid collapsing relationships from different layers.
5. Separate technical workspace validation from domain factual, scientific, legal and operational qualification.
6. Make explicit publication, activation and reader-access decisions separately.

The included Local Kit `check` and `build-v9` commands establish only the technical properties that they test.
