# CLI Reference

Run `python arketype.py` from the repository root. The CLI ships with the complete Arketype archive and delegates workspace initialization and checks to the bundled Authoring Kit.

| Command | Purpose | Example |
| --- | --- | --- |
| `list` | List archetypes | `python arketype.py list` |
| `list --family` | Filter by one source family | `python arketype.py list --family Structures` |
| `search TERM` | Search names, descriptions and use cases | `python arketype.py search "nature"` |
| `show SLUG` | Print one archetype | `python arketype.py show taxonomie-classification` |
| `profiles` | List situated profiles | `python arketype.py profiles` |
| `profile SLUG` | Inspect one situated profile | `python arketype.py profile suivi-employe` |
| `recipes` | List design-only compositions | `python arketype.py recipes` |
| `recipe ID` | Print one composition recipe | `python arketype.py recipe taxonomie-nature` |
| `create` | Initialize an empty workspace | See below |
| `compose` | Initialize with a conceptual composition plan | See below |
| `validate` | Validate Arketype catalogue metadata | `python arketype.py validate` |
| `validate --check-kit` | Also check each local template with the Kit | `python arketype.py validate --check-kit` |
| `build-html` | Regenerate the offline visual catalogue | `python arketype.py build-html` |

## v1.6 optional authoring and read-only semantic helpers

| Command | Supported behavior |
|---|---|
| `create --authoring legacy` | Default Kit 3.2.4 neutral historical workspace |
| `create --authoring v11` | Create a **new, empty** Kit 4.0.0-draft.3 workspace plus noncanonical readiness guidance |
| `compose --authoring v11` | Optional v11-ready neutral composition scaffold; no automatic canonical merging |
| `semantic-status --path PATH` | Inspect local v11 profile/readiness metadata **only** |
| `dik-coverage --dik-root DIR --project FILE --locales fr,en,fr-CA` | Run explicitly selected local diK `1.0.0-alpha.7` in **read-only** report mode |

```bash
python arketype.py create --type referentiel-semantique \
  --slug example-v11 --title "Example v11" --parent . --authoring v11
python arketype.py semantic-status --path ./example-v11
python arketype.py dik-coverage \
  --dik-root /trusted/diK-v1.0.0-alpha.7 \
  --project /projects/example/dik.project.json --locales fr,en,fr-CA
```

`--authoring v11` **does not** issue KQ/KP, assign Wikidata QIDs, enable strict v11, rewrite an older Kristal or install diK. The newer `import-dik-catalog`, `select-v11-catalog` and `recover-v11` subcommands belong to the **Kit inside a workspace**, not to `arketype.py`. See [[Semantic-Authoring-v11]], [[diK-and-Dictionaries]] and [[diK-Catalog-Exchange-v11]].

## `create` and `compose`

Both accept `--type`, `--slug`, `--title`, `--parent`, optional `--profile`, `--recipe`, repeatable `--with`, `--dry-run` and `--authoring {legacy,v11}`. For `compose`, a `--recipe` or at least one `--with` is required. If `--recipe` is supplied, the primary archetype may be inferred; any explicit `--type` must match its primary archetype.

```bash
python arketype.py create   --type etat-systemes   --slug workstation-state   --title "Workstation State"   --parent .
```

```bash
python arketype.py compose   --recipe suivi-employe   --slug employee-case-design   --title "Employee Case Design"   --parent .   --dry-run
```

The `--slug` accepts lowercase ASCII letters, digits and internal hyphens, up to 80 characters. The parent folder must already exist and the destination must not. The command exits with an error instead of overwriting.

## `build-html` output

By default, HTML is written to `catalogue/index.html`. You can direct output elsewhere:

```bash
python arketype.py build-html --output ./preview/catalogue.html
```

The output is a static projection of the current JSON inventories; it does not change a Kristal canon.

## Error handling

- If a recipe cannot be found, inspect `python arketype.py recipes`.
- If an archetype cannot be found, inspect `python arketype.py list`.
- If a destination already exists, choose a new slug or location.
- If the Authoring Kit rejects a workspace, investigate the reported `check` error; do not bypass validation.

**See also:** [Getting Started](Getting-Started) · [Validation and Testing](Validation-and-Testing)
