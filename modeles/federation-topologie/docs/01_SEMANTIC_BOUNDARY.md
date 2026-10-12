# Semantic ownership boundary

**Candidate responsibility:** topology-owner.

**Preserve:** A parent reference does not own or absorb a child state.

**Avoid:** Do not copy subordinate commitments or assume a parent owns each referenced child.

External sources and separately owned knowledge states should be linked through explicit references rather than silently duplicated into the local canon. Any real-world ownership decision requires a domain contract.
