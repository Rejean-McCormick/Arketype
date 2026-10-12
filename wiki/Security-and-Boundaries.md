# Security, Privacy, and Semantic Boundaries

Arketype is a **design library**, not an operational storage or case-management service. Its neutral templates should remain free of real sensitive data.

## Records involving people

**Testimony / deposition** (`deposition-temoignage`) stores attributed statements and their provenance. The correct semantic form is “person X stated P,” not “P is established as true.” Original recordings, transcriptions, corrections, consent or other lawful collection basis, access restrictions, and evaluations should be distinguishable.

**Employee follow-up** (`dossier-suivi`) describes a casefile of documents, meetings, notes, actions and follow-ups. Sensitive employee information, allegations, assessments and decisions must not be conflated. An operational system needs enforceable permissions, retention/deletion policies, auditability, and applicable legal review.

**Medical or police protocols** (`procedure-protocole`) describe protocols and their branches. An archived protocol is not a live instruction, an executed authorization, or a replacement for current local policy, professional judgment and required approvals.

## System-state and diagnostic records

Distinguish observed state, desired configuration, inferred system health, reported symptoms, hypotheses, test results, and approved interventions. A suggestion to reboot a system is not authority to execute it.

## Cross-Kristal references and publication

- An external reference does not transfer semantic ownership.
- Pinning exact sources and their provenance is necessary when asserting reliance on outside work.
- A diagram, search index, reader view or Context Pack does not grant access to restricted data.
- Composition plans are `design_only`, with unresolved contracts and no publication authorization.
- No part of Arketype automatically pushes to a repository, qualifies facts, synchronizes data or activates a runtime.

## Recommended operational checklist

Before building a real application around an archetype, specify: the responsible data owner; user roles and access policies; lawful collection basis where relevant; retention; source attribution; immutable event history if required; version pinning; validation; error handling; and explicit publication/activation controls.

**See also:** [Architecture](Architecture), [Composition Recipes](Composition-Recipes), [Validation and Testing](Validation-and-Testing).
