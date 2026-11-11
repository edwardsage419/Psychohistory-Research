# R077 independent exact-score acceptance and human-readiness audit

track: Codex B; subflow: B1/B3 scientific-readiness
run_date:2026-11-11 UTC (user-facing date2026-11-11 Asia/Shanghai)
observed_head:ce6ae2dbf96f5346cf5062de3773b72c0ab90446
status:COMPLETE_NEW_SYNTHETIC_MATH_AUDIT / PARTIAL_HUMAN_READINESS
source_links: frozen R073/R077 protocols and17selected blobs in pins.json;
PR18/28/29, official Zenodo15462528, original R073 submission4743f74d.
work_performed: integer independent audit, two new single-event boundaries,
original donor-interface synthetic exercise, source/receipt qualification review.
evidence_scope: synthetic only; original functions on artificial inputs; public
source METADATA and historical receipts, no new human rows/scores/fit.
output_paths:this directory; commit_sha/PR inHANDOFF/final delivery.
ci_status:NOT_RUN; billing_checked:no paid API/install/purchase/dispatch,
free CI quotaNOT_VERIFIED. blockers/next_action: qualified double-run plan.

## Current state and distinct increment

PR18,28,29 are confirmed merged into main by another authorized workflow.
We did not merge them. OpenA30 changes two deployment-label strings only; its
scope is complementary. Frozen R073c8a0b47f and original R07770889bd1 remain
unchanged; B28 candidateb050fcf1 is callable but original production not replaced.
A29's opt-in synthetic shadow retains its production veto. Merged engineering
code is not scientific approval to revise the frozen real-human results.

Existing evidence is reused, not repeated: B18 four archived modes have40
selected source byte identities matching current files; B28 four modes have18
matching identities and64explicit raw stream hashes verified. Entries overlap,
not58independent sources. B18's command list lacks stream-hash fields: no claim
of separately authenticating all its raw streams. A29's11+13archive members
individually match their manifests. Previous35-order and71-method campaigns,
and A's engineering suite, were NOT rerun. Evidence/existing-evidence-check.json
distinguishes retained historical test status from this round's new execution.

## Independent INTEGER route and preserved scientific definition

integer_certificate.py imports no original/candidate code, Fraction or Decimal.
It counts the supplied artificial source rows into integer bins. For source
positivesC/countN and conditional positivesc/countn, exact model probability is
`(c*N+20*C)/(N*(n+20))`, reduced by gcd. M0=C/N; TFT/WSLS retain1/20and19/20.
These are the same frozen mathematical formulas. Original code instead rounds
C/N, intermediate multiply/add/divide and0.05/0.95 in binary floating arithmetic.
Exact mathematics is not claimed as bitwise equivalence to those intermediates.

History bins are independently encoded as own1,opp1,2*own1+opp1,and
8*own1+4*opp1+2*own2+opp2, matching the seven frozen families and four past bits.
For a session, takeD=lcm of exact probability denominators; squared-loss integer
sum isS=Σ(a_i*(D/b_i)-y_i*D)^2. Exact Brier isS/(n_session*D²). No float or
shared Fraction arithmetic enters this route. Average these rational risks with
LCMs over sessions, never over pooled rows. Pair signs use integer cross-products
between the two risks with positive denominators. Six comparisons are exactly
M3−M1,M4−M3,M1−M0,M2−M0,M5−M0,M6−M0. No tolerance or metric change.

Why source recovery works: every qualified source event enters exactly one M4
bin, so summing its integer counts givesC,N; projection gives the lower tables.
B28's checks guarantee this algebraic consistency, NOT donor authenticity or
timeline completeness. This round independently reconstructs histories from
synthetic timelines and compares all24state bins to the original donor's tables.
For all16histories×7models×2labels in two source fixtures, the candidate exact
probabilities match integer ratios and are label invariant (448subchecks/mode).
This remains synthetic evidence, not an authentication of real training rows.

Full source-interface control: generate12artificial sessions(six/six),188people,
100rounds/person with reciprocal opponent actions. The ORIGINAL R073 validator
and ORIGINAL R076 donor builder accept this shape and produce18424source events.
An independent history constructor does not call R073's event/record helper.
Both an identity-boundary source and a varied source are checked. Target controls
use15artificial sessions,7/8treatments,1040events, plus five unequal sessions.
Count-shaped targets are NOT raw R077 records or source-qualified cohorts. Four
complete B28 exact trees (112leaves each, including all model risks/pair votes)
match the integer route per mode. Independent event/session reversal also passes.
R077's single pooled12-session transfer is kept distinct from R073's5-other-
session-per-treatment LOSO; no experiment split was changed or new fit selected.

