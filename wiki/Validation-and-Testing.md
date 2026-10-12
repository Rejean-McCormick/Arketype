# Validation and Testing

Arketype uses Python's standard-library `unittest` suite and the bundled Kristal Authoring Kit to check local repository consistency.

## Run checks

```bash
python -m unittest discover -s tests -v
python arketype.py validate
python arketype.py validate --check-kit
```

The repository's GitHub Actions workflow (`.github/workflows/tests.yml`) runs unit tests and workspace checks on push and pull requests when hosted on GitHub.

## What the checks cover

- Catalogue entries, IDs, slugs, file paths and candidate family names.
- Empty template canons and non-normative statuses.
- Distinct workspace identities across all 19 shipped templates.
- Alignment of the 14 recipes and the five profiles to known archetypes.
- Diagram node and edge references across the 24 situated diagrams.
- Local Kit `check` verification for every neutral template.
- Local instantiation of selected new workspaces and preservation of independent identities.
- HTML generation, source links, logo reference and brand-color presence.

The v1.2.2 release report documents 33 passing tests and 19 passing Local Kit checks. Run the suite after editing this library; previous results do not guarantee future changes are correct.

## What the checks explicitly do not prove

They do not verify factual truth, the scientific correctness of a taxonomy, causal validity of a diagnosis, medical or legal fitness of a protocol, employee-record governance, production security, or automatic compliance with a future Framework release.

**Important distinction:** `check` is not `build-v9`; building is not qualification; qualification is not publication; publication is not activation.

**See also:** [Security and Boundaries](Security-and-Boundaries), [Working with Templates](Working-with-Templates).
