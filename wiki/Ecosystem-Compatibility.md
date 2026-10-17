# Ecosystem Compatibility

Arketype 1.4.0 adds an **Ecosystem Compatibility** tab inside the desktop **Developer Ops** screen. It provides **read-only local file inspection**, not a remote GitHub health report or a certification.

Choose zero or more paths to local checkouts of **Framework**, **Authoring Kit**, **Kristal workspace**, **Manager**, and **Bootstrap**, then click **Inspect local compatibility**. Leaving a path blank is safe: it means **NOT CONFIGURED**, not a passed test.

## What is actually inspected

- Arketype's bundled Authoring Kit version and SHA-256; if an external Kit is selected, whether its `tools/kristal.py` is byte-identical.
- Selected Framework `contracts/release.json`, `contracts/contract-set.json`, and presence of the `v10-compatibility-lock.json`, without running its Test Conformance Kit or qualifying the normative contract-set.
- The metadata status, v10 target and distinct identities of the 19 neutral templates.
- Only descriptor metadata of a selected local workspace, never the bodies of registered canonical artifacts.
- The local existence of expected Manager/Bootstrap source modules; presence does **not** mean runtime, sync or publication works.

CLI users can enter `compat` in Developer Ops, optionally followed by `--framework PATH --kit PATH --workspace PATH --manager PATH --bootstrap PATH`. No shell or arbitrary commands are accepted.

For architecture and governance boundaries, see [Ecosystem Alignment](../docs/ECOSYSTEM_ALIGNMENT.md). The existing [Security and Boundaries](Security-and-Boundaries) chapter remains applicable.

## Important limitations

- A matching version is not Framework conformance.
- A matching hash proves only identical local file bytes.
- A successful local template test does not qualify an external Kristal.
- `C1`, `C2`, `C3`, GitHub host access, real collection indices, public/private visibility, immutable publication and activation are **not checked**.
- Konstellation, not Arketype, is responsible for exploring real Kristal instances and their concepts.

## Mise à jour 1.6.0

Le mode `--authoring v11` utilise maintenant Authoring Kit `4.0.0-draft.3` épinglé par empreintes, Framework `11.0.0-draft.4` est la référence de conception, et diK `1.0.0-alpha.7` reste sélectionnable depuis une copie locale pour la couverture en lecture seule. Les identités v9 historiques et les opérations de publication demeurent inchangées. Les inspections par versions et empreintes ne sont **pas** une qualification normative.
