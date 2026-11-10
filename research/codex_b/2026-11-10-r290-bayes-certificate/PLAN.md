# R290 S86 exact Bayes minimum and learned-rule law certificate

Base main25bcd51dd58bf0c245ae84c563406e679a966b5a. Dedicated branch
codex-b/r290-s86-bayes-certificate-20261110; only this directory changes.

Actual normal oldB CLI accepts coordinated false oracle/regret and wrong ignored
baselines. In MONOTONE pi1/2 FP=FN=1,m1,heldout188/441: settingoracle188/441 and
regret0 falsely labels learned rule Bayes-optimal, still all7oldcontrols reject.
True optimum5/21, regret83/441. Oracle0/regret188/441 also passes, as do cutoff999
and baseline999. Original archived values correct; oldBexpectedrisk is correct.
KnownoldBassert-O/worldcoverage limitations already documented; not our primary
discovery. No changes to original R/B/frozen models or baselines.

Independent algorithm: five-bit decision masks enumerate all32 binary rules.
Use integer class/cost risk numerator vector, minimum plus attaining masks gives
exact Bayes certificate (12configurations). Six cutoff masks, smallestt tie and
constant masks certify baselines. Aggregate complete1950training ledger into
32-bin learned-rule weight law for24world/m combos; calculate heldout risk by
integer dot product, regret by nonnegative minimum-gap sum. This differs from
R per-sample Fraction risk loop and oldB per-bin binomial marginal calculation.
Strict complete273leaf result contract,144risk/baselinefractionfields,exact24keys,
CSV identities/masses/shapes/types. Input correctonarchive independent proof.

TDD12new methods; original4unittest methods normal/-O (32total final methods).
Eight badartifactCLIcases:5oldfalseaccepts,2oldJSONcorrectrejects,1oldCSVcorrect
reject; newrejectall8. OriginalR --emit JSONstdout byteidentity; no original CSV
emitter exists, do not invent one. Existing B JSON+ledger CLIs run isolated NORMAL
Python in both modes (explicitly no claim oldasserts remain activeunder-O).
Record native old12negative controls separately, sourcepins,rawlogs/certificates.
Onefreshreview, latestmain/PRscope,independentdraft[skipci],no merge/paid/CI dispatch.

- [x] RED/GREEN32-rule optimizer, learned-law and full result contract.
- [x] Real normal/-O replay, originaltests/nativeJSON and old/new badcases.
- [ ] Onefreshreview and fixes if required; scope/report/handoff.
- [ ] Refreshmain/PRs, draft delivery/attach and all-eventsCI observations.
