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
| `clear` | Clear the console transcript | No |

The long-running processes run in background threads; GUI updates remain on the main thread. The **Create Kristal** form is the designated operation for creating a workspace, including preview and explicit confirmation.

## Not a shell or deployment service

Developer Ops deliberately does not run arbitrary commands, execute downloaded scripts, access connected services, modify a remote repository, certify factual claims, or publish/activate Kristals.

**Next:** [Desktop Launcher](Desktop-Launcher) · [CLI Reference](CLI-Reference) · [Security and Boundaries](Security-and-Boundaries)
