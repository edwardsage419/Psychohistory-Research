# R304 S100 scientific report: noisy group-label observation and predictive risk

Date UTC 2026-10-31. Freeze commit: 04424fe2798d8b03efe90d582ac6a29ed0ccdbfd. Original R304 source freeze: 60f6406cede7eb5bb7cea9dc622835d8fe3f4c41. Scope: E1 artificial project-created utility only. Status: PARTIAL.

## Exact prespecified results

Original 216 artificial decisions were checked against the frozen R304 JSON. There are 108 label-free (s,d,e,menu) configurations. Exactly 12 have different actions under the two group labels; 96 have the same action. All 12 of the original alternative choices are accounted for. The new complete source contains 1296 atomic (true label, observed label, error level) rows, including zero-probability atoms.

Across the 108 equally weighted configurations, Brier risks are:

| Symmetric label error | Prior without observed label | Naive use of observed label | Bayes using known error |
| --- | --- | --- | --- |
| 0 | 1/36 | 0 | 0 |
| 1/4 | 1/36 | 1/36 | 1/48 |
| 1/2 | 1/36 | 1/18 | 1/36 |

For a label-sensitive configuration, the prior risk is 1/4, naive risk is epsilon, and calibrated Bayes risk is epsilon(1-epsilon). Invariant configurations have zero loss under all three predictions. This is an exact known-parameter theoretical exercise. The Bayes improvement at epsilon=1/4 is 1/144 in grid-average Brier relative to either prior or naive. At epsilon=1/2, a naive perfectly trusted noisy label doubles the aggregate risk relative to the label-free prior. The boundary depends on the deliberately balanced two-label prior, symmetric channel and original artificial utility grid.

## Reproducibility and scientific scope

R generator: research/validation/r304_s100_noisy_label.js. Frozen original R304 results and 216 decisions checked exactly; 1296 source atoms enumerated. The B independent threshold oracle uses the menu-specific direct inequalities s*d>2e for equal-total favored alternatives and 6s*d>16+12e for lower-total favored alternatives, with opposite-group alternatives never chosen. The B auditor independently checks every atom and all three risks; eight altered-source/summary controls were rejected in the in-session V8 execution. A separate Python Fraction enumeration reproduced all nine aggregate risk values. This is internal nonblind mathematical verification; native Node CLI and external team execution remain NOT_RUN unless separately observed.

The experiment assumes an analyst knows the exact s,d,e and menu and knows the noise rate. No real participant allocation, learned parameter, uncertainty estimate, experimental randomization, sample-out-of-study prediction, or external generalization is supplied. No empirical probability calibration is established. No new E2 human or E3 historical evidence. R073 and PESEN v0.1 remain frozen. Original R304 bounded E1 acceptance is unchanged. GitHub Actions were not requested because free-run quota was not independently verified.
