# Hsee (1996): joint versus separate evaluability in personal decisions

Actual research date: 2026-11-21. Track: personal decision theory. Status: primary-paper targeted review and candidate acceptance preparation; no program test, independent participant-level replication, or scientific acceptance.

## Source and scope
Christopher K. Hsee (1996), *The Evaluability Hypothesis: An Explanation for Preference Reversals between Joint and Separate Evaluations of Alternatives*, Organizational Behavior and Human Decision Processes 67(3), 247–257. DOI: 10.1006/obhd.1996.0077.
Public original journal reproduction: https://pages.ucsd.edu/~cmckenzie/Hsee1996OBHDP.pdf
Reviewed original article introduction, Study 1 through Study 3 methods/results and Study 4 design, corresponding to printed pages 247–253; remaining Study 4 numerical results and final discussion require separate review. No restricted participant data redistributed.

## Observed original-paper evidence
Study 1: 116 unpaid college students, joint WTP for dictionary A/B approximately $19/$27, separate WTP $24/$20. Reported reversal contrast t=4.56, p<.001. Separate A versus B comparison t=1.69, p=.1, hence its direction is descriptive and not independently significant at 0.05.
Study 2: 112 college students. Two hypothetical programmer candidates; joint WTP salaries A/B $31.2k/$33.2k, separate $32.7k/$26.8k. Reported reversal contrast t=4.94, p<.001; joint A/B contrast t=1.65, p=.1. Evaluability ratings GPA 3.7, experience 2.1.
Study 3: 98 college students. TV attributes clarity and warranty; when warranty rating was made interpretable as months, joint versus separate evaluations showed a reversal contrast t=3.47, p<.01. The separate A/B difference itself had p=.12. The hard/hard condition showed no such reversal.
These are original author-reported experimental findings, not independently recomputed statistics. A joint/separate comparison uses different evaluation contexts and between-person comparisons; it does not establish that every individual's preference will reverse.

## Distinct decision-system gap
Earlier Lichtenstein & Slovic (1971) file addresses choice versus monetary pricing. This study holds the response scale (WTP) constant and varies whether options are seen side by side. Earlier framing and option-visibility files address presentation and hiding; this candidate specifically audits whether a hard-to-interpret attribute becomes evaluable after comparison and whether a ranking change is wrongly attributed to changed personal values.

## Candidate question and explanation rule
When a user gives a single option a low score but later favors it in a side-by-side comparison, ask: "Did you learn what the unfamiliar metric means, did the comparison supply a useful reference, or did your priorities actually change?"
Record evaluation mode (single or joint), alternatives visible, attribute units, reference ranges, question wording, time and confirmed weights. Preserve each original response. Do not silently revise user weights or assert that the later judgment is inherently correct. A numerical range alone is not proof of predictive validity.

## Synthetic holdout candidates, not executed
1. With identical options, units and user-confirmed weights, changing single-option to side-by-side display must not silently mutate stored objective facts or confirmed weights.
2. An unfamiliar attribute such as a technical quality index has no known benchmark. System must flag interpretability unknown and must not assign a population percentile.
3. When a benchmark is supplied, system must retain source and benchmark applicability; a benchmark for another population cannot be silently transferred.
4. A user's two original ratings disagree across evaluation modes. System must preserve both, request clarification and label the cause unknown until confirmed.
5. A contrast p<.001 for reversal is incorrectly rendered as evidence that separate-condition A/B difference is significant; reject this interpretation (Study 1 separate p=.1).
6. Joint comparisons involving a newly visible option must preserve the user's right to view all options and undo display filtering.

## Competing explanations and limitations
Contextual comparison, norm/reference effects, response construction, salience, anchoring, learning, measurement error and true preference change may each explain some differences. Original experiments use hypothetical products and student participants; transfer to high-stakes career, family or relocation choices is unvalidated. The author-selected examples do not prove a universal causal mechanism. The 2001 González-Vallejo and Moran paper (DOI 10.1006/obhd.2001.2953) explicitly adds attribute importance as a moderator; its publisher abstract was checked, full text/statistics not independently verified.

## Handoff
Independent acceptance track: design withheld paired display-mode cases with constant facts and weights; check no overwrite and no unwarranted significance claims.
Model track: consider recording evaluation mode and attribute interpretability separately from utility weights, only after owner authorization.
Data track: evaluate benchmark provenance and portability before using external distributions.
No implementation authorization, CI, PR merge, original R073/PESEN v0.1 or frozen-protocol change. Zero new spending.
