# Archetype Catalog

The table below lists **all 19 structural archetypes** shipped in Arketype 1.6.0 (the same historical archetype set initially published with 1.2.2). English names here are explanatory; the original JSON identifiers and stable slugs remain unchanged. A primary visual pattern is a *reader convention*, not a complete constraint on native data.

| ID | English archetype | Stable slug | Primary visual pattern | Typical uses |
| --- | --- | --- | --- | --- |
| **ARK-01** | **Semantic Reference** | `referentiel-semantique` | Cluster | Reusable knowledge stores, dictionaries, educational and cultural references |
| **ARK-02** | **Federation / Topology** | `federation-topologie` | Network | Distributed campuses, organizational units and linked subsystems |
| **ARK-03** | **Milestone and Proof Map** | `carte-jalons-preuves` | Hub / satellites | Progress maps, mathematical roadmaps and cross-theory docking points |
| **ARK-04** | **Procedure / Protocol** | `procedure-protocole` | Branching | SOPs, institutional protocols and checklists |
| **ARK-05** | **Compilation / Collection** | `compilation-collection` | Cluster | Cookbooks, reference collections and anthologies |
| **ARK-06** | **Research Memory** | `memoire-recherche` | Timeline | Research notebooks, inquiry histories and lab studies |
| **ARK-07** | **Invariant / Formal Theory** | `invariant-theorie` | Tree | Theorem systems, invariant specifications and formal studies |
| **ARK-08** | **Causal Diagnosis** | `diagnostic-causal` | Hub / satellites | System troubleshooting, vehicle diagnosis and fault isolation |
| **ARK-09** | **Multiplex / Organizational Model** | `modele-multiplexe` | Multilayer | Organizational studies and social or institutional mappings |
| **ARK-10** | **Learning Path** | `parcours-pedagogique` | Linear | Curricula and personalized learning journeys |
| **ARK-11** | **Event Ledger / Chronology** | `registre-evenementiel` | Timeline | Incident logs, history, audit trails and case timelines |
| **ARK-12** | **Layered Interpretations** | `interpretations-couches` | Multilayer | Comparative analysis and alternative interpretations |
| **ARK-13** | **Media and Creative Universes** | `univers-oeuvres-medias` | Cluster | Worldbuilding, archives and media continuity |
| **ARK-14** | **Simulation / Transitions** | `simulation-transition` | Linear | Simulation, state machines and training situations |
| **ARK-15** | **Hybrid Composition** | `composition-hybride` | Network | Cross-system models and multi-part applications |
| **ARK-16** | **Testimony / Deposition** | `deposition-temoignage` | Casefile | Witness records and declarative evidence dossiers |
| **ARK-17** | **Taxonomy / Natural Classification** | `taxonomie-classification` | Tree | Nature maps, biological categories and material typologies |
| **ARK-18** | **System-State Matrix** | `etat-systemes` | Matrix | Infrastructure status, asset state and configuration review |
| **ARK-19** | **Casefile / Follow-Up** | `dossier-suivi` | Casefile | Employee follow-up, case management and tracked interventions |

## Choosing by the structural question

- **What must happen next?** Choose a procedure (`procedure-protocole`) or learning path (`parcours-pedagogique`).
- **How do the parts relate?** Choose a federation (`federation-topologie`), organizational layers (`modele-multiplexe`) or hybrid composition.
- **What belongs to which class?** Choose taxonomy (`taxonomie-classification`), possibly with a semantic reference.
- **What happened when?** Choose an event ledger (`registre-evenementiel`).
- **What is the current condition of each system?** Choose a system-state matrix (`etat-systemes`).
- **What is claimed, observed or supported?** Choose testimony, research memory, proof map or causal diagnosis as the relevant epistemic role demands.
- **What material and actions belong to this case?** Choose a casefile (`dossier-suivi`).

## Individual design notes

### ARK-01 — Semantic Reference

**Structure:** Connected concepts, entities and sourced relationships.

**When to use:** Reusable knowledge stores, dictionaries, educational and cultural references.

**Integrity boundary:** Distinguish assertions from instructional projections and record sources.

**Suggested primitives:** `referents`, `types`, `relations_typees`, `assertions_contextualisees`, `sources`, `provenance`.

**Template:** `modeles/referentiel-semantique/` · **Source:** `archetypes/referentiel-semantique.json`

### ARK-02 — Federation / Topology

**Structure:** Hierarchy or network of separately identifiable knowledge states.

**When to use:** Distributed campuses, organizational units and linked subsystems.

**Integrity boundary:** A parent reference does not own or absorb a child state.

