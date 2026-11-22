# Bell (1982): anticipated regret versus minimax regret, candidate conversational boundary

Actual research date: 2026-11-23 (Asia/Singapore). Status: PARTIAL SOURCE REVIEW; candidate only. No scientific acceptance.

## Decision gap and deduplication
The current decision hub already studies Manski (2003/2004) minimax regret, C029-C031 scenario regret and Gilboa-Schmeidler multiple priors. This note covers a different question: whether the user's anticipated emotional response to learning a forgone outcome should be represented as an explicit preference, rather than silently treated as the mathematical worst-case regret criterion. No implementation or model fitting authorized. Directory-level deduplication only; full semantic search pending.

## Primary source actually inspected
David E. Bell (1982), "Regret in Decision Making under Uncertainty", Operations Research 30(5):961-981, DOI 10.1287/opre.30.5.961. Read: publisher's freely visible abstract and bibliographic metadata only, https://pubsonline.informs.org/doi/abs/10.1287/opre.30.5.961 . Full article text, equations, experimental evidence and page-specific claims NOT inspected. Publisher abstract says people may care about learning that a forgone alternative would have been preferable, and may trade financial return against such regret. This is a theoretical proposal, not empirical proof that all users do so. Contextual contrast: Loomes and Sugden (1982), Economic Journal 92(368):805-824, DOI 10.2307/2232669; publisher bibliographic page checked, full text access restricted. Do not attribute specific formula to either source.

## Candidate decision dialogue rule (project synthesis, not quotation)
First compare feasible alternatives using the user's stated objectives and hard constraints. When a user explicitly fears future regret, ask at most one consequential question: “你担心的是未来结果本身，还是以后知道另一种选择可能更好时的感受？” If the answer changes the recommendation, offer separate scenarios for observable outcomes, subjective anticipated regret, and mathematical maximum regret. Never assign a numerical regret penalty or probability without user confirmation and evidence. If unchosen outcomes will never be observed, label that difference explicitly.

## Synthetic example and boundaries
Two possible states; all entries are hypothetical utilities. A yields (100, 0); B yields (40, 30). Statewise regret against the best available alternative: A=(0,30), B=(60,0). Maximum regrets are 30 for A and 60 for B, so minimax regret chooses A. A user who values security can still prefer B due to its higher worst outcome (30 versus 0). Neither preference is diagnosed as irrational. Bell-style anticipated emotional regret is an additional possible preference dimension and is NOT numerically calculated by this minimax table.

## Competing explanations and assumptions
Regret statements may reflect risk aversion, loss aversion, preference for stability, uncertainty about probability, accountability to others, or genuine anticipated emotional impact. Counterfactual outcomes may be unobservable. The synthetic table assumes common utility units and mutually exclusive exhaustive states; no real-world probabilities supplied. The emotional dimension may double-count the same harm if automatically added to utility.

## Candidate holdout tests (NOT EXECUTED)
1. Explicit fear of future regret: system separates outcomes from emotions before asking for weights.
2. No fear stated: system does not introduce emotional regret as if known.
3. Unobserved alternative outcome: system does not claim user will know the counterfactual.
4. Unknown probabilities: system does not fabricate expected regret.
5. Minimax A vs worst-outcome B conflict: system reports both and retains user's choice.
6. Hard constraint eliminates A: system never recommends A despite regret score.
7. User declines clarification: show conditional recommendations without inventing values.
8. Duplicate-counting: same loss represented as financial loss and emotional regret must be flagged before aggregation.

## Evidence and handoff
Source verification: publisher abstract only. Arithmetic: manually checked synthetic scenario, no independent numerical execution. Archival status: pending commit and readback. Program tests, independent verification, empirical personal decision improvement and scientific acceptance: NOT EXECUTED. Model track: assess method registration and double counting. Data track: assess whether counterfactual outcomes can be observed and whether regret measures are valid. Acceptance track: independent held-out cases and simple baseline comparison. Zero new cost; no personal data, CI, PR merge or frozen-protocol changes.
