# C034 addendum: clipping breaks shared-offset cancellation

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent verification NOT_RUN. Scope: decision-hub method dispatch and failure tests. Complements the existing C034 shared-offset addendum; no existing result or frozen protocol is changed.

## Decision gap and method-selection rule

The earlier C034 addendum proves that an *unclipped additive* objective-specific calibration offset cancels in a pairwise utility difference. A score interface that constrains every value to [0,1] by clipping changes that mathematical model. A decision hub must inspect the transformation applied to raw scores before selecting the shared-offset cancellation certificate.

Inputs: nominal A=(0.8,0.4), B=(0.5,0.8), weight w in [0.60,0.65], shared offsets c1,c2 in [-0.30,0.30], and transformed scores T(z)=min(1,max(0,z)). Both options receive the same offset within each objective. Scores are cardinal, higher is better, and hard constraints are checked first. This is a synthetic counterexample, not empirical calibration evidence.

## Constructive reversal witness

Take w=0.60, c1=+0.30, c2=-0.30. After clipping, A=(1.0,0.1), B=(0.8,0.5). The weighted utility difference is 0.60*(1.0-0.8)+0.40*(0.1-0.5)=-0.04. Thus B outranks A in this feasible realization.

The unclipped shared-offset formula would instead yield 0.7w-0.4=+0.02 and certify A. Its assumptions fail after clipping. In the nominal no-offset realization, D=+0.02 at w=0.60. Therefore a shared offset plus clipping can change the ranking. It is unsafe to apply the original certificate simply because the offsets share provenance.

The exact calculation for any declared offset pair is D(w,c1,c2)=w[T(0.8+c1)-T(0.5+c1)]+(1-w)[T(0.4+c2)-T(0.8+c2)]. With unknown offsets, bound this expression over the *joint* feasible set, using the actual transformation and dependencies. Do not substitute the unclipped formula or assign probabilities. A finite exact bound for this piecewise-linear example can be found by evaluating endpoints and clipping breakpoints of c1,c2, together with weight endpoints; the objective is multi-affine within each clipping cell.

## Baselines, failure conditions and acceptance preparation

Simple baseline: nominal weighted score comparison at w=0.60 gives A ahead by 0.02. Independent-cell rectangle is a separate conservative baseline, not evidence that score errors are independent. The clipping-aware comparison is the appropriate candidate when the data pipeline really clips.

Candidate acceptance checks: (1) reproduce the witness D=-0.04; (2) verify no-offset D=+0.02; (3) preserve the original +0.02 unclipped result under the same shared offsets; (4) reject shared-offset cancellation when clipping is declared; (5) do not assume clipping without provenance; (6) do not infer a probability of reversal; (7) unknown transformation or unknown dependency returns UNKNOWN for the certificate; (8) hard-constraint REJECT cannot be reversed by score comparison; (9) verify the clipping breakpoint search against dense synthetic sampling; (10) ensure the user's weight bounds remain unchanged.

Failure conditions: non-cardinal or incomparable scoring, unknown transformations, option-specific offsets, changed weight semantics, and unresolved feasibility. Data track owns empirical evidence about clipping and calibration provenance. Independent acceptance track owns a separate implementation and boundary tests. Formal integration requires owner authorization. No source-paper replication, program test, real-user validation, or scientific acceptance is claimed.

Source relation: project-local algebraic counterexample to the assumptions of C034_ADDENDUM_SHARED_SCORE_ERROR_CANCELLATION_2026-11-20.md; no external primary-paper claim.
