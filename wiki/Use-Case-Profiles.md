# Use-Case Profiles

Arketype includes **21 situated profiles**. Each links a primary archetype to optional supporting forms and a design-only assembly. Their examples below are fictitious and explain structure; they are not sample canonical domain records.

| Profile | Usage · domain | Primary archetype | Assembly |
| --- | --- | --- | --- |
| `troubleshooting-systeme` — System Troubleshooting | diagnosis · technology | `diagnostic-causal` | `troubleshooting-systeme` |
| `environnement-protocolaire` — Procedural Environment | procedures · cross-domain | `procedure-protocole` | `environnement-protocolaire` |
| `taxonomie-nature` — Nature Taxonomy | knowledge · natural-world | `taxonomie-classification` | `taxonomie-nature` |
| `etat-de-systemes` — System-State Tracking | monitoring · technology | `etat-systemes` | `etat-de-systemes` |
| `suivi-employe` — Employee Follow-Up | case-management · workplace | `dossier-suivi` | `suivi-employe` |
| `campus-federe` — Federated University / Campus | learning · education | `federation-topologie` | `uckk-campus` |
| `publication-moodle` — Moodle Learning Publication | integration · education | `parcours-pedagogique` | `parcours-moodle` |
| `collection-traditions` — Traditions and Mythology Collection | knowledge · culture | `compilation-collection` | `collection-traditions` |
| `organisations-sociales` — Contextual Social Organizations | modeling · social-systems | `modele-multiplexe` | `organisations-contextuelles` |
| `navigation-preuves-longues` — Long-Proof Landmarks and Junctions | research · mathematics | `carte-jalons-preuves` | `carte-preuves-longues` |
| `recherche-mathematique` — Mathematical Research Frontier | research · mathematics | `memoire-recherche` | `recherche-mathematique` |
| `dossier-scolaire` — Individual School Follow-Up | case-management · education | `dossier-suivi` | `dossier-scolaire` |
| `dossier-medical` — Individual Medical Follow-Up | case-management · health | `dossier-suivi` | `dossier-medical` |
| `dossier-civique` — Civic / Administrative Individual Casefile | case-management · civic | `dossier-suivi` | `dossier-civique` |
| `diagnostic-vehicule` — Vehicle Fault Diagnosis | diagnosis · automotive | `diagnostic-causal` | `diagnostic-vehicule` |
| `operations-police` — Police Operations Protocols | procedures · public-safety | `procedure-protocole` | `operations-protocoles` |
| `operations-hopital` — Hospital Operations Protocols | procedures · health | `procedure-protocole` | `operations-protocoles` |
| `orchestration-medicale` — Medical Knowledge Orchestration | orchestration · health | `composition-hybride` | `medi-connaissances` |
| `cartographie-scolaire` — School System and Rules Mapping | modeling · education | `modele-multiplexe` | `systeme-scolaire` |
| `referentiel-polyusage` — Multi-Purpose Semantic Reference | knowledge · cross-domain | `referentiel-semantique` | `ekole-multiusage` |
| `temoignages-enquete` — Attributed Testimony and Inquiry | evidence · civic | `deposition-temoignage` | `dossier-depositions` |

## System Troubleshooting

**Example scenario:** Service outage investigation.

An operator logs a service outage and preserves dated observations. The diagnosis model proposes competing failure explanations; a state matrix records component availability and versions; a separate timeline captures what happened and when.

```text
[Issue: service unavailable] → [Symptoms] → [Competing causes] → [Tests]
                         ↘ [Observed system state]
                         ↘ [Incident timeline]
```

**Primary archetype:** `diagnostic-causal`. **Supporting:** `registre-evenementiel`, `etat-systemes`, `composition-hybride`.

**Possible inputs:** symptoms, event logs, observed states, test results.

**Candidate outputs:** candidate causes, discriminating tests, recommended actions.

**Integrity requirement:** Record observed results and uncertainty explicitly. An unconfirmed hypothesis remains unconfirmed even if it appears in a prominent diagram.

