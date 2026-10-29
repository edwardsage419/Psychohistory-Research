# B: R271 S67 nonblind independent formula and source audit

Date: 2026-10-30 UTC. Scope: E1 exploratory finite artificial source and 27 world risk records.

Independent method: for each subset S of candidate four-bit windows, the probability that all selected windows contain only successes is 2^(-|union of bit positions|). Inclusion-exclusion over subsets yields the exact probability of any raw p<=1/8. FROZEN_FIRST is 1/16. BONFERRONI_ANY at m=3 is zero because min raw p=1/16 exceeds 1/24. This route uses no R generator or its enumeration.

Actual execution:
* Independent native Python CLI --check processed 13,584 persisted CSV rows, compared all 27 exact world risks, checked SHA256, unique primitive configurations, source mass, window coordinates, counts, p values, selected index, report flags and full source coverage. Exit 0, PASS.
* Independent native Python --test ran 7 unittest cases; 6 mutation cases were correctly rejected: duplicate world, missing world, altered fraction, E2 promotion, bool-as-int and deleted CSV row.
* Archived independent JS B program was evaluated in a V8 runtime using the full independently regenerated source CSV and JSON. All 27 exact risks and 13,584 rows PASS, six mutations rejected.
* R's independent Python program --test passed 8 tests; R --emit produced CSV and JSON whose Git blob IDs match the separate JS generator's GitHub-created blobs exactly.

Persisted source SHA256 9a72624ebcfc77e3eb65cdfe44696efc0d85a282f695a5ad77029753f75db9cb; persisted result SHA256 0f6268f76b705fb69b9aa806ba9551f7eb109dfda8a93eddeceaa4476fc89379.

The independent JS source and R JS generator are archived as standalone scripts. Their native Node CLI execution remains NOT_RUN. Python native checks were actually executed locally; full local Python scripts are available as run artifacts but are not yet GitHub archived. This is an internal nonblind algorithmic check, not external independent replication. No real data, independent holdout, empirical calibration, E2 or E3. Strict blind prescore status is NO because overlap outcomes were partly anticipated during design. R073 and PESEN v0.1 remain frozen.

Open: Node native CLI, external review, observational applicability, original R271 acceptance unchanged. No Actions or paid services invoked.
