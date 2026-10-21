# R164 scientific report: content salience, frequency, content-copying strength and artificial replacement

2026-10-21. Original **P1 / 07-006 Content Biased Transmission**. Precomputation protocol [frozen at 5c403e6](https://github.com/edwardsage419/Psychohistory-Research/commit/5c403e61c2d0cdfb8dbdd8982e3c3e621df51b95), before any program code or results. **Status CLOSED_BOUNDED_E1**, confined to an original synthetic two-token frequency process. No direct inference about human recall, actual attention, religious memory, survival content or real cultural behavior.

## First-hand article records and empirical access limits

* Barrett and Nyhof (2001), *Spreading Non-natural Concepts: The Role of Intuitive Conceptual Structures in Memory and Transmission of Cultural Materials*, *Journal of Cognition and Culture* 1(1):69–100, DOI [10.1163/156853701300063589](https://doi.org/10.1163/156853701300063589); [Oxford university publication record](https://ora.ox.ac.uk/objects/uuid%3Aa6ed93bb-3ba0-4934-adec-9bb827cf8e9f). Authors' abstract reports recall/transmission advantages for some expectation-violating items in experiments. No trial-level narrative material or original observer recall values were acquired or independently scored.
* Boyer and Ramble (2001), *Cognitive templates for religious concepts: cross-cultural evidence for recall of counter-intuitive representations*, *Cognitive Science* 25(4):535–564, DOI [10.1016/S0364-0213(01)00045-3](https://doi.org/10.1016/S0364-0213%2801%2900045-3); [Elsevier publisher original abstract](https://www.sciencedirect.com/science/article/pii/S0364021301000453) and [Wiley journal record](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog2504_2) examined. Published studies distinguish domain-level expectancy violations, inferential opportunities and basic-level violations. They show that **content features cannot all be reduced to one universal monotonic salience coefficient**. Original narratives, three-country participant responses and author estimators have not been replicated.
* Stubbersfield, Tehrani and Flynn (2015), *Serial killers, spiders and cybersex: Social and survival information bias in the transmission of urban legends*, *British Journal of Psychology* 106:288–307 DOI [10.1111/bjop.12073](https://doi.org/10.1111/bjop.12073), [Wiley original abstract](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjop.12073). The original separates choosing to receive, encode and retrieve, and choose to transmit. Real experimental story transmission paths or effect sizes were not obtained.

None of the above supplies measurements for our invented multiplier. R164 implements a **project-defined normalized content selection weight**. It is not a reproduction of any author psychological model and does not prove that any particular category of real-world information is more memorable or desirable.

## Freeze 72 exact toy copying histories

Artificial content A frequency p in [0,1], versus token B with frequency 1−p. Initial p∈{1/5,2/5,3/5,4/5}. Artificial A content weight r∈{1,2,4}; social copying share h∈{0,1/2,1}; symmetric independent replacement e∈{0,1/4}. **4×3×3×2=72 different frozen worlds**, each with five exact time values t=0..4, as well as each period's content-weighted probability and before-replacement copying rate. All values are exact rational numbers. [Complete 89,087-byte JSON](R164_EXACT_RESULTS.json) retains the full original experimental output.

For this project, content-biased copying probability of A is
\[
S(p,r)=\frac{rp}{rp+(1-p)},\quad
q=(1-h)p+hS(p,r),\quad
p_{t+1}=(1-e)q+e/2.
\]
These equations and replacement semantics were **invented here**, with no measured psychological parameters or observed participants.

Two independently implemented exact Fraction methods:
1. Direct rational normalization and recurrence.
2. Separate A versus B weighted urn masses, then independent random-sampling and content-sampling mixture channels plus a symmetric replacement channel. The oracle does not call the direct-step solver.

All **72 × 5 frozen frequency states** agree by strict rational equality across both implementations. Source tests also checked exact normalization, positivity, finite scenarios, invalid-input rejection, and each transition in full JSON.

## Mathematical hypotheses and counterexamples

1. When r=1, content selection reduces exactly to random selection S(p,1)=p, regardless of h. With e=0, p stays constant.
2. When h=0, the r coefficient has **zero effect on any frequency path**, so observing even a full such trajectory cannot recover r. If e=0, p is constant regardless of r. If h=0,e>0, the path follows the exact closed form \(p_t=1/2+(1-e)^t(p_0-1/2)\).
3. When r=4 and p0=1/5, the selected content rate is exactly S=1/2; this is a synthetic reweighting of a minority token, not evidence that uncommon human stories spread in a particular way.
4. With h=1, e=0, content odds multiply by r each round: \(p_t=r^t p_0/[1-p_0+r^t p_0]\). For r>1, p strictly increases from any interior start in the artificial model and remains strictly below one for every finite generation.
5. **Frozen counterexample to simple popularity inference**: initial p=4/5, r=2, h=1, e=1/4. Salience-weighted p becomes 8/9 before replacement; next p=(3/4)(8/9)+1/8=**19/24 ≈ 0.791667**, below the original 4/5. Therefore adding one favorable content sampling coefficient cannot be interpreted as guaranteed net frequency growth when further transformation processes occur.
6. A higher adoption share can improve or harm hypothetical correctness depending on externally specified content truth and local task requirements. This experiment does not assign a true quality to A or B, since no author paper establishes a universal quality ordering.
7. The original human-memory papers involve different experimental stages (receiving, retaining, transmitting) that are collapsed into a single artificial recurrence here. The simplified mapping lacks external validity and cannot be used to rank real content items, people or groups.

## Verification, immutable artifacts and research closure

[Program](r164_content_salience_exact.py), [102 genuine unittest methods](test_r164_content_salience_exact.py): 72 individually named cases and 30 boundary, exact odds, identification, and negative input/data replay tests.

* [First GitHub Actions run39529224497](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39529224497) passed 102 tests separately under Python 3.11 and 3.12. Both produced identical source, tests, JSON and ZIP SHA256.
* [Pinned dual-runtime run39529293414](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39529293414) passed the same 102 tests in both Python versions and directly matched all four immutable hashes.
* [Final archive run39529323641](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39529323641) passed the 102 tests per Python version; independent archive job118991385446 reran all 102, regenerated JSON and ZIP, matched four SHA256 and permanently committed them to main at [archive commit ccb1f2f](https://github.com/edwardsage419/Psychohistory-Research/commit/ccb1f2fa8be0075a43d1e47a8d85708b8901a9ee).
* **714 executed unittest methods across seven invocations; 102 distinct tests; zero failures**. These are computational reproducibility checks, not independent original human study evidence.
* SHA256 source `27252e908413335780e43f8bb4bb089d2abb0cd4ba31cc2967d63480f6f89133`; tests `a5dc28d23e8ed11f3c3b6b4ec3b8bd3e8d5d8ff3d6ef1e7ccc85f4666b84b013`; full JSON `ce27a70aee6ee82ca360efc93b12632c44f6bbd7a73b32bf1aaafc602df69f52`; original [complete ZIP](R164_Content_Salience_72_Worlds_102_Tests.zip) `271beda59c738310a608b7e65eb88f9144159d40441aef180ddf7aa11b4f3e55`.
* Reproduce from `research/R164`: `python r164_content_salience_exact.py > R164_EXACT_RESULTS.json` followed by `python -m unittest -q test_r164_content_salience_exact.py`. All standard library.

**Formal acceptance CLOSED_BOUNDED_E1** for 72 synthetic frequency scenarios with exact arithmetic and bounded concept review. New person-level independent out-of-sample evidence E2=0, real historical replication E3=0. R073/PESEN v0.1 remain frozen. The next original directory candidate is **R165 P1 / 07-007 Neutral Cultural Drift**, verified from original model catalog; proceed through the R series before classification or fusion.
