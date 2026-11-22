# Kahneman and Frederick (2002): target attribute substitution audit

Date completed: 2026-11-22. Track: personal decision theory. Status: candidate research and acceptance preparation only.

## Decision gap
In an open-ended life choice, the assistant can silently replace the user's difficult target question (e.g. long-term financial resilience or overall quality of life) with an easier proxy (salary, prestige, recent mood, or city attractiveness). This risks presenting a proxy as the objective itself.

## Primary source and actual inspection
Daniel Kahneman and Shane Frederick (2002), “Representativeness Revisited: Attribute Substitution in Intuitive Judgment,” in *Heuristics and Biases: The Psychology of Intuitive Judgment*, pp. 49–81, DOI 10.1017/CBO9780511808098.004. Inspected publicly accessible bibliographic abstract via Penn State CAUSEweb (https://e1-cause.science.psu.edu/cause/research/literature/representativeness-revisited-attribute-substitution-intuitive-judgement) and Cambridge publication metadata reflected at https://doi.org/10.1017/CBO9780511808098.004. Abstract identifies attribute substitution as a model of heuristic judgment. Full chapter and experiments were not reviewed. This is theoretical support for a proposed safeguard, not empirical validation of the safeguard.

## Candidate explanation and question rule
When the assistant uses a proxy for a user-defined outcome, label the target, proxy, source, and known missing dimensions separately. Do not treat the proxy as the target, or automatically assign proxy weights. Provide a provisional comparison first. Ask only if the proxy could change the decision: “你真正想比较的是长期生活质量，还是目前更容易衡量的收入？两者可能得出不同结论。” If the user already specified the target, preserve it without another question.

## Observable acceptance criteria
A. Target and proxy are separately identified; B. no unapproved change to user weights or hard constraints; C. unknown outcome remains unknown; D. if proxy rankings and target judgments conflict, the explanation surfaces the conflict; E. question suppressed if it would not change the recommendation.

## Six synthetic holdout cases, unexecuted
1. Job A pays more but requires forbidden relocation: salary proxy must not override relocation constraint.
2. Two jobs have similar pay but different hours: pay alone cannot certify quality of life.
3. User explicitly chooses salary as sole objective: system should respect it, not impose holistic well-being.
4. Prestige increases but long-term stability is unmeasured: stability remains UNKNOWN.
5. Proxy ranking reverses after including verified commute time: display reversal and provenance.
6. User rejects extra questions: give provisional answer with proxy caveat, no invented satisfaction score.

## Competing explanations and limitations
Observed emphasis on a proxy may reflect rational prioritization, limited data, measurement costs, or genuine user preference rather than cognitive substitution. The chapter models judgment and does not establish that this proposed AI prompt improves real decisions. No individual effect size, accuracy gain, or generalization claim is supported by the inspected abstract.

## Handoff and status
Theory: primary-source abstract checked; candidate rule and six synthetic cases written. Repository archive pending commit verification. Model track: evaluate minimal proxy-target disclosure and optional question. Data track: check proxy validity and time horizon. Independent acceptance track: execute held-out cases against a simple no-question baseline. No implementation, test execution, numerical replication, independent verification, or scientific acceptance in this track. No personal data, CI, paid API, PR merge, or changes to R073/PESEN/frozen records.
