# Plan: research/codex_b/2026-11-10-r077-exact-paired-ties/PLAN.md

Refreshed main e5f2baa7 and17 open PRs. New A#17 composes R170 byte identity and
is disjoint. Prior B#13 covers donor multiplicity, B#16 scoring mutation coverage;
this work addresses the exact-tie limitation explicitly disclosed in B#16.
Raw round/session duplicate paths already have downstream protection, so no
speculative source validation change selected. No source files or protocols edited.

Root cause: R077 increments float Brier sums by record order, subtracts session
means and compares signs without an exact certificate. Same synthetic multiset
can be categorized equal or better; all35 rational risks are exactly1/4.
Integer witness: p1=7/14,p3=5/14;3 positive/4 negative, each squared numerator343,
denominator1372. Source counts independently coherent (32 artificial rows).
Ruling: user autonomy/continue authorizes bounded implementation without renewed
design questions; implement inline in new branch and Codex B directory, then one
fresh engineering reviewer. Do not alter frozen original outputs or adopt new
statistical thresholds. Runtime comparisons use already installed Python versions.
