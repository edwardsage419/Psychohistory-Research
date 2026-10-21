# R162: Attention prestige-proxy copying, synthetic correctness and identifiability controls

Date: 2026-10-21. Original catalog **P1 / 07-004 Prestige Biased Transmission**. Computation and tests predeclared in [frozen protocol](../../protocols/R162_PRESTIGE_PROXY_72_ATTENTION_LOTTERIES_PRESCORE_FREEZE_2026-10-21.md), commit [67c6805](https://github.com/edwardsage419/Psychohistory-Research/commit/67c6805792bb71d09afc9f2f1e8e0a9d7383a928). **CLOSED_BOUNDED_E1** for 72 toy attention lotteries only. No real prestige observed and no validated learning or success predictions.

## Original literature and critical measurement boundary
* Joseph Henrich and Francisco J. Gil-White (2001), *The evolution of prestige: freely conferred deference as a mechanism for enhancing the benefits of cultural transmission*, *Evolution and Human Behavior* 22(3):165–196, DOI [10.1016/S1090-5138(00)00071-4](https://doi.org/10.1016/S1090-5138%2800%2900071-4). The original Elsevier publisher abstract and introduction were checked. Their theory distinguishes voluntarily conferred prestige from coercive dominance, and proposes others' deference as a potentially useful indirect cue for social learning. This mathematical demonstration does not recreate prestige psychology, observational cue validity, any original empirical examples, or its evolutionary fitness theory.
* Chudek and colleagues (2012), *Prestige-biased cultural learning: bystander's differential attention to potential models influences children's learning*, *Evolution and Human Behavior* 33(1):46–56, DOI [10.1016/j.evolhumbehav.2011.05.005](https://www.sciencedirect.com/science/article/pii/S1090513811000481). Original publisher abstract checked, concerning an experimental test with children; **original children's observed decisions and treatments were not acquired or replayed**.
* Ángel V. Jiménez and Alex Mesoudi (2019), *Prestige-biased social learning: current evidence and outstanding questions*, *Palgrave Communications* 5:20, DOI [10.1057/s41599-019-0228-7](https://www.nature.com/articles/s41599-019-0228-7). The original open review abstract and publisher presentation were examined. The distinction between cue popularity/prestige, actual skill in the relevant domain, and adaptive accuracy remains empirically important. **No field data, actual observer attention or direct competence records were fitted in this R162**.

## Artificial model and 72 prespecified cases
Three completely fictional demonstrators labeled 0,1,2 exhibit binary, abstract actions \(y_i\in\{0,1\}\), with four ordered patterns 000, 100, 011, 111. One person index j∈{0,1,2} is arbitrarily assigned a *hypothetical* attention-cue status, granting \(\lambda\in\{0,1,3\}\) extra selection tickets beyond every demonstrator's one base ticket. The probability of copying artificial action A=1 is exactly
\[
P_A(y,j,\lambda)=\frac{\sum_{i=0}^2(1+\lambda\mathbf 1_{i=j})y_i}{3+\lambda}.
\]
Neutral baseline sampling has \(P_0(A)=\sum_i y_i/3\). An **externally assigned artificial correct token** c∈{0,1}, independent of all cues, defines hypothetical single-choice success S=P_A if c=1 and S=1−P_A if c=0, and baseline S0 accordingly. Exactly **4 patterns × 3 cue indices × 3 attention strengths × 2 correct answers =72 frozen worlds**. None is a record of observed prestige, ability, attention or social contact.

Two independent exact Fraction algorithms:
1. Direct weighted selection probability plus synthetic correctness arithmetic.
2. Explicit enumeration of three base tickets and \(\lambda\) additional tickets for the favored demonstrator; count action A and externally assigned correct-action tickets in separate sums. 
Every one of the 72 combinations produced strictly identical five rational outputs (copy probability, neutral copy probability, synthetic success, baseline success and difference), and all probabilities were in [0,1]. [Full 35,093-byte results JSON](R162_EXACT_RESULTS.json) contains all 72 cases.

## Prespecified mathematical counterexamples
With public demonstrator actions (1,0,0), favoring demonstrator 0 with three extra tickets yields \(P_A=4/6=2/3\), versus neutral \(1/3\). If A is the correct synthetic response, model expected success improves by **+1/3**. If B is correct instead, exact same attention cue yields expected success change **−1/3**. Under exactly the same action pattern, favoring demonstrator 1 with three extra tickets makes \(P_A=1/6\).

Thus being copied more often does **not logically entail** possessing accurate information. Cue validity, true task competence and the ability to distinguish prestige from coercive dominance are empirical questions with no estimation in this experiment. The action-frequency statistic (one A out of three) by itself cannot determine the attention-weighted probability. Furthermore:
* \(\lambda=0\) makes selected model identity j unobservable in copying results.
* If all three actions agree, j and \(\lambda\) are unidentifiable from choice proportions, despite potentially distinct observer attention.
* Complementing all demonstrator actions and the correct answer leaves expected success and its change invariant, with A-copy probability replaced by its complement.
* Correctness here is entirely assigned; no actual short-run adaptive, evolutionary or historical fitness consequences are established.

These are concrete observation and construct-validity limits. Direct human-learning prediction would require carefully defined attention and observed success, with controlled comparisons against success bias, conformism and independent learning. R163 is separately allocated to the original catalog's **Success Biased Transmission**, so the two mechanisms will not be conflated in the present stage.

## Real CI evidence and permanent archive
[Source program](r162_prestige_attention_exact.py); [99 different genuine unittest methods](test_r162_prestige_attention_exact.py): 72 uniquely named full scenarios and 27 edge/identification/symmetry/input checks.
* Initial [CI run39526761194](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39526761194) successful, with Python3.11/3.12 each executing 99 tests and outputting identical SHA256 for source/test/full JSON/ZIP.
* Pinned [CI run39526844299](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39526844299) successful, two Python environments each executing 99 tests with four immutable SHA256 confirmations; publisher job118983462445 independently reran 99 tests and four SHA256, then permanently pushed [complete JSON](R162_EXACT_RESULTS.json) and [original-source ZIP](R162_Prestige_Cue_72_Worlds_99_Tests.zip) into main at [archive commit6600e68](https://github.com/edwardsage419/Psychohistory-Research/commit/6600e6829a707310281e678928edb55f737aec39).
* **495 actual unit test executions across the two runs, 99 distinct tests, zero failures**. Test repetitions are computational replication only.
* SHA256 source `261738a8d2a53f649157d04f79ae198b6d96553cca5daabbbe32727b350382ff`; tests `fb83f7d68f2ce3d34083f81543153ac8617c1bd77c20c1f30ad5fee083f364ea`; JSON `405ee44d302da5ba79ea31a8df2c364a6bd7712eed85d120d48a42c4860cd264`; ZIP `d9b39445b6b632a7fd86d120a7a7cd18f2a665572109f777e9031dfdf1d0c660`.
* Replay from `research/R162`: `python r162_prestige_attention_exact.py > R162_EXACT_RESULTS.json`, then `python -m unittest -q test_r162_prestige_attention_exact.py`. Standard Python library only.

**CLOSED_BOUNDED_E1** for frozen 72 mathematical cue lotteries and source conceptual audit. Zero newly obtained real-person independent behavior evidence E2; zero historical external-event forecast E3. R073 and PESEN v0.1 remain FROZEN. According to original catalog, continue R163 **P1/07-005 Success Biased Transmission**. All R models precede unified categorization and fusion.
