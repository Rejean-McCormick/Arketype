# Arketype in the Kristal v10 ecosystem

**Status:** non-normative design library. **Framework reference:** `10.0.0-draft.3.1` (draft). **Bundled Authoring Kit:** `3.2.4`.

Arketype is a source-code and template catalogue. Its models and composition recipes are **design-only**. They are neither registered domain Logical Artifacts nor an official framework schema, nor qualified or published GitHub v10 nodes. Arketype never assumes authority over existing Kristals.

## Component boundaries

| Component | Owner's responsibility | What Arketype does |
| --- | --- | --- |
| Kristal Framework v9/v10 | Logical commitments; optional hosted-network contracts | Declares a version reference, does not reimplement conformance |
| Authoring Kit | Initializes and checks workspaces; builds v9 and read surfaces | Uses the bundled 3.2.4 Kit for new neutral workspaces |
| KristalDiag / C1 | Independent qualification | Does not issue C1 receipts |
| Bootstrap + C2/C3 | Grants, hosting node configuration, qualification and publication gates | Does not grant, deploy, sync, publish or activate |
| Kristal Manager | Registry of actual local workspaces and controlled sync | Can inspect presence of its local source; no registry replacement |
| Konstellation | Navigation **across Kristals and inside selected Kristals** | Offers **declared** archetype patterns as noncanonical visual hints, not a global instance inventory |
| Kompiler | Read-only semantic Context Packs | No generation of domain Context Packs |
| GitHub host | Authorized hosted read surfaces and collections | Independent source-code repository (do not put Arketype itself under `kristal-public/kristals/`) |
| Kristal-Kollection | Legacy/historical crosswalk | Not an operational registry for this version |

## Optional pattern metadata

`archetypes/*.json` and `inventaires/*.json` contain descriptive `id`, `slug`, `visual_pattern`, responsibility, integrity and use-case information. Consumers may use these data **only as UI conventions** and should attach them to an instance only with an **explicit, attributable mapping**. A local file name or tree shape is not proof of an archetype, semantic type, commitment, provenance or public status.

## Developer Ops > Ecosystem Compatibility

The inspector reads local metadata and hashes only. No GitHub URL is contacted. It does not execute the selected external toolkit, parse the domain's canonical artifacts, build AI projections, create receipts, or perform a publication action. Output statuses have narrow meanings:

- `identical_bytes`: selected external Authoring Kit matches the bundled `outils/kristal.py` exactly at SHA-256.
- `declared_version_matches`: inspected Framework `release.json` and `contract-set.json` declare the catalogue's draft reference; this **does not** run Framework TCK or validate compatibility lock content.
- `templates_consistent`: 19 empty templates have distinct identities and a declared v10 target; run `validate --check-kit` for stronger local envelope checks.
- `metadata_only`: only a selected workspace descriptor/authoring index was inspected, without reading contents.
- `runtime_source_present` / `source_present`: files appear at expected locations; **no runtime execution** is implied.
- `not_configured`, `not_available`, `source_incomplete`, `review_required`: unavailable/unknown/mismatched evidence, never PASS.

Choose local checkout paths in the GUI, or run:

```bash
python -m unittest discover -s tests -v
python arketype.py validate --check-kit
python -c "from arketype_ecosystem import inspect_ecosystem,format_ecosystem_report;print(format_ecosystem_report(inspect_ecosystem()))"
```

The built-in Developer Ops command `compat` accepts optional `--framework`, `--kit`, `--workspace`, `--manager` and `--bootstrap` **local paths**. It never connects to GitHub. These flags do not alter any workspace.

## Outstanding ecosystem qualification

A complete Manager runtime checkout, exact approved Framework commit pin, signed C1/C2 gate interoperability, C3 `kristals/index.json`, and a qualifying hosted read surface are separate cross-repository work. Arketype cannot declare them complete from local metadata, and a GitHub repository listing would not prove them.

**Non-equivalences:** Logical Commitment ≠ blob digest; State Commitment ≠ Git SHA; build ≠ qualification; sync ≠ immutable publication ≠ activation; read surface ≠ canonical state; reference ≠ ownership.
