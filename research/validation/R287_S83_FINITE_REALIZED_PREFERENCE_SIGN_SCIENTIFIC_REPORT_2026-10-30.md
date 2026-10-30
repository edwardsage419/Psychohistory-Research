# R287 S83: finite-sample realized preference signs under common consequences
Date: 2026-10-30 UTC. Track R. Status: NEW_SUBSTUDY_PARTIAL, E1 artificial internal nonblind.
Prescore freeze commit: 254b5f73c86a18d55a11c68118bd1d0fc77ce80c. The original R287 CLOSED_BOUNDED_E1 status remains unchanged.

## Source, scope, and procedure
Original R287 source and freeze were read before S83. Original 2304-source CSV Git blob ddf3ae0b924016a3a8aac7253a1a6a9b44d864d1, SHA256 84d8000d0ed2683a77b12a9e47a43d013960b9a95198457beac9aa5acef1d080. Original vNM literature pointer: von Neumann and Morgenstern (1944), *Theory of Games and Economic Behavior*, Princeton University Press. No claim to a new empirical result about human preference.
The R route read all 2304 original CSV rows, independently reconstructed each source probability and realized utility difference, preserved every ordered eight-bit source, and classified the sign of the four-opportunity average. Three fixed artificial utility profiles and lambda in {1/4,1/2,3/4} produce nine worlds of 256 sources each. Exact integer arithmetic was used for all masses and signed differences. Source coverage, mass, and four negative controls (duplicate, missing, altered mass, altered sign) passed.

## Exact probabilities
All numbers are exact fractions; WRONG means strictly opposite the sign of the *population* expected utility difference, TIE means the realized four-opportunity difference equals zero. The population sign never reverses under the common consequence mixture.

| Profile | lambda | P(correct) | P(wrong) | P(tie) | P(wrong given non-tie) |
| --- | --- | --- | --- | --- | --- |
| LINEAR | 1/4 | 2499/4096 | 1581/4096 | 1/256 | 31/80 |
| LINEAR | 1/2 | 147/256 | 93/256 | 1/16 | 31/80 |
| LINEAR | 3/4 | 1619/4096 | 1181/4096 | 81/256 | 1181/2800 |
| SQRT_ON_SQUARES | 1/4 | 2499/4096 | 933/4096 | 83/512 | 311/1144 |
| SQRT_ON_SQUARES | 1/2 | 147/256 | 69/256 | 5/32 | 23/72 |
| SQRT_ON_SQUARES | 3/4 | 1619/4096 | 1109/4096 | 171/512 | 1109/2728 |
| SATURATING | 1/4 | 3147/4096 | 609/4096 | 85/1024 | 203/1252 |
| SATURATING | 1/2 | 171/256 | 65/256 | 5/64 | 65/236 |
| SATURATING | 3/4 | 1691/4096 | 1105/4096 | 325/1024 | 1105/2796 |

One bounded counterexample: in SQRT_ON_SQUARES, P(strict wrong sign) rises from 933/4096 to 1109/4096 as lambda increases from 1/4 to 3/4, although the underlying expected utility ordering remains fixed. For SATURATING the corresponding increase is 609/4096 to 1105/4096. Ties also increase, so conditional and unconditional reversal probabilities must be distinguished. For LINEAR, unconditional wrong probability decreases while the tie probability increases. A positive affine utility recoding 3u+7 preserves all categories.

## Evidence, negative cases, and acceptance
R source: research/validation/r287_s83_original_source_signs_20261030.js.
Full 2304 derived receipt: research/validation/R287_S83_ALL_2304_SIGN_RECEIPTS.csv.
Exact result: research/validation/R287_S83_EXACT_RESULTS.json.
Independent B route: multinomial counts of common, noncommon-low and noncommon-high outcomes, 15 count cells per world; nine exact result objects agree. Remote persisted 2304 derived rows were checked for uniqueness, complete coverage, source mass, realized difference, and category. B native Python exact multinomial CLI passed; original R archived Node native CLI was NOT_RUN. Four negative controls were rejected by the R strict checker. No outside team independently replicated this result.

A01 PASS bounded artificial question; A02 PASS original fixed source blob; A03 PARTIAL (V8 execution and independent Python mathematical route, original Node native CLI NOT_RUN); A04 PASS four mutations and retained ties; A05 PASS explicitly E1; A06 PARTIAL pending full native replay and external review. New S83 scientific acceptance PARTIAL. Original R287 bounded acceptance unchanged. E2 new predictions 0; E3 new predictions 0. R073 and PESEN v0.1 remain FROZEN. No Actions were initiated, and no paid resources were used. Account billing was not independently inspected.