## New boundary: single-event probability identities break before summation

If a state's empirical proportion equalsC/N, smoothing must leave that proportion
unchanged. Withn=N,c=C, `(C+20*C/N)/(N+20)=C/N` identically. This is exact for
every outcome; no statistical assumption or row ordering is involved.

| Entirely artificial source | Exact M0=M1 Brier for y=0 | Original M1−M0 one-event delta | Old votes across2sessions | B28 votes |
| --- | --- | --- | --- | --- |
| C1/N9 | 1/81 | +1.734723475976807e-18 | 0better/0equal/2worse | 0/2/0 |
| C5/N18424 via original donor | 25/339443776 | −2.6469779601696886e-23 | 2better/0equal/0worse | 0/2/0 |

The second uses the FULL artificial12-session/188-person/100-round source:
all actions before final round are zero; only2fixed+3shuffled final actions are
one. All t3..t100past histories are zero. The original pooled fit hasN18424,C5
and each conditional table's only occupied state hasc5,n18424. This is a valid
shape-complete synthetic timeline, not18424fabricated independent observations
or an assertion that the real cohort had this composition.

Both targets contain ONE event per artificial session. `math.fsum` on these
single losses retains the false direction: a summation-only repair cannot fix
probability-rounding identities. These are new boundaries beyond PR18's35
permutations and B28's enormous-count tiny-nonzero example. B28 already handles
both correctly, so its code is not changed and no second repair is invented.
Primary evidence includes old float hex/exact binary ratios, old/corrected votes
and pure integer witnesses. These examples affect the PREDECLARED M1−M0 contrast;
they cannot establish that any real historical session had a changed vote.

## Actual new tests and falsifiability

Initial integer stub RED:1method/5subcases,5assertion failures, no errors;
hand probability1/9 anchor thenGREEN. New7methods pass in Python3.12.14 ordinary
and-O:14positive method executions. Each mode emits four whole exact trees and
two single-event old/candidate discrepancies. Discarded candidate copies with
alpha21 or cyclically shifted prediction histories each fail the whole-score
integer comparison by assertions, not import errors. Original/candidate source
files are never edited by controls. See each mode's actual patches and hashes.

```bash
python3 -B research/codex_b/2026-11-11-r077-scientific-readiness/run_audit.py --output research/codex_b/2026-11-11-r077-scientific-readiness/evidence/normal
python3 -O -B research/codex_b/2026-11-11-r077-scientific-readiness/run_audit.py --output research/codex_b/2026-11-11-r077-scientific-readiness/evidence/optimized
```

Bothexit0. New output directory required; use fresh temporary paths to reproduce.
commands.json records actual argv/cwd/exit/stdout/stderr byte hashes; nonempty
raw streams retained.22selected original/own fingerprints match before/after.
No other runtime/platform, full-repository suite, repeated old baseline, CI or
new human validation claimed. This is same-runner algorithm independence,
not independent data or outside-team replication.

## Real data readiness, interpretation and limits

Current R073 upstream tree metadata matches frozen source blob sizes; target
Zenodo v1 landing page lists expectedMD5 and public Open label, but no specific
license text is visible. Its API is unavailable through this runtime's tunnel
(403) and web tool; current raw access/use scope is NOT established. No new raw
human data downloaded, so current complete qualified risk-set recovery is NOT_RUN.
Do not turn this into a claim that the data is absent/unlawful or that earlier
successful R077 source qualification did not happen.

Two historical run metadata and9835byte result digest match the old record.
The archived macro scores/votes lack private per-session exact margins/source
tables and cannot determine the new vote transitions. Historical14/0/1and8/0/7
are unchanged and their exact-score impact is UNKNOWN. Full original partner
feedback information available to people and reenrolment between sessions remain
outside this computational audit. No causal-memory or open-loop validity added.

QUALIFIED_DOUBLE_RUN_PLAN.md sets preconditions and preserves the original
source/risk set, 7models/6pairs, alpha/noise, weights and all historical failures.
After explicit separate authorization, old/candidate/integer computations would
share one qualified private snapshot, report anonymous aggregate means/exact
deltas/votes/sign-transition counts, and prohibit any per-person/per-session
records, fit tables or low-entropy ID hashes in public output. No human runner
or new original-program hook is implemented. A retains integration ownership.

Closed computational subtasks: independent integer check at original donor
interface/dimensions; two previously uncovered scalar vote boundaries; explicit
source/authorization/output contract for a future comparison. Formal154queue
scientific net closures0, new E2/E3/human scores/external-team evidence0.
R073/PESEN freezes unchanged; overall historical impact/readinessPARTIAL/UNKNOWN.
