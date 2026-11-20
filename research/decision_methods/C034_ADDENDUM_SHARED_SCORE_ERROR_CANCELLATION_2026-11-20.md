# C034 addendum: shared calibration errors and pairwise cancellation

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent verification NOT_RUN. Extends C034's rectangular score-error example without changing its result, any R-series status, R073, PESEN v0.1 or frozen protocol.

## Decision problem

The C034 score-error radius e assumes four independent score cells. A real scoring instrument can instead have a shared objective-specific calibration offset. Treating the same shared offset as four independent errors can produce an unnecessarily unresolved comparison. This addendum gives an exact dependency-aware certificate for one narrow additive model.

## Inputs and assumptions

Two options have nominal A=(0.8,0.4), B=(0.5,0.8). Weight w is user-confirmed only to lie in [p,q] within [0,1], second weight 1-w. All scores are higher-is-better cardinal values on compatible, explicitly accepted scales; hard constraints have already been checked.

For objective j in {1,2}, the observed/actual score is x_j(a)=mu_j(a)+c_j for BOTH options a in {A,B}. Each common offset c_j lies in [-e,e], and may be correlated across objectives. The same c_j must apply to both options in a given joint realization. No option-specific residual error is included in this model. Scores are not clipped or renormalized after adding offsets. No probability distribution is asserted.

## Exact result and minimal example

U_w(A)-U_w(B)=w[(0.8+c_1)-(0.5+c_1)]+(1-w)[(0.4+c_2)-(0.8+c_2)]=0.7w-0.4.

Thus the exact feasible difference interval is [0.7p-0.4,0.7q-0.4], independent of e, provided the joint additive model is correct. Universal strict A preference iff p>4/7; universal strict B preference iff q<4/7. At equality, strict preference is not certified. If the interval straddles 4/7, either ordering may occur.

At w in [0.60,0.65] and e=0.03, min difference is 0.02 and max 0.055, so A is universally strictly preferred. Under C034's DIFFERENT independent-cell rectangle with the same e, min difference would be 0.02-0.06=-0.04, hence unresolved. These are different uncertainty sets and cannot be interchanged. The common-error model is justified only by evidence that the calibration error really is shared.

## Residual error extension

If x_j(a)=mu_j(a)+c_j+r_j(a) with four independently bounded residuals |r_j(a)|<=h, the common offsets still cancel. The exact difference interval becomes [0.7p-0.4-2h,0.7q-0.4+2h]. This reproduces C034 with h in place of e. If residuals are dependent, use their actual joint feasible set; the rectangle may be conservative.

## Baselines, failure conditions, evidence

Baseline: C034 independent-cell rectangle. It is conservative when the shared-offset model is true. A second baseline uses nominal scores and midpoint w; it cannot certify a full interval.

Failure conditions: option-specific biases, multiplicative calibration, nonlinear transformations, clipping at score boundaries, unverified common-error assumption, changes to weight semantics, incomparable units, or unknown hard-constraint feasibility. UNKNOWN dependency structure must not silently be replaced with shared-error cancellation. An option rejected by C028 remains rejected.

This is an algebraic project-local synthetic example, not a replication of an external original paper. It supplies no empirical evidence that any actual score source has shared calibration error. Data track should check calibration design and joint provenance; independent acceptance track should implement separate joint-realization tests. Formal model integration remains subject to owner authorization.

## Candidate acceptance properties

1. Exact cancellation of shared c_1 and c_2 at fixed w.
2. Correct endpoint extrema over [p,q].
3. Equality p=4/7 yields no strict A certificate; q=4/7 yields no strict B certificate.
4. At [0.60,0.65], e=0.03 gives lower difference 0.02 for shared errors, versus -0.04 for independent-cell errors.
5. Adding independent residual radius h restores the 2h penalty.
6. Arbitrary correlation between c_1 and c_2 does not affect cancellation.
7. Option-specific offsets invalidate the shared-error certificate.
8. Unknown dependence yields UNKNOWN for the shared-model claim, without claiming independence is empirically true.
9. C028 hard-constraint REJECT is never overridden.
10. Score clipping or nonlinear transforms require a new calculation.
