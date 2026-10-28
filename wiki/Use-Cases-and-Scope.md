# Use Cases, Scope and Coverage

Arketype 1.6.0 continues to treat the **structure**, **usage**, **domain**, **integration** and **authority/data constraints** of a Kristal as independent dimensions. A profile expresses design expectations, not proof of realized capabilities.

- The 19 archetypes describe possible native structures. They are not domain standards.
- The 21 profiles describe intended activities, expected inputs, outputs and review questions.
- The 23 recipes suggest noncanonical assembly relationships with unresolved semantic owners and references.
- Scope guidance is a *draft* reviewed by an owner before any Kristal workspace mutation.

## Local CLI

```bash
python arketype.py uses
python arketype.py recognize --path /path/to/UCKK.zip
python arketype.py recognize --path /path/to/multi-projects.zip --focus A-Kristal-VehiculeDiag
python arketype.py scope-guide --profile navigation-preuves-longues
python arketype.py create --profile dossier-scolaire --slug school-demo --title "School demo" --parent . --dry-run
```

These commands never import content, publish, activate, or inject a scope. A complete scan of a Kristal and authorized injection belong to a separate application such as Skope. Arketype only supplies typed profile proposals and scope design guidance.

## Distinct responsibilities

- **UCKK**: institution/pathways/courses are referenced states; Moodle needs a separate adapter and approval.
- **Traditions**: attribution and cultural context are essential; comparison cannot equate beliefs.
- **Math proof maps**: endpoints and junctions are navigation metadata, not proof validation.
- **Individual dossiers**: observations, official findings and decisions are distinct; private content stays in secured applications.
- **MediKristal**: independent medical software is not itself one Kristal; no clinical clearance is implied.

Read `docs/12_USAGE_PROFILES_AND_SCOPES.md` and `docs/13_SKOPE_COMPATIBILITY.md` for typed details, candidate scope JSON and interoperability limits.
