# Composition Recipes

The library contains **14 noncanonical composition recipes** under `assemblages/`. They describe how multiple archetype responsibilities **might** be related. They do not implement cross-state merging, data transport, validation, activation or publication.

| Recipe ID | English scenario | Primary archetype | Proposed supporting archetypes |
| --- | --- | --- | --- |
| `atlas-preuves` | Sparse proof atlas | `carte-jalons-preuves` | `invariant-theorie`, `memoire-recherche` |
| `diagnostic-vehicule` | Vehicle diagnostics | `diagnostic-causal` | `modele-multiplexe`, `simulation-transition` |
| `dossier-depositions` | Testimony dossier | `deposition-temoignage` | `registre-evenementiel`, `interpretations-couches`, `carte-jalons-preuves` |
| `ekole-multiusage` | Ekole multipurpose reference | `referentiel-semantique` | `modele-multiplexe`, `parcours-pedagogique` |
| `environnement-protocolaire` | Procedural environment | `procedure-protocole` | `registre-evenementiel`, `simulation-transition` |
| `etat-de-systemes` | System-state tracking | `etat-systemes` | `registre-evenementiel` |
| `livre-recettes` | Cookbook compilation | `compilation-collection` | `procedure-protocole` |
| `medi-connaissances` | MediKristal knowledge component | `composition-hybride` | `referentiel-semantique`, `procedure-protocole`, `diagnostic-causal` |
| `operations-protocoles` | PoliceOps / HospitalOps protocols | `procedure-protocole` | `registre-evenementiel`, `simulation-transition` |
| `suivi-employe` | Employee follow-up | `dossier-suivi` | `registre-evenementiel`, `deposition-temoignage` |
| `taxonomie-nature` | Nature taxonomy | `taxonomie-classification` | `referentiel-semantique` |
| `troubleshooting-systeme` | System troubleshooting | `diagnostic-causal` | `registre-evenementiel`, `etat-systemes`, `composition-hybride` |
| `uckk-campus` | UCKK campus federation | `federation-topologie` | `parcours-pedagogique` |
| `univers-medias` | Media universe | `univers-oeuvres-medias` | `compilation-collection`, `registre-evenementiel` |

## Rules that apply to every composition

1. **Primary responsibility first:** identify the owner of each kind of knowledge.
2. **References remain references:** do not copy or absorb an independent state merely because it is linked.
3. **Contract status is unresolved:** every declared component relation in these recipes is design-only and needs a real domain contract before implementation.
4. **Pin the source:** when one state relies on another, specify its exact source identity and appropriate commitment/provenance information.
5. **Preserve epistemic status:** logs, observations, statements, conclusions, hypotheses and proof references are not interchangeable.
6. **No publication authority:** every recipe has `publication_authorization: false`.

## Preview or instantiate a primary workspace

```bash
python arketype.py recipe troubleshooting-systeme
python arketype.py compose --recipe troubleshooting-systeme --slug diag-plan --title "Diagnostic Plan" --parent . --dry-run
```

Remove `--dry-run` only when you want Arketype to create a *single* new local primary workspace with a design plan. It does not instantiate every referenced supporting component.

## An important example: MediKristal

The `medi-connaissances` recipe represents **the knowledge-oriented Kristal portion** of a larger MediKristal environment. It must not be read as a claim that the entire application, its workflows, permissions and business logic can be turned into one canonical Kristal. The descriptive recipe preserves those architectural boundaries.

**See also:** [Architecture](Architecture) · [Use-Case Profiles](Use-Case-Profiles) · [Security and Boundaries](Security-and-Boundaries).