**Suggested primitives:** `noeuds`, `liens_parent_enfant`, `scopes`, `references_epinglees`, `statuts_de_cristallisation`.

**Template:** `modeles/federation-topologie/` · **Source:** `archetypes/federation-topologie.json`

### ARK-03 — Milestone and Proof Map

**Structure:** Sparse milestones, branches and pointers to proofs held elsewhere.

**When to use:** Progress maps, mathematical roadmaps and cross-theory docking points.

**Integrity boundary:** A shortcut edge does not constitute proof; pin exact proof references.

**Suggested primitives:** `carrefours`, `points_terminaux`, `frontieres_atteintes`, `arcs_resume`, `references_de_preuve`, `points_arrimage`, `obligations_ouvertes`.

**Template:** `modeles/carte-jalons-preuves/` · **Source:** `archetypes/carte-jalons-preuves.json`

### ARK-04 — Procedure / Protocol

**Structure:** Ordered and conditional steps, roles, prerequisites and exceptions.

**When to use:** SOPs, institutional protocols and checklists.

**Integrity boundary:** Description, execution and authorization are different.

**Suggested primitives:** `conditions_entree`, `etapes`, `transitions`, `branches`, `roles`, `ressources`, `issues`.

**Template:** `modeles/procedure-protocole/` · **Source:** `archetypes/procedure-protocole.json`

### ARK-05 — Compilation / Collection

**Structure:** Curated, ordered and annotated independent works or knowledge items.

**When to use:** Cookbooks, reference collections and anthologies.

**Integrity boundary:** Curation does not imply ownership of every included item.

**Suggested primitives:** `entrees`, `references`, `ordre`, `criteres_selection`, `variantes`, `annotations`, `provenance`.

**Template:** `modeles/compilation-collection/` · **Source:** `archetypes/compilation-collection.json`

### ARK-06 — Research Memory

**Structure:** Hypotheses, observations, trials and findings over time.

**When to use:** Research notebooks, inquiry histories and lab studies.

**Integrity boundary:** Preserve the difference between hypotheses and established findings.

**Suggested primitives:** `connaissances`, `hypotheses`, `tentatives`, `obligations`, `resultats`, `strategies`, `promotions`.

**Template:** `modeles/memoire-recherche/` · **Source:** `archetypes/memoire-recherche.json`

### ARK-07 — Invariant / Formal Theory

**Structure:** Formal definitions, rules and logical dependencies.

**When to use:** Theorem systems, invariant specifications and formal studies.

**Integrity boundary:** Proof obligations need real justification and scope.

**Suggested primitives:** `invariants`, `morphes_equivalents`, `consequences`, `contre_exemples`, `preuves`, `certificats`, `tests`.

**Template:** `modeles/invariant-theorie/` · **Source:** `archetypes/invariant-theorie.json`

### ARK-08 — Causal Diagnosis

**Structure:** Symptoms, possible causes, test results and competing explanations.

**When to use:** System troubleshooting, vehicle diagnosis and fault isolation.

**Integrity boundary:** Inferences are not permissions to perform interventions.

**Suggested primitives:** `topologie`, `etats_operatoires`, `perturbations`, `observations`, `hypotheses`, `tests`, `inference_derivee`.

**Template:** `modeles/diagnostic-causal/` · **Source:** `archetypes/diagnostic-causal.json`

### ARK-09 — Multiplex / Organizational Model

**Structure:** Several relationship layers over shared entities.

**When to use:** Organizational studies and social or institutional mappings.

**Integrity boundary:** Avoid collapsing relationships from different layers.

**Suggested primitives:** `entites`, `couches_relationnelles`, `roles`, `ressources`, `regles`, `temps`, `points_de_vue`.

**Template:** `modeles/modele-multiplexe/` · **Source:** `archetypes/modele-multiplexe.json`

### ARK-10 — Learning Path

**Structure:** Sequenced objectives, prerequisites and activities.

**When to use:** Curricula and personalized learning journeys.

**Integrity boundary:** Learning projection is not the whole knowledge base.

**Suggested primitives:** `objectifs`, `dependances`, `sequences`, `activites`, `criteres_evaluation`, `references_savoir`.

**Template:** `modeles/parcours-pedagogique/` · **Source:** `archetypes/parcours-pedagogique.json`

### ARK-11 — Event Ledger / Chronology

**Structure:** Dated observations, events and revisions.

**When to use:** Incident logs, history, audit trails and case timelines.

**Integrity boundary:** An event log is not necessarily current state or causal proof.

