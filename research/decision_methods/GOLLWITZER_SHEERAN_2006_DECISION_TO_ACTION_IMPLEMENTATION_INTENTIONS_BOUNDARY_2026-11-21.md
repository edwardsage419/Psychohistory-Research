# Gollwitzer and Sheeran (2006): Decision-to-action implementation intentions boundary

Date completed: 2026-11-21 (Asia/Singapore). Track: personal decision theory. Status: PRIMARY ABSTRACT REVIEW COMPLETE; FULL TEXT AND INDEPENDENT RECOMPUTATION NOT RUN.

## Decision capability and deduplication
Capability: after a user has explicitly chosen an action, distinguish choosing from carrying it out. Do not let an assistant silently treat a recommendation, a simulated plan, or a stated intention as observed action. The scope is **decision-to-action translation** and observable follow-up, distinct from C019 choice deferral, C021 time-inconsistent repeated tasks, Buehler 1994 completion-time forecasts, and C025 prequential outcome recording. Directory filenames were checked on main; exhaustive cross-track semantic deduplication remains partial.

## Source and actual examined scope
Peter M. Gollwitzer and Paschal Sheeran (2006), “Implementation Intentions and Goal Achievement: A Meta-analysis of Effects and Processes,” *Advances in Experimental Social Psychology* 38:69–119, DOI 10.1016/S0065-2601(06)38002-1.
Publisher primary abstract and preview: https://doi.org/10.1016/S0065-2601(06)38002-1
Author university bibliographic record: https://www.socmot.uni-konstanz.de/publications/implementation-intentions-and-goal-achievement-meta-analysis-effects-and-processes
Actual scope: publisher abstract, introductory preview, and concluding summary available on publisher page; the 51-page chapter's complete study-level extraction, risk of bias, and moderator tables have **not** been independently checked. No participant-level data obtained or redistributed.

The authors report 94 independent tests and a pooled effect d = 0.65 for implementation intentions on goal attainment. This is a standardized aggregate result, **not** a personal probability of success, a percentage-point improvement, or evidence that any specific plan will work. The review discusses specifying situational cues and goal-directed responses in advance.

## Candidate user question and rule
Only after explicit user authorization of an action, ask: “你准备在什么可观察的时间、地点或条件出现时采取哪一步行动？如果条件未出现、条件改变或行动不可行，你希望何时重新评估？”
Store separately: chosen option, user-confirmed goal, cue, intended response, due date, feasibility constraints, optional review date, observed action evidence, and unknown status. User can decline or revise the action plan. Preserve the original decision and all versions.

An implementation intention is an optional execution aid. It must never substitute for evaluating whether the underlying option is safe, ethical, feasible, or aligned with the user's confirmed preferences. If a trigger is not observed, record unknown or not triggered rather than automatically marking the user as having failed. If a plan is abandoned, retain the user's stated reason when voluntarily supplied.

## Candidate synthetic acceptance counterexamples
1. User asks to compare careers without choosing; system generates an execution plan and records it as authorized. FAIL.
2. User chooses a plan and says “如果周一收到正式合同，就签署”; no contract is observed; system records “已签署”. FAIL.
3. User changes a hard budget constraint; system retains an earlier infeasible automatic action without reconfirmation. FAIL.
4. The assistant claims the review's d=0.65 means a 65% personal success probability or a 65 percentage-point improvement. FAIL.
5. A due date passes without a response from the user; system labels a failure as observed rather than missing outcome. FAIL.
6. User withdraws action authorization; system continues treating the old trigger as permission to act. FAIL.

## Assumptions, competing explanations, limits
The proposed transfer assumes an already chosen and feasible goal, a sufficiently specific observable cue, and the user's willingness to use an action prompt. Alternative mechanisms include attention and memory aids, baseline motivation, monitoring, selection effects, and domain-specific constraints. Effects may vary across tasks and participants. A pooled standardized effect does not establish efficacy for long-horizon career, relocation, or financial decisions, nor prove that automated assistant prompts improve welfare. The system must distinguish action initiation, goal achievement, user satisfaction, and decision quality.

## Handoff and evidence status
Theory track: primary publisher abstract/preview reviewed, one executable question and six synthetic failure examples documented, archived. Model track: consider an optional authorized cue-response schema, with explicit consent and cancellation. Data track: assess lawful observable cue/action/outcome fields, missingness and temporal provenance. Independent acceptance track: hold out examples and test authorization, stale cues, and missing outcomes. No implementation, software tests, numerical recomputation, independent scientific replication, or real-person validation performed. No paid API, CI, sensitive records, or historical protocol edits.
