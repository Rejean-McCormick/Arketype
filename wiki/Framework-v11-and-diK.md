# Framework v11 and diK integration

Arketype 1.6.0 retains its **design-only** role. A semantic entity is identified by `KQ` in its namespace, while a property is `KP`. `KA` statements and `KS` source identities are distinct. Wikidata Q/P remain **external** mappings in a reviewed crosswalk. Dictionary words and translated labels are **not** identities in Framework v11 canonical graphs.

Use `python arketype.py create --type referentiel-semantique --slug my-kristal --title 'My Kristal' --parent . --authoring v11` to create a **new empty** local Kit4 workspace with a readiness guide; no fake KQ IDs are issued and strict v11 stays disabled until registration of real graph, identity registry, crosswalk and lexical catalog. The 19 old templates remain valid unchanged in legacy mode.

Use `python arketype.py semantic-status --path /path/to/my-kristal` for **metadata-only** readout. Use `python arketype.py dik-coverage --dik-root /trusted/diK-v1.0.0-alpha.7 --project /path/to/dik.project.json --locales fr,en,fr-CA` for **read-only** actual diK lexical completeness, subject to actual named local files. A missing translation is not guessed; a French fallback is not a direct French-Canadian translation.

Migration of historical textual identities requires a scoped, independently reviewed plan and execution by an authorized Authoring Kit producer. It never replaces quotes or changes committed source history. No action above publishes, activates or qualifies a Kristal.

See [Ecosystem Compatibility](Ecosystem-Compatibility.md) and `docs/14_FRAMEWORK_V11_ET_DIK.md` in the main repository for contract details.

## Arketype 1.6.0 : limites de l'interopérabilité

- **Framework** `11.0.0-draft.4` est la référence; aucun schéma normatif n'est modifié par Arketype.
- **Authoring Kit** `4.0.0-draft.3` est sélectionné uniquement par le mode `--authoring v11`; les 19 stubs historiques gardent la version `3.2.4`.
- **diK** `1.0.0-alpha.7` demeure une source externe explicitement choisie pour les rapports de couverture en lecture seule. Les corrections de dictionnaire, l'import massif et les plans de migration restent dans diK et l'Authoring Kit.

Une conformité réelle exige de tester les dépôts exacts ensemble; un résultat `vendored_source_verified` garantit les octets copiés du Kit, pas un certificat complet.
