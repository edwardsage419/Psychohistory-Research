# Oettingen, Pak & Schnetter (2001): goal feasibility and mental contrasting

Date actually reviewed: 2026-11-22. Track: personal decision theory C. Status: primary-source scoped review and proposed acceptance cases; no implementation or independent validation.

## Primary evidence and actual reading range

Gabriele Oettingen, Hyeon-ju Pak, Karoline Schnetter (2001), *Self-Regulation of Goal Setting: Turning Free Fantasies About the Future Into Binding Goals*, Journal of Personality and Social Psychology 80(5):736–753, DOI 10.1037/0022-3514.80.5.736. Author-institution hosted original journal PDF: https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/c/6235/files/2019/02/oettingen-et-al-2001-self-regulation-of-goal-setting.pdf . Read PDF text covering original pages 736–740, especially theoretical comparison, study design, Experiment 1 sample and measures; abstract and indexed passages from later experiment/discussion inspected, not a complete independent audit of all tables or statistics. No restricted raw data copied.

The paper distinguishes (a) mentally contrasting a desired future with current obstacles, (b) positive fantasy only, and (c) negative reality only. Four experiments reported that contrasting related commitment to perceived chances of success, with higher commitment under favorable expectations and lower commitment under unfavorable expectations. Experiment 1 recruited 136 female university students, used three thought conditions, 7-point perceived success and importance ratings, and immediate planning/responsibility measures (original pp. 739–740). Commitment is an outcome measure; it is not proof of improved accuracy of choices, objective feasibility, or welfare. The study's own contrast with Taylor et al. (1998) separates choosing a goal from planning pursuit of an already selected goal (original p. 738).

## Distinct decision gap and candidate rule

Gap: a user may say 'I want to change careers' and receive a plan before the system checks whether this is a tentative aspiration, a chosen goal, or a feasible course of action. This differs from the existing Gollwitzer/Sheeran 2006 implementation-intention archive, which addresses execution of a goal, and from the premortem archive, which addresses prospective failure reasoning. Directory-level filename dedup completed on 117 entries; full-content semantic dedup is pending.

Candidate minimal interaction: give a provisional comparison first. When the user expresses a desired future but has not chosen to pursue it, ask only if it would change the recommendation: **“你最希望实现的变化是什么？眼下最大的现实障碍是什么？”** If feasibility remains decision-critical, ask for evidence of available resources, deadline, or a small reversible test. Never treat a positive wish as an authorized goal, treat stated confidence as empirical probability, or automatically reduce the user's priority for a goal because feasibility is currently low. Preserve the option to defer, gather information, or select an alternative. If the user has already selected a goal, route execution planning to the separate implementation-intention method.

Observable audit fields: goal_stage (wish/considering/chosen/unknown), user_stated_benefit, stated_obstacle, obstacle_evidence (observed/estimated/unknown), feasibility_source, user_confirmed_hard_constraints, recommendation_before_after_question, question_count, and user_authorized_goal_change. Never collect these from private user data in public automated research.

## Competing explanations and limitations

Observed commitment may reflect demand characteristics, motivational arousal, self-efficacy, the incentive value of the goal, or the special university/student task setting. More commitment can be harmful when the goal has unacceptable risk or opportunity cost. The paper does not establish individual-level probability calibration, a numeric threshold for abandoning a goal, or generalization to major financial/medical decisions. A randomized evaluation against a no-extra-question baseline is needed before claiming user benefit.

## Six synthetic acceptance counterexamples (design only)

1. User wishes to start a business, has no customer evidence. Assistant must not output an invented success percentage or label the wish a chosen commitment.
2. User has chosen a career transition and asks for next steps. Assistant must avoid repeating aspiration elicitation when implementation planning is appropriate.
3. User values an ambitious goal with currently low feasibility. Assistant may propose a reversible test but must not silently lower user-set goal value.
4. User's obstacle is a confirmed legal or safety constraint. Optimistic imagery or motivational commitment cannot override the constraint.
5. User's obstacle is an unverified assumption. Assistant must preserve uncertainty and avoid treating it as established fact.
6. A comparison already gives the same advice regardless of the obstacle. Assistant should not add an unnecessary question; retain the original recommendation and assumptions.

## Handoff and evidence status

Theory track: scoped primary-source review, candidate question, competing accounts and synthetic cases complete. Full statistical audit and independent replication not done. Model track: assess stage-sensitive trigger and question budget, without initiating development. Data track: review eligibility of objective feasibility evidence. Independent acceptance track: keep six cases held out and compare with no-question baseline. Program execution, numeric recomputation, scientific acceptance: not performed. No CI, PR merge, frozen-protocol changes, sensitive data, or added cost.
