# Bundled Authoring Kit v4.0.0-draft.3 (opt-in)

Exact selective vendoring of `tools/kristal.py`, `tools/kristal_v11_core.py`, and
all `templates/` files from the supplied Authoring Kit **4.0.0-draft.3** ZIP.
`VENDOR_PIN.json` records their SHA-256 and original sizes.

`--authoring v11` uses these copies to create a **new blank workspace**. It never
mint KQ/KP/KA/KS, claim Q/P equivalences, insert a lexical dictionary, publish,
or activate the workspace. The 19 historical templates still use bundled Kit 3.2.4.

The design baseline is Framework **11.0.0-draft.4**. Its v11 schemas are reported
unchanged from draft.3, but this is not an independent, full cross-repository
TCK qualification. External diK alpha.7 is not bundled or executed implicitly.
