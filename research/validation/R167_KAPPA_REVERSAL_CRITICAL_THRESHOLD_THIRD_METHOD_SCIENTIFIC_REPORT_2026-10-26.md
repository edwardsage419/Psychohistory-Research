# R167 third method: exact critical group reweighting threshold

Date: 2026-10-26 Asia/Singapore
Evidence: E1, artificial two-group mathematics only
Status: PASS_BOUNDED_INTERNAL_E1
Prior formal R167 status: CLOSED_BOUNDED_E1 unchanged
Frozen new protocol: [R167 critical threshold preregistration](../../protocols/R167_KAPPA_REVERSAL_CRITICAL_THRESHOLD_THIRD_METHOD_FREEZE_2026-10-26.md), committed before execution in `3ff757de60838bb742fe5347c94f2a3a0a935fea`.
Original archived R167 results blob: `86839d8d473e4aee2f450d8c598797299ec1cf41`.

## Question and exact derivation

For fixed initial low and high group frequencies a<=b, low/high weights x,y>0, x+y=1, local decline delta>0, and pre-state group reweighting kappa>=0, define

```
q_g = p_g - delta*p_g*(1-p_g)
R_g = 1 + kappa*p_g
w'_g = w_g*R_g / sum_h w_h*R_h
P' = sum_g w'_g*q_g
```

Set m=xa+yb, S=xa(1-a)+yb(1-b), C=1-delta(1-a-b), and gap=b-a. Then the exact one-step decomposition is

```
W = -delta*S
B = x*y*kappa*gap^2*C / (1+kappa*m)
P'-P = W+B
```

This follows from q_b-q_a=(b-a)*C and the two-group covariance identity. Let D=xy*gap^2*C-delta*S*m. When D>0,

```
P'-P > 0  if and only if  kappa > kappa_crit = delta*S/D.
P'-P = 0  if and only if  kappa = kappa_crit.
```

When D<=0 and S>0, no finite nonnegative kappa reverses the within-group decline. The theorem assumes the specified two-group recurrence, fixed initial state and nonnegative group-growth factors. It is a conditional mathematical result, with no inferred real group selection mechanism.

## Frozen-grid results

The original 4 frequency pairs × 2 high-group weights × 3 delta values × 3 kappa values produced exactly 72 distinct first-step cases. Eleven exact rational scalars per case, including archived within, between, total, frequencies and weights, matched the original R167 JSON. Total: 792 exact archival comparisons, zero mismatches.

The 24 delta-positive cases correspond to 8 unique initial configurations with 3 kappa values each. Four unique configurations have a finite threshold, producing 12 grid cases; the other four configurations produce 12 cases with no finite nonnegative threshold. All 24 sign predictions passed. Among the 24, 5 grid cases show strict aggregate reversal and zero cases lie exactly at the critical threshold. All 36 off-grid direct-weight boundary tests passed, comprising kappa_crit/2, kappa_crit and kappa_crit+1 for each of 12 finite-threshold grid cases. Forty-two controls covering kappa=0 and equal group frequencies passed.

Distinct finite critical values:

| initial (a,b) | high-group weight y | delta | kappa critical |
| --- | ---: | ---: | ---: |
| (1/4,3/4) | 1/2 | 1/4 | 6/5 |
| (1/4,3/4) | 3/4 | 1/4 | 8/3 |
| (1/5,4/5) | 1/2 | 1/4 | 4/7 |
| (1/5,4/5) | 3/4 | 1/4 | 80/83 |

The (1/3,2/3) and equal-frequency (1/2,1/2) pairs have no finite reversal threshold for these frozen weights and delta=1/4. This statement is specific to the frozen settings.

Prespecified boundary check for (a,b)=(1/4,3/4), y=1/2, delta=1/4:

| kappa | exact net P'-P |
| --- | ---: |
| 1 | -1/192 |
| 6/5 | 0 |
| 2 | 1/64 |

This extends the original single Simpson-style example to a precise necessary and sufficient reweighting threshold.

## Execution and provenance

Primary executable: [JavaScript exact BigInt rational implementation](r167_critical_kappa_threshold_20261026.js). It reads the original immutable JSON from `research/R167` and checks all 72 first-step records. Actual execution in the research environment produced [72-case exact receipt](R167_KAPPA_REVERSAL_CRITICAL_THRESHOLD_72_WORLD_EXACT_RECEIPT_2026-10-26.json). The executable was reloaded from GitHub and the calculation was repeated in a separate execution.

B audit: independent Python Fraction implementation using direct normalized weights and a separately derived affine numerator threshold. It was executed locally with 72 cases, 24 sign checks, 36 exact boundary tests and 42 controls. Its local source Git blob was confirmed identical to the committed [B source](../evidence_audit/r167_b_independent_threshold_20261026.py). See [B report](../evidence_audit/B_R167_INDEPENDENT_DIRECT_WEIGHT_THRESHOLD_SCIENTIFIC_AUDIT_2026-10-26.md).

Scientific limits: the primary and B scripts are independent implementations within the same research project. This is internal programmatic corroboration, not external independent replication. No held-out human prediction, historical calibration, causal identification, probability calibration or real-group inference is provided. E2=0, E3=0, external replication=0. R073 and PESEN v0.1 remain frozen. The original239 v7.8 crosswalk and 154-item queue remain unchanged. No new paid resources or GitHub Actions were initiated.