**Suggested primitives:** `evenements`, `acteurs`, `horodatages`, `validites`, `liens_causaux_hypotheses`, `versions`.

**Template:** `modeles/registre-evenementiel/` · **Source:** `archetypes/registre-evenementiel.json`

### ARK-12 — Layered Interpretations

**Structure:** Separate derived readings of shared underlying material.

**When to use:** Comparative analysis and alternative interpretations.

**Integrity boundary:** Keep interpretation and reproducible source distinct.

**Suggested primitives:** `donnees`, `transformations`, `couches_interpretatives`, `liens_typés`, `hypotheses`, `limites`.

**Template:** `modeles/interpretations-couches/` · **Source:** `archetypes/interpretations-couches.json`

### ARK-13 — Media and Creative Universes

**Structure:** Linked works, settings, characters and media manifestations.

**When to use:** Worldbuilding, archives and media continuity.

**Integrity boundary:** Preserve provenance and distinction between work and interpretation.

**Suggested primitives:** `univers`, `oeuvres`, `evenements`, `manifestations`, `alias`, `sources`, `restrictions_de_lecture`.

**Template:** `modeles/univers-oeuvres-medias/` · **Source:** `archetypes/univers-oeuvres-medias.json`

### ARK-14 — Simulation / Transitions

**Structure:** State-transition definitions and hypothetical scenarios.

**When to use:** Simulation, state machines and training situations.

**Integrity boundary:** Simulation does not grant real-world execution authority.

**Suggested primitives:** `etats`, `transitions`, `contraintes`, `variables`, `scenario`, `resultats_derived`.

**Template:** `modeles/simulation-transition/` · **Source:** `archetypes/simulation-transition.json`

### ARK-15 — Hybrid Composition

**Structure:** An assemblage of several kinds of independent knowledge structure.

**When to use:** Cross-system models and multi-part applications.

**Integrity boundary:** Do not merge semantic owners or treat application logic as canon.

**Suggested primitives:** `sous_modeles`, `frontieres`, `contrats_interface`, `references`, `politiques`, `projections`.

**Template:** `modeles/composition-hybride/` · **Source:** `archetypes/composition-hybride.json`

### ARK-16 — Testimony / Deposition

**Structure:** Attributed accounts with recordings, transcriptions and revisions.

**When to use:** Witness records and declarative evidence dossiers.

**Integrity boundary:** Reported claims are not automatically verified facts.

**Suggested primitives:** `declarants_et_pseudonymes`, `seances_et_intervenants`, `questions_reponses`, `enonces_attribues`, `dates_des_faits_allegues`, `dates_de_recueil`, `supports_originaux`.

**Template:** `modeles/deposition-temoignage/` · **Source:** `archetypes/deposition-temoignage.json`

### ARK-17 — Taxonomy / Natural Classification

**Structure:** Classification tree with groups, subclasses and synonyms.

**When to use:** Nature maps, biological categories and material typologies.

**Integrity boundary:** Classification criteria, authority and exceptions must be explicit.

**Suggested primitives:** `racines`, `groupes`, `classes`, `sous_classes`, `specimens`, `relations_de_classement`, `synonymes`.

**Template:** `modeles/taxonomie-classification/` · **Source:** `archetypes/taxonomie-classification.json`

### ARK-18 — System-State Matrix

**Structure:** Observed condition of multiple systems across dimensions.

**When to use:** Infrastructure status, asset state and configuration review.

**Integrity boundary:** Observed, desired and inferred states must remain separate.

**Suggested primitives:** `systemes`, `composants`, `dimensions_d_etat`, `valeurs`, `dates_d_observation`, `statuts`, `ecarts`.

**Template:** `modeles/etat-systemes/` · **Source:** `archetypes/etat-systemes.json`

### ARK-19 — Casefile / Follow-Up

**Structure:** Central record of documents, notes, actions and follow-ups.

**When to use:** Employee follow-up, case management and tracked interventions.

**Integrity boundary:** Sensitive assessments and decisions require explicit governance.

**Suggested primitives:** `dossiers`, `pieces`, `notes`, `actions`, `jalons`, `evaluations`, `restrictions_d_acces`.

**Template:** `modeles/dossier-suivi/` · **Source:** `archetypes/dossier-suivi.json`

## What an archetype does not guarantee

Every archetype is a candidate design. The local template has zero committed domain knowledge by default. A valid production Kristal still needs domain-specific source integrity, validation, logical contracts, lifecycle rules, and (when applicable) access controls.

**See also:** [Visual Grammar](Visual-Grammar) · [Use-Case Profiles](Use-Case-Profiles) · [Working with Templates](Working-with-Templates).