**Composition recipe:** `assemblages/troubleshooting-systeme.json`.

## Procedural Environment

**Example scenario:** Facility handover procedure.

Document a procedure that names prerequisites, authorized roles, branching conditions and exception paths. The event ledger can later record observed execution; a simulation can illustrate training scenarios.

```text
[Preconditions] → [Check] → {Pass?} ─yes→ [Next step]
                          └no→ [Exception / escalation]
                          [Execution log kept separately]
```

**Primary archetype:** `procedure-protocole`. **Supporting:** `registre-evenementiel`, `simulation-transition`.

**Possible inputs:** steps, roles, preconditions, exceptions.

**Candidate outputs:** structured procedure, execution checklist, control points.

**Integrity requirement:** A documented branch does not grant authorization to take that action. Operational safeguards remain external to this archetype.

**Composition recipe:** `assemblages/environnement-protocolaire.json`.

## Nature Taxonomy

**Example scenario:** Cataloguing a nature collection.

A collector organizes observational categories and related names. The taxonomy tree defines the classification scheme, while a semantic reference holds definitions, synonyms and source citations.

```text
                       [Natural category]
                        /           \
                   [Group A]    [Group B]
                     |             |
                 [Subgroup]    [Specimen]
```

**Primary archetype:** `taxonomie-classification`. **Supporting:** `referentiel-semantique`.

**Possible inputs:** names, classification rules, synonyms, sources.

**Candidate outputs:** taxonomic tree, glossary, class reference.

**Integrity requirement:** An observed specimen, a classification claim, and a nomenclature source are separate kinds of evidence.

**Composition recipe:** `assemblages/taxonomie-nature.json`.

## System-State Tracking

**Example scenario:** Tracking several workstations.

An inventory tracks system identity and observed condition across several dimensions. The associated event ledger can explain the sequence of changes without being substituted for the latest snapshot.

```text
                  availability | version | last observed
    workstation A       up       | v1.2    | date A
    workstation B       down     | v1.1    | date B
```

**Primary archetype:** `etat-systemes`. **Supporting:** `registre-evenementiel`.

**Possible inputs:** systems, metrics, timestamps, versions.

**Candidate outputs:** state matrix, deviations, follow-up items.

**Integrity requirement:** Do not equate desired configuration, current measurement, and interpreted health status.

**Composition recipe:** `assemblages/etat-de-systemes.json`.

## Employee Follow-Up

**Example scenario:** Sensitive follow-up dossier.

A restricted record may track meetings, agreed actions, supporting documents and later reviews. Statements and allegations can be referenced with their own provenance and assessed separately.

```text
[Case file] → [Meeting notes]
            → [Actions and review dates]
            → [Supporting documents]
            → [Referenced statements]
```

**Primary archetype:** `dossier-suivi`. **Supporting:** `registre-evenementiel`, `deposition-temoignage`.

**Possible inputs:** meetings, notes, documents, actions.

**Candidate outputs:** case dossier, timeline, summaries.

**Integrity requirement:** This model is not an HR application. No real personal data belongs in the public template; permissions and retention must be enforceable outside the descriptive model.

**Composition recipe:** `assemblages/suivi-employe.json`.

## Specialized profiles and scope requirements

The profiles above have machine-readable evidence questions (`coverage_checks`), candidate inclusions/exclusions (`scope_guidance`), and application integration targets. None is prequalified. Examples backed by the supplied user archives are listed in `inventaires/cas-reels-usage.json`; they are not imported into the library. Full discussion is in [Use Cases and Scope](Use-Cases-and-Scope).

## Using the profiles

Preview one: `python arketype.py profile troubleshooting-systeme`. Create an instance only if its primary archetype fits your own domain needs; the recipe does not automatically instantiate all supporting states or resolve their ownership.

**See also:** [Composition Recipes](Composition-Recipes) · [Archetype Catalog](Archetype-Catalog) · [Security and Boundaries](Security-and-Boundaries).
