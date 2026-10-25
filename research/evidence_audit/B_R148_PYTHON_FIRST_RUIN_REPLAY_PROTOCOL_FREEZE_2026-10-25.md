# B R148 independent Python first-ruin audit freeze
Date: 2026-10-25. Parent main b64f7399675128975f5d778c732e3becd98a79da.
Input: frozen R148 original nine-stock eight-year synthetic process and newly generated event-path CSV. No changes to R148 policy rules. Evidence E1 only.

Prespecified independent verification: use Python standard library Fraction or exact integer arithmetic to implement a fresh state-distribution recursion over 9 stock states and four climate/failure events for q=f=1/4. Compare all eight first-ruin weighted numerators, terminal survivor, expected harvest, and annual fees against the separate JavaScript full 65536 event-path enumeration for OPEN, QUOTA and ADAPT. Each probability uses denominator 4^16. Verify archived R148 survival and net outcomes.

Prespecified adversarial controls: change absorbing stock zero into positive one and require the state-machine invariant to reject; replace the original eight-year unconditional governance fee with a stop-after-ruin fee and require a different ledger for QUOTA and ADAPT. Verify denominator/mass identity, and inspect first-ruin cumulative distributions without treating them as observed hazard rates. Any policy comparison is an E1 within-model comparison only.

Preserve script, receipt, and audit report under research/evidence_audit. No external human E2, historical E3, or independent external research team. CI may remain NOT_RUN for zero-cost safety.