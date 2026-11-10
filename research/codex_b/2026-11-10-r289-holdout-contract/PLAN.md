# R289 S85 heldout evaluation and tie-policy contract

Base main81188642a7d32d94d8cc4773785a3d2b89349ebb; dedicated branch
codex-b/r289-s85-holdout-contract-20261110, only this directory changes.

Reproduced native R source mutations, original files untouched:
1. Replace independent-test mixture with per-future-source maximum H3/H5 reward:
   compute/selftest exit0, all6 negative-control flags true. UNIFORMm1 claimed
   test reward331/81 instead8128/2187, regret-59/162. Forbidden future-informed
   policy evaluation rather than original legitimate fixed-policy test reward.
2. Replace strict>0 with>=0 in both direct selection and polynomial route:
   selftest exit0, incorrect_tie_rule still claims rejectedtrue; UNIFORMm1 H5
   probability67/81 rather25/81. Literal boolean check does not exercise selector.
Original archived computation correct. Old B previously independently checked
original outputs; do not claim its historical audit failed or new human leakage.

New independent algorithm: joint stopping-state dynamic program over four offer
stages, exact Fraction, no enumeration/import of R or old B. Derive paired reward
law, convolve training signed differences m1/2, then explicitly integrate fresh
independent joint-test law using strictly selected training policy. Full136-leaf
result contract incl60world fractions, six polynomial records, typed metadata/
historical flags. Match243 unique ledger sources by first-passage formula and
joint-law aggregation. Optional original486 source parity in replay, not DP input.

TDD12methods, exact hand anchors and independent81-source test oracle. Real source
mutants vs new artifact gate, plus single-route tie control correctly rejected by
originalselftest. Native R --emit in temporarycwd, B Python --test and sixworld
output; original byte identities. Ordinary/-O; old asserts under-O disabled, not
unittestcounts. Record source versions/commands/logs, all failures and scope.
No frozen model/parameter/split/metric/human score change; artificial nonblindE1.
One fresh-context review, latestmain/22PR scope refresh, independentdraftPRskipci,
attach/no automaticmerge/paidAPI/resources/workflowdispatch.

- [x] RED/GREEN independent DP and full artifact contract.
- [x] Ordinary/-O actual replay, source mutants/controls and native identities.
- [x] Review, necessary fixes, source/scientific limitations and handoff.
- [x] Latestmain/PR refresh, draft delivery and all-events Actions observation.
