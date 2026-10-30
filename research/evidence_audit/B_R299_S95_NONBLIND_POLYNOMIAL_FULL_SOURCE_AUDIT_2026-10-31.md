# B R299 S95 nonblind exact algebraic and source audit

Date: 2026-10-30 UTC. Target key (B,R299,S95-v1,independent-polynomial-weights-and-full-400-source-audit). Prospective B test plan committed as `1d510d923f6d8ebe7b163811d249eaa2b0378d15` before B execution. The main S95 protocol was committed as `6a84026ee32039b1e4b256ae46370aee1add11de` before R computation.

## Actual read and execution scope

Read original R299 prescore protocol, report, original bounded E1 acceptance, R S95 freeze, archived JS generator, complete 400-row CSV, complete 40-group JSON, and current GitHub blob identities. Executed the archived R generator in the V8 JavaScript environment, regenerating the exact original CSV and JSON contents with byte-for-byte equality to remote GitHub files. Executed archived B JavaScript auditor independently in V8, importing no R generator code. Local Python 3 standard-library Fraction independently computed the 40 group risks by a separate formula and the eight nontrivial gamma=1/2 paired differences agreed exactly.

## Independent mathematics

Let alpha=1/2, q=1-alpha and j index rewards from 0 to n-1. MC final S0 is the sum of R_j times coefficient gamma*alpha*q^(n-1-j). Online TD final S0 has coefficient gamma*alpha^2*(n-1-j)*q^(n-2-j) for j<n-1 and coefficient zero for the latest reward. Both S1 estimates use coefficient alpha*q^(n-1-j). These polynomial weights are derived independently from the update ordering and avoid importing the R recursion.

With independent Bernoulli rewards 2*Bernoulli(p), mean of S0 is 2p times sum(weights); variance is 4p(1-p) times sum(weight^2). Squared bias uses the oracle gamma*2p. Holdout risk adds oracle irreducible 4gamma^2 p(1-p). These formulas reconstruct all archived aggregate fields and every source's final values, history probability, estimation error and conditional holdout risk.

## Executed gates

| Gate | Actual result |
| --- | --- |
| Complete source identity and unique keys | 400 / 400 PASS |
| Frozen group universe and probability mass | 40 / 40 PASS |
| Exact paired comparisons | 20 / 20 PASS |
| R archived JS replay vs remote CSV | BYTE_EQUAL PASS |
| R archived JS replay vs remote JSON | BYTE_EQUAL PASS |
| Independent no-import B polynomial audit | PASS |
| Local Python Fraction cross-language spot checks | 8 nontrivial comparisons exact |
| Mutations: duplicate, deletion, probability, S0, S1, row holdout, group risk, E2 promotion | 8 / 8 REJECTED |
| Archived Node CLI in native checkout | NOT_RUN |
| External independent team | NOT_RUN |
| GitHub Actions | NOT_RUN |

The full source and result blob SHA1 values, original JS script and B auditor identities are preserved in `research/validation/R299_S95_MACHINE_REPLAY_RECEIPT_2026-10-31.json`. Original deterministic R299 remains separately CLOSED_BOUNDED_E1; new S95 remains PARTIAL. This is nonblind internal programmatic replication, with the same study team seeing R outputs before B audit. It does not establish external reproducibility or real human E2 performance.

## Scientific limitations and open gates

No empirical training/test separation, human probability calibration, uncertainty interval from independent experiments, causal psychological claim or general TD/MC superiority is supported. The independent test reward here is an exact artificial fresh draw. Original R073 and PESEN v0.1 frozen. E1 only, E2=0, E3=0. No Actions were dispatched; free-runner quota and billing were not independently checked. Native Node --test, --emit and --check in a clean checkout remain open. Preserve all original sources and negative evidence.
