# Semantic ownership boundary

**Candidate responsibility:** event-history-owner.

**Preserve:** An event log is not necessarily current state or causal proof.

**Avoid:** Do not equate a timestamped observation with established causality or current state.

External sources and separately owned knowledge states should be linked through explicit references rather than silently duplicated into the local canon. Any real-world ownership decision requires a domain contract.
