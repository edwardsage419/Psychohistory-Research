# R336 scientific report: constructed inoculation and novel-attack transfer

Date 2026-10-24. Original239 **03-014 Inoculation Theory**. Scientific status **PASS_BOUNDED_E1_CONSTRUCTED_INOCULATION_TRANSFER_CONTRAST_ONLY**.

## English primary sources and reuse review

McGuire (1961), *Resistance to Persuasion Conferred by Active and Passive Prior Refutation of the Same and Alternative Counterarguments*, *Journal of Abnormal and Social Psychology* 63:326–332, DOI 10.1037/h0048344. McGuire and Papageorgis (1961), *The Relative Efficacy of Various Types of Prior Belief-Defense in Producing Immunity Against Persuasion*, 62:327–337, DOI 10.1037/h0042026. Papageorgis and McGuire (1961), *The Generality of Immunity to Persuasion Produced by Pre-exposure to Weakened Counterarguments*, 62:475–481, DOI 10.1037/h0048430. The 1961 studies investigated real participants, with conditional interactions and transfer claims. This research does not use their participant records or fitted coefficients.

The [03-014 reuse preaudit](../../docs/ORIGINAL_239_03-014_INOCULATION_REUSE_PREAUDIT_2026-10-24.md) reviewed R291, R292, R303, R307, and R334. R335 also concerns constructed public pressure. Their inspected summaries do not establish the exact present model. Early R001–R064 binary ZIP itemwise audit remains blocked. **NO_STRICT_REUSE_VERIFIED_IN_INSPECTED_SUMMARIES** does not imply global novelty.

## Temporal order and complete source

[Prescore frozen protocol](../../protocols/R336_INOCULATION_96_ARTIFICIAL_ATTACK_ATOMS_PRESCORE_FREEZE_2026-10-24.md) committed at [3f10d5a6c2c8b713d3b14abc61c768383de8c934](https://github.com/edwardsage419/Psychohistory-Research/commit/3f10d5a6c2c8b713d3b14abc61c768383de8c934). All artificial data, replay source and independent audit committed later at [1d580bed37891ca4516a5c3d338037bd3ba8c2d1](https://github.com/edwardsage419/Psychohistory-Research/commit/1d580bed37891ca4516a5c3d338037bd3ba8c2d1). No retroactive modification to frozen rules.

Enumerated 3 preexposure modes (NONE, PASSIVE, ACTIVE), 2 weak-preview flags, 2 refutation flags, 2 same-versus-novel attack flags, and 2 subsequent attack intensities. Exactly **48** fully specified worlds. Two competing policies per world yield **96** complete artificial CSV records. No sampled participants, no stochastic observations and no empirical fitting.

Belief starts at 6, unprotected attack reduces it by 2 or 4. The transfer model has preassigned defenses of 2/3 for passive/active on same-topic attacks, 1/2 for novel attacks, conditional on weak preview and refutation. The topic-specific support countermodel uses the same defense on same-topic attacks and zero on novel attacks. These integer assignments are investigator-created and cannot measure actual resistance.

## Prespecified exact falsifiers

| Gate | Exact finite result | Assessment |
|---|---|---|
| F1 | 48 worlds, 96 original artificial records | PASS |
| F2 | Same-topic model agreement 24/24 | PASS |
| F3 | Novel-topic transfer strictly exceeds countermodel 4/24 | PASS |
| F4 | Weak-preview absent 24/24 and refutation absent 24/24 have no benefit | PASS |
| F5 | Strong same-topic active=5, passive=4; weak later attack active=passive=6 | PASS |
| F6 | Independent no-import enumeration and two tamper rejections | PASS |
| F7 | Three GitHub Actions jobs success | PASS |

The four novel-topic differences occur exactly when preview and refutation are present and the mode is passive or active. Other 20 novel-topic conditions agree. Stronger assigned defense can saturate at the initial belief ceiling, so even the constructed active mode has no strict advantage in every condition.

## Independent validation

[GitHub Actions run 40055738338](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40055738338) completed with **python311=success, python312=success, independent=success**. Each production interpreter ran six unit tests and exact byte replay. The independent script uses index-based state enumeration, does not import the production module, reconstructs both CSV and JSON byte for byte, and rejects one altered CSV model label and one altered JSON result. This tests replay integrity and consistency with the frozen finite rules. It does not establish the causal psychological mechanism or external validity.

## Scientific limits and future gates

Scientific evidence **E1 constructed finite arithmetic only**. Real human E2: NOT_ESTABLISHED. Historical E3: NOT_ESTABLISHED. Original 1961 participant-level replication: NOT_ESTABLISHED. Cross-attack transfer and the difference from topic-specific support are imposed by the model's fixed integer coefficients; they are not independent human findings. Early archive strict reuse audit and 173 provisional README links remain OPEN. Crosswalk provenance does not imply scientific validity. R073 and PESEN v0.1 unchanged. Complete R series and evidence audits before classification and fusion; personal decision system deferred.
