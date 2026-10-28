# Ecosystem Compatibility

**Arketype 1.6.0 ecosystem baselines:** Framework **11.0.0-draft.4**, optional Authoring Kit **4.0.0-draft.3** for new v11 workspaces, and separately supplied **diK 1.0.0-alpha.7** for an explicitly configured read-only coverage report. Historical templates continue to use Kit **3.2.4**.

## What the desktop inspector does

The **Developer Ops → Ecosystem Compatibility** view is a local, metadata-only inspector. It can inspect paths to Framework, Authoring Kit, a Kristal workspace, Manager, Bootstrap and optional diK source metadata. Leaving a path blank means **NOT CONFIGURED**, never a successful qualification.

Checks include:

- Declared Framework release/version pins and presence of selected contract metadata (not the complete normative TCK).
- Bundled Kit versions and fingerprints, and limited comparisons with a selected local installation.
- Workspace identity and `state_ref` separation for the 19 historical neutral templates.
- Presence of selected local integration modules and metadata, **not** runtime readiness or access rights.

In Developer Ops, use `compat` (optionally `--framework PATH --kit PATH --workspace PATH --manager PATH --bootstrap PATH`; consult the installed console `help`). This is an allowlisted **local** inspection, not a shell or a remote GitHub test.

## What it does not do

A matching version/hash checks local bytes or declarations only; it does **not** prove Framework conformance, a valid domain graph, an approved crosswalk, a real Wikidata import, synchronization, publication or activation. Hosted GitHub access controls and public/private visibility are outside this metadata check.

To author a new graph, use [[Semantic-Authoring-v11]]. To get actual coverage from a selected diK checkout, use [[diK-and-Dictionaries]]. For the **separate Kit draft.3 catalog workflow**, use [[diK-Catalog-Exchange-v11]].
