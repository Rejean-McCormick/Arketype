# Frequently Asked Questions
**v1.6.0:** Arketype optionally creates an *empty* v11-ready Kit **4.0.0-draft.3** workspace (`create --authoring v11`) and can request a read-only coverage report from an explicitly selected local **diK alpha.7** checkout. Framework draft.4 is the current design baseline. None of these steps automatically migrates legacy text, allocates KQ/QIDs, activates a graph or certifies Framework conformance. See [[Semantic-Authoring-v11]], [[diK-and-Dictionaries]] and [[diK-Catalog-Exchange-v11]].


## Is Arketype a replacement for the Kristal Framework?

No. Arketype is a non-normative library of candidate structures and empty workspace templates. It reuses the bundled Authoring Kit and makes no new Framework-level contract.

## Can I use a single archetype for more than one purpose?

Yes. A semantic reference may support teaching, research, museums or personal study. A casefile may support many properly governed forms of follow-up. Profiles capture the situation; archetypes capture the fundamental structure.

## Does one archetype always correspond to one diagram pattern?

No. Each has a dominant reading motif and may also have secondary patterns. A knowledge graph can be rendered as a tree for one task, but the diagram must not silently discard native relationships.

## Can a composition recipe automatically merge Kristals?

No. Recipe links remain unresolved design proposals. Owners, exact references, contracts and any permitted semantic transfer have to be specified separately.

## Does `check` guarantee that a diagnosis or testimony is correct?

No. It checks local technical structure. A recorded testimony must remain an attributed report unless separately evaluated; a diagnostic hypothesis is not a confirmed cause.

## Is the HTML catalogue live?

No. It is an offline generated projection. Run `python arketype.py build-html` after changing JSON inventories.

## Is the GitHub Wiki published by copying the repository ZIP?

No. The `wiki/` directory is ready-to-publish Markdown; GitHub Wikis are separate repositories. Follow [Publishing the Wiki](Publishing-the-Wiki).

## Where is the logo?

The user-supplied SVG is preserved in the **Arketype 1.6.0** distribution at `assets/logo-k.svg`, with a derived PNG for the Windows launcher. This Wiki also carries an unchanged copy as `assets/logo-k.svg`. The main application README intentionally does not embed the logo.

## Can I store real employee dossiers or testimony in the included templates?

Do not put private records in the public library templates. A production workflow must first implement access restrictions, lawful collection basis where relevant, retention, audit, identity controls and appropriate governance.
