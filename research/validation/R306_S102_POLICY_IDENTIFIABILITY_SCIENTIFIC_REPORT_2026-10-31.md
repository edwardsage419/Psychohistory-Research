# R306 S102 scientific report: exact group-polarization policy identifiability

Date 2026-10-31 UTC. Research track r. Pre-score protocol commit dd7ac39f7411cab9995658b283caf0c5624dc1d2. Original R306 freeze 1db7fc7cc12cbf1bbec67e3df25c634d689c25b6. Source original 216-world JSON Git blob fc06f79fa1c7a232e2c74a4c8d3031fa1580ac24. This is a project-invented E1 artificial finite model, not an empirical claim about human polarization. Original R306 CLOSED_BOUNDED status unchanged. Extension S102 scientific acceptance PARTIAL.

## Question, frozen experiment and mathematical mechanism

For each of 27 ordered three-person opinion triplets from {-1/2,0,1/2}, distinguish four original policies AVG, SOCIAL, ARG, COMBINED using an exactly observed group post-discussion mean. The original model is m_post=m+alpha(c-m)+beta(a-m), with q=sign(m), c the most extreme existing member in the direction q, and a=q (supporting) or -q (counter). Policies have (alpha,beta)=(0,0),(1/2,0),(0,1/2),(1/2,1/2). The original 27 groups x 4 policies x 2 contexts = 216 worlds are reused unchanged.

Prespecified observation designs: SUPPORT_ONLY, COUNTER_ONLY, BOTH_CONTEXTS with the same policy stable across both contexts. Exact signatures partition four policies; report identifiable labels, ambiguous labels, four-way-identifiable groups, and optimal classification accuracy with a uniform prior over the four policies. This is an oracle with perfectly known prediscussion triplet and zero measurement noise, so its accuracy is an upper bound for the stipulated observation contract.

## Exact results

| Design | Distinct policy-signature classes across 27 groups | Uniquely identifiable policy worlds out of 108 | Ambiguous policy worlds | Fully identifiable groups out of 27 | Uniform-prior optimal policy classification accuracy |
| --- | ---: | ---: | ---: | ---: | --- |
| SUPPORT_ONLY | 83 | 72 | 36 | 18 | 83/108 |
| COUNTER_ONLY | 83 | 72 | 36 | 18 | 83/108 |
| BOTH_CONTEXTS | 83 | 72 | 36 | 18 | 83/108 |

For each design, 18 groups have four singleton policy classes; 2 homogeneous nonneutral groups have two classes of size two; 7 neutral-mean groups have one class of size four. All 27 group partitions are archived in the JSON. 216 original policy-context worlds are archived in the CSV. These are exact finite counts, not a population sample or human effect sizes.

## Negative finding and mechanism limitation

Observing both argument contexts gives ZERO improvement over observing either single context on this frozen universe. The additional observation is redundant for distinguishing the four policies, despite changing some numerical outcomes. In homogeneous all-positive/all-negative groups, AVG and SOCIAL are observationally equivalent, and ARG and COMBINED are observationally equivalent. In all seven zero-mean groups, all four policies yield zero under both contexts. Thus even an error-free consensus measurement does not uniquely identify a mechanism in 9 of the 27 artificial groups. This is structural non-identifiability, not statistical noise.

Example group (0,0,1/2): SUPPORT outputs AVG=1/6, SOCIAL=1/3, ARG=7/12, COMBINED=3/4; COUNTER outputs AVG=1/6, SOCIAL=1/3, ARG=-5/12, COMBINED=-1/4. All four policies are identifiable in either context. Homogeneous (1/2,1/2,1/2) has AVG=SOCIAL=1/2; ARG=COMBINED=3/4 in SUPPORT and -1/4 in COUNTER. Both contexts cannot distinguish these pairs.

The original 216 archived world outcomes were directly reread and checked against an independent integer-twelfths reconstruction: 216/216 post-means matched, 0 mismatches. This check is nonblind, performed within the same research project.

## Source, execution and independent audit

Original project model source: research/R306/r306_exact_group_polarization.py (blob 3fcb1a5fd9032f7bcf615d7a77ff8597b8c31ea8). Original author-level motivation: Moscovici and Zavalloni 1969 DOI 10.1037/h0027568; Myers and Lamm 1976 DOI 10.1037/0033-2909.83.4.602; Burnstein and Vinokur 1977 DOI 10.1016/0022-1031(77)90002-6. No original empirical trial data or author-fitted model parameters were used.

The archived R generator (research/validation/r306_s102_policy_identifiability.py) ran with standard-library Python 3, generated exactly 216 rows and 27 partition objects. CSV SHA256 fc0aec7a2bf930f9675b0e92368b684543212d7e2d726b3306258c62eaea95f8; JSON SHA256 da3d74090f51a6bdc91981d9216459747b8d8d3003e6e7f688724ef8182c787c. Independent B script uses a separate Fraction affine oracle and explicit exceptions, no R imports; its full-source/partition audit passed and rejected 9/9 tamper tests in both ordinary and python -O execution. Local generator and independent script were run before GitHub archive. GitHub Actions were not triggered; remote CI remains NOT_RUN. External independent researcher replication NOT_RUN.

## A01 through A06 and boundaries

A01 PASS for frozen finite identification question and observation contracts. A02 PASS for original project-model fixed Git blobs and synthetic source identity, with empirical mechanism validation OPEN. A03 PASS for local exact generator, independent local audit and byte-matched Git blobs, CI OPEN. A04 PASS for neutral/homogeneous controls, no-gain negative finding and 9 tamper rejections. A05 PASS for explicitly limited E1 claims; E2 human=0, E3 history=0, external replication=0. A06 OPEN until future formal extension acceptance; status PARTIAL. Original R306 closure remains unchanged. R073 model and scoring FROZEN, PESEN v0.1 FROZEN. No model fusion, no personal decision system.

## Next evidence

A new experiment would need actual within-group pre/post attitudes, known argument conditions, independent group identity and appropriate consent/license. Observational equivalence can only be reduced by adding measurements or interventions that truly distinguish the policy mechanisms, with a new protocol frozen before analysis. No post hoc choice of a favorable artificial grid. No new paid services.
