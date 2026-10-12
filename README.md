# Arketype

**A visual archetype library for Kristal knowledge-state workspaces**  
**Release:** 1.4.0 · **Status:** local design library, non-normative

Arketype helps you explore, compare, and instantiate different structural forms of Kristals. It provides neutral workspace templates, documented archetypes, illustrative composition plans, a visual HTML catalogue, and local creation tools. Its diagrams explain *how a knowledge structure is organized*; they do not certify claims, establish domain standards, or authorize operational actions.

| Included | Count | What it means |
| --- | ---: | --- |
| Archetypes | **19** | Distinct structural starting points |
| Neutral workspaces | **19** | Empty local templates with separate `state_ref` identities |
| Composition recipes | **14** | Design-only ways to combine forms while preserving boundaries |
| Use-case profiles | **5** | Concrete scenarios such as troubleshooting, taxonomy and employee follow-up |
| Situated diagrams | **24** | Labeled illustrations, one per archetype and use-case profile |
| Visual patterns | **10** | A shared vocabulary: tree, network, matrix, timeline, casefile and others |

## Start here

1. Extract the repository archive, then **double-click `Lancer_Arketype.pyw`** on Windows (Python 3.10+ with Tkinter). It opens a unified desktop launcher with **Home**, **Catalogue**, **Create Kristal**, and **Developer Ops**. The Catalogue is searchable in the launcher; **Open full visual catalogue** opens the illustrated offline HTML view. Developer Ops includes an allowlisted local console and **Ecosystem Compatibility** read-only diagnostics for explicitly selected checkouts—never an arbitrary shell, remote sync, or publication.
2. You can also open **`catalogue/index.html`** directly without Python or Tkinter. It provides search, structural filters, labeled diagrams and links to JSON. Read the **[GitHub Wiki source](wiki/Home.md)** for concepts, detailed archetype descriptions, examples, composition rules, and safety boundaries.
3. Use Python 3.10+ to explore or instantiate a workspace from the repository root:

```bash
python arketype.py list
python arketype.py search "taxonomy"
python arketype.py profiles
python arketype.py profile troubleshooting-systeme
python arketype.py recipes
python arketype.py validate --check-kit
```

To **preview** a new local workspace without writing anything:

```bash
python arketype.py create --type taxonomie-classification \
  --slug nature-atlas --title "Nature Atlas" --parent . --dry-run
```

Remove `--dry-run` to create `./nature-atlas` with a new identity and an empty canon. The Windows **desktop launcher** is `Lancer_Arketype.pyw` (Python with Tkinter). The interface has been smoke-tested under a virtual Linux display; a native Windows machine test is still pending. The creation page previews before writing. Developer Ops runs on a background thread to keep the window responsive.

## The catalogue and its source data

The visual catalogue is a **generated projection**, not a live reader of committed Kristal states. Update its source inventories and regenerate it when needed:

```bash
python arketype.py build-html
```

| Location | Responsibility |
| --- | --- |
| `catalogue.json` | Catalogue index and archetype file references |
| `archetypes/*.json` | Individual archetype definitions and semantic boundaries |
| `inventaires/archetypes-visuels.json` | Visual properties of the 19 archetypes |
| `inventaires/grammaire-visuelle.json` | Ten standardized diagram patterns |
| `inventaires/diagrammes-situes.json` | Labeled, illustrative nodes and edges |
| `inventaires/profils-usage.json` | Five concrete use-case profiles |
| `assemblages/*.json` | Fourteen non-canonical composition proposals |
| `modeles/` | Neutral Authoring Kit workspaces; not populated domain datasets |
| `catalogue/index.html` | Offline HTML interface generated from JSON |
| `catalogue/Arketype_Visual_Catalogue_v1.4.0.pdf` | Included printable catalogue |
| `wiki/` | English GitHub Wiki pages, ready for a separate Wiki repository |
| `Lancer_Arketype.pyw` | Single Windows entrypoint for the desktop launcher |
| `arketype_gui.py` | Offline desktop UI: Home, Catalogue, Create Kristal, Developer Ops |
| `arketype_launcher_ops.py` | Tested allowlist for local console operations (no shell) |
| `arketype_ecosystem.py` | Read-only Framework / Kit / local workspace compatibility inspector |
| `docs/ECOSYSTEM_ALIGNMENT.md` | Inter-repository ownership boundaries and inspection limits |

The HTML and Windows interfaces use the visual branding color **`#1E6864`** and the supplied logo.

## Representative use cases

- **System troubleshooting:** causal diagnosis linked to observations, test results, and system-state snapshots.
- **Procedural environments:** branching protocols with roles, preconditions, exceptions, and separately recorded execution traces.
- **Nature taxonomy:** tree-based classifications with explicit criteria and sources.
- **System-state tracking:** a matrix of observed systems, indicators, and dated snapshots.
- **Employee follow-up:** a restricted casefile combining notes, actions, supporting documents, and timeline references.

The same foundation also supports UCKK-style federations, multi-use Ekole knowledge references, sparse proof maps, media universes, research memory, and testimony/deposition records.

## Important boundaries

**Archetypes are proposed designs, not official Kristal contracts.** Arketype does not replace Kristal Framework, the Authoring Kit, domain-specific validation, or operational applications. Its templates contain no committed domain assertions, and its composition recipes are expressly marked `design_only`.

- A recorded statement is not automatically a verified fact; a causal hypothesis is not an authorized remedy.
- System observation, desired configuration, computed status, and operational decision remain distinct.
- Employee, testimony, medical, and other sensitive records require a separate application with access control, retention rules, consent/legal basis where applicable, and audit protections. Do not put real sensitive data into the public templates.
- **Building is not qualifying, synchronizing, publishing, or activating.** `check` and `build-v9` validate local technical structure, not domain truth.

## Validate and extend

```bash
python -m unittest discover -s tests -v
python arketype.py validate --check-kit
```

The repository uses the included Kristal Authoring Kit **3.2.4** and refers to Kristal Framework **10.0.0-draft.3.1** (**draft**, not a qualified GitHub network). See [Getting Started](wiki/Getting-Started.md), [Architecture](wiki/Architecture.md), [CLI Reference](wiki/CLI-Reference.md), and [Security and Boundaries](wiki/Security-and-Boundaries.md) for the detailed workflow.

## GitHub Wiki publishing

The `wiki/` folder is **ready-to-publish Wiki content**, but GitHub stores a repository Wiki in a **separate Git repository**. Committing this folder to the main Arketype repository does **not** publish the Wiki automatically. Follow [Publishing the Wiki](wiki/Publishing-the-Wiki.md) after enabling the Wiki on the intended GitHub repository; no remote publication is performed by this archive.

## Ecosystem compatibility (read-only)

In the Windows launcher open **Developer Ops → Ecosystem Compatibility**. Choose optional local Framework, external Kit, workspace, Manager and Bootstrap checkout folders to inspect metadata and file hashes. Results explicitly differentiate **declared reference**, **identical bytes**, **not configured**, **review required** and **not verified**. The inspector does not run C1/C2/C3 or access GitHub, and cannot publish or activate a Kristal. See [Ecosystem Alignment](docs/ECOSYSTEM_ALIGNMENT.md) and [Wiki guide](wiki/Ecosystem-Compatibility.md).
