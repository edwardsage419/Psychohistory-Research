# R296 prescore freeze: original 02-001 Rescorla–Wagner shared error, cue blocking and unblocking

Date 2026-10-23 Asia/Taipei. Original 239 candidate item **02-001 Rescorla Wagner Learning Rule**, P1. This protocol must precede all R296 model execution and results. All stages E1 exact fully artificial mathematical re-derivations, zero new E2 or E3. R073 and PESEN v0.1 remain frozen, all original R learning precedes categorization/fusion.

## Original source and domain boundary

Robert A. Rescorla & Allan R. Wagner (1972), "A Theory of Pavlovian Conditioning: Variations in the Effectiveness of Reinforcement and Nonreinforcement", in Black & Prokasy (eds.), *Classical Conditioning II: Current Research and Theory*, pp.64–99, Appleton-Century-Crofts. Source authorship and bibliographic confirmation: original author Allan R. Wagner's Yale page https://wagner.yale.edu/publications ; scanned original chapter: https://www.columbia.edu/~rk566/Session4/Theory%20of%20Pavlovian%20Conditioning.pdf . Learning rule posits a *shared compound prediction error*, unlike independent per-stimulus error model used solely as constructed negative-control. Our numeric design below is an artificial finite example, not published author animal outcome counts or empirical effect-size reproduction. Existing reinforcement-learning R series may share parameters/formula; original catalogue evidence assignment remains item-specific, no double count of any earlier real dataset.

## Fully fixed synthetic trials

Two cue association strengths V_A,V_B initially zero. Cue associability α_A=α_B=α∈{1/4,1/2}, outcome salience β=1. A-only pretraining condition n_pre∈{0,8} trials with reinforced target λ=1; only present A updates by ΔV_A=α*(1−V_A). After pretraining, AB compound receives target reward λ_comp∈{1,2} for m∈{0,1,2,3,4} trials. In the Rescorla–Wagner model, each present cue receives the **same compound prediction error**: V_A' = V_A+α*(λ_comp−V_A−V_B), V_B'=V_B+α*(λ_comp−V_A−V_B).

As mathematically distinct independent-error negative control, pretraining A is identical; in compound trials each cue learns its own λ residual: U_A'=U_A+α*(λ_comp−U_A), U_B'=U_B+α*(λ_comp−U_B). This competitor is not asserted as an original author-implemented independent theory, nor is it given extra data; it receives the exact same frozen trial schedule.

Universe: 2 α × 2 pretraining × 2 compound reward shifts × 5 compound stage lengths **40 fully labeled artificial source rows**, exactly 8 unique worlds with all 5 stage indices, including m=0. Rows store α, n_pre, λ_comp, m, pretraining A strength, RW current A/B, shared total/remaining error, independent-control current A/B, action/source provenance; all Fraction and deterministic. Trial trajectories must be reconstructed from scratch, no random sources, data fitting, outside reward, or synthetic human participants.

## Pre-specified analytic claims

Let p=1−(1−α)^n_pre denote A pretrain strength. After m compound trials:
RW_B(m)=(λ_comp−p)/2 * [1−(1−2α)^m].
RW_A(m)=p+RW_B(m).
RW_SUM(m)=λ_comp+(p−λ_comp)*(1−2α)^m.
IND_B(m)=λ_comp*[1−(1−α)^m].
IND_A(m)=λ_comp+(p−λ_comp)*(1−α)^m.

Confirm all exact Fraction equations, for all 40 source states. RW compound error is always λ_comp−(RW_A+RW_B), all stage masses are deterministic *states*, not joint probability observations.

Blocking: for both α, after 4 compound λ_comp=1 trials, RW B associative strength after 8 pretraining A trials is **strictly less** than B after 0 A pretraining. For α=1/2 p=255/256 and m=4, RW B trained=1/512 versus no-pretrain 1/2, whereas independent-control B for either pretraining is 15/16. This is formal cue competition, not automatically true in all real learning.

Unblocking/reward upshift: with n_pre=8 fixed, RW B learning after m=4 and λ_comp=2 is strictly larger than after λ_comp=1 (both α). Independent-control B remains pretraining-insensitive, but responds to outcome magnitude. α=1/2 λ_comp=2 RW B=257/512 (using pretrain p=255/256). α=1/2 RW total immediately reaches compound target after one compound trial; any further exact changes are zero.

No pretraining and m=0 must have RW_B=IND_B=0, independent model and RW must be compared at the identical complete schedule. Include independent negative/tamper tests for all state rows, analytic formula agreement, original source/JSON SHA256.

## Gates

Python 3.11/3.12 source-code unit tests, main --emit and --test, all 40 original source CSV, eight-world 5-point exact results, machine SHA receipt, independent source auditor which never imports the main code, adverse tamper tests, three-job observed successful GitHub Actions, permanent Git main source archive, formal scoped E1 acceptance then only original catalogue 02-001 update to v1.0 from v0.9 and queue -1. Source provenance linkage is not empirical validation. Next original 02-003 Q Learning remains independently pending. Do not modify R073 or PESEN v0.1.
