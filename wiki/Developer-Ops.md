# Developer Ops

The desktop **Developer Ops** screen provides a supervised command palette and a console transcript. It runs fixed local actions only. `arketype_launcher_ops.py` parses every command against an explicit allowlist and invokes the existing CLI using subprocess argument arrays (`shell=False`). Unknown commands, `python -c`, `rm`, `curl`, publishing and activation are rejected.

| Command | Operation | Writes library files? |
| --- | --- | --- |
| `help`, `status` | Show help or local catalogue counts | No |
| `list`, `search WORDS`, `show SLUG` | Explore archetypes | No |
| `profiles`, `profile SLUG` | Explore use-case profiles | No |
| `recipes`, `recipe ID` | Explore composition proposals | No |
| `validate`, `validate --check-kit` | Validate catalogue and optionally all Local Kit templates | No |
| `test` | Run the Python unit test suite (may create temporary test workspaces) | No intended changes to shipped library |
| `inventory` | Verify recorded local file hashes | No |
| `build-html` | Rebuild the local visual HTML from JSON | **Yes, local HTML only** |
| `open-catalogue` | Open the local HTML in the default browser | No |
| `compat` | Read-only local metadata/declared-version inspection for selected ecosystem sources, including optional Framework v11 and diK | No |
| `clear` | Clear the console transcript | No |

The long-running processes run in background threads; GUI updates remain on the main thread. The **Create Kristal** form is the designated operation for creating a workspace, including preview and explicit confirmation.

## Not a shell or deployment service

Developer Ops deliberately does not run arbitrary commands, execute downloaded scripts, access connected services, modify a remote repository, certify factual claims, or publish/activate Kristals.

**Next:** [Desktop Launcher](Desktop-Launcher) · [CLI Reference](CLI-Reference) · [Security and Boundaries](Security-and-Boundaries)

## v1.6 semantic ecosystem note

Developer Ops compatibility inspection is **metadata-only** and never independently certifies Framework v11 schemas, the external Kit, Wikidata, or a diK project. The optional `semantic-status` and `dik-coverage` CLI operations are documented under [[Semantic-Authoring-v11]] and [[diK-and-Dictionaries]]; diK execution requires an explicitly chosen local source tree; **1.0.0-alpha.7** is the documented baseline. Kit 4.0.0-draft.3 catalog selection and recovery are commands in the workspace-local Kit, not commands offered through Developer Ops. See [[diK-Catalog-Exchange-v11]].
