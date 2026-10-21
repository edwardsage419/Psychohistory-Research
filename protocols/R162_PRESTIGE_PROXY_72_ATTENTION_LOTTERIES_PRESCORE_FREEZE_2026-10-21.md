# R162 precode freeze: artificial prestige proxy, selective copying and unobserved competence

Date 2026-10-21. Original catalog **P1 / 07-004 Prestige Biased Transmission** (exact label and priority verified in MODEL_CANDIDATE_CATALOG_v0.1.json). Previous R161 CLOSED_BOUNDED_E1, indexed main commit f9c58aafdbd8ad1b778279e4ac1ed5b111d1ca03. All frozen cases and tests recorded before program implementation.

## Primary scholarly sources and measurement boundary
Henrich & Gil-White (2001), *The evolution of prestige: freely conferred deference as a mechanism for enhancing the benefits of cultural transmission*, *Evolution and Human Behavior* 22(3):165–196, DOI [10.1016/S1090-5138(00)00071-4](https://doi.org/10.1016/S1090-5138%2800%2900071-4); original Elsevier abstract directly checked: prestige differs from coercive dominance and can serve as a proxy for expertise or quality of cultural information.
Chudek et al. (2012), *Prestige-biased cultural learning: bystander's differential attention to potential models influences children's learning*, *Evolution and Human Behavior* 33(1):46–56, DOI [10.1016/j.evolhumbehav.2011.05.005](https://www.sciencedirect.com/science/article/pii/S1090513811000481), original publisher abstract checked, reporting an empirical child-learning test of attention cues.
Jiménez & Mesoudi (2019), *Prestige-biased social learning: current evidence and outstanding questions*, *Palgrave Communications* 5:20, DOI [10.1057/s41599-019-0228-7](https://www.nature.com/articles/s41599-019-0228-7), open original critical review abstract and discussion checked, emphasizes unresolved measurement and evidence issues.
This project has NOT accessed the original experimental child choices, original attention observations, prestige/competence measurements, or any author-level fit. The toy attention weights below are an invented **cue**, not operationalized prestige or actual skill. No physical coercion/dominance, individuals, real groups or trait stereotypes represented.

## Frozen 72 one-step demonstrations
Exactly three synthetic demonstrators indexed 0,1,2, each publicly adopting artificial cultural token A (1) or B (0). Four frozen observed action profiles, in order: 000, 100, 011, 111. Synthetic extra attention/prestige cue marks index j∈{0,1,2}, with additional integer attention tickets strength lam∈{0,1,3}; ticket weights w_i = 1+lam if i=j else 1. A hypothetical copy chooses demonstrator in proportion to their attention weight and copies that model's symbol:
P(A|y,j,lam)= sum_i w_i y_i / (3+lam).
The benchmark impartial choice is the simple arithmetic frequency P0(A)=sum_i y_i/3.
Artificial ground truth for success is exogenously assigned by c∈{0,1} (if c=1 symbol A correct, else B correct). Conditional **expected correctness** S=P(A) if c=1, else 1-P(A); baseline S0 defined from P0. There is no productivity payoff, no signal reliability assumption and no real correctness data. Exactly 4×3×3×2=72 distinct input cases.

## Independent exact oracles
1. Direct Fraction weighted-sum computation for P(A), P0(A), S, S0 and advantage S−S0.
2. Independently enumerate attention lottery tickets as [0,1,2] plus lam copies of j; calculate A ticket counts / total and success from that. No call to method 1. All 72 cases must exactly match in Fraction.

## Frozen counterexamples, identification and measurement limits
1. Pattern 100, favored j=0 and lam=3: P(A)=4/6=2/3, versus neutral 1/3. If A correct, expected correctness increases by 1/3; if B correct, it falls by 1/3.
2. Same pattern 100, j=1 and lam=3: P(A)=1/6, reducing exposure to A. A majority or success bias need not equal attention bias; no empirical claim that any actor has valid prestige cues.
3. When lam=0, j index has no effect for every action profile. For 000 or 111, copying output is independent of j and lam. Observed choice probabilities on these cases cannot identify whom the learner attended.
4. Signal-correctness confounding: if the favored model produces the correct output, biased copying can help; if the favored model produces the incorrect output, it harms. Derive the sign of S−S0 for all mixed-action cases, and record that unknown cue reliability prevents a general claim that prestige predicts competence.
5. Exact category complement symmetry: swap every y_i to 1−y_i and correctness c to 1−c, then S remains identical, while P(A) becomes 1−P(A).
6. Expected copying can depend on j even with fixed model action frequencies; two histories with the same 1-of-3 frequency can produce different P(A). A model using just the mean frequency is insufficient under weighted sampling.
7. Correctness values are artificial assigned labels, never empirical accuracy. No out-of-sample comparison or practical cultural learning decision evaluation.

## Formal gate
At least 72 separately named full-case unittest methods plus >=20 independent tests for identity/edge/negative controls; deterministic complete UTF-8 JSON, source/test/JSON ZIP, Python3.11/3.12 CI with pinned four SHA256, permanent GitHub main archive and readback. E1 only; E2=0 E3=0; R073/PESEN v0.1 frozen. R163 next original catalog entry to verify before announcing it. Finish original R sequence before classification/fusion.
