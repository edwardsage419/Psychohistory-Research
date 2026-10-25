# R164 third method: exact observational partition and mechanism nonidentifiability

Date: 2026-10-25, Asia/Singapore. New prospective protocol: protocols/R164_OBSERVATIONAL_IDENTIFIABILITY_72_WORLD_EXTENSION_FREEZE_2026-10-25.md, commit 95bf2e51fef98ba96c9f3b88176e5b4a4fa550ac. Existing original R164 remains CLOSED_BOUNDED_E1, untouched.

## Source and method

Frozen input research/R164/R164_EXACT_RESULTS.json, SHA256 ce27a70aee6ee82ca360efc93b12632c44f6bbd7a73b32bf1aaafc602df69f52, Git blob 087686b629cba4d0b94492d360893a47e334ecb2. Exact 72 artificial worlds, 360 original frequency states, four initial p0, three r, three h, two e. No actual human observations.

Recurrence: p_next = (1-e)[p + h(r-1)p(1-p)/(1+(r-1)p)] + e/2.

Predefined regimes: for each known initial p0, observe first 1, 2 or 4 transitions (2, 3 or 5 total states); group all candidate (r,h,e) worlds by exact rational equality. Also group separately with externally known e. Each group is a finite-grid observational equivalence class.

## Results, exact class counts

| Observation | e information | Classes | Singleton worlds | Ambiguous worlds | Largest class |
| --- | --- | ---: | ---: | ---: | ---: |
| p0,p1 | unknown | 39 | 30 | 42 | 5 |
| p0,p1 | known | 40 | 32 | 40 | 5 |
| p0,p1,p2 | unknown | 40 | 32 | 40 | 5 |
| p0,p1,p2 | known | 40 | 32 | 40 | 5 |
| p0..p4 | unknown | 40 | 32 | 40 | 5 |
| p0..p4 | known | 40 | 32 | 40 | 5 |

For p0=1/5, one transition gives 9 classes, 6 singleton worlds; two transitions give 10 classes, 8 singleton worlds. For each other initial p0, one transition already gives 10 classes and 8 singleton worlds. At every p0 there are two persistent five-world classes, one per replacement e. Each five-world class comprises r=1 with any h (three worlds) and h=0 with r=2 or 4 (two worlds). All these combinations have the same exact path because the content coefficient is inactive.

One nontrivial one-transition collision exists: p0=1/5, r=4, h=1, e=0 and e=1/4 both give p1=1/2. The next values differ: p2=4/5 versus 29/40. Two transitions resolve this specific collision.

**Interpretation:** within this fixed 72-world synthetic grid, 40 worlds remain observationally ambiguous even with all five frozen timepoints. A longer trajectory cannot distinguish the structurally inactive salience or copying parameters in the five-world classes. No general continuous-parameter identifiability theorem follows from this finite-grid count.

## Audit and limitations

Source-replay partition counts were calculated from original frozen JSON, then an independent JavaScript BigInt rational urn oracle executed 360 exact state comparisons, 18 class membership signature checks and two actual mutation computations. The independent oracle detected 32 applicable salience-omission mutants and 35 applicable replacement-omission mutants. See B audit in research/evidence_audit/B_R164_OBSERVATIONAL_PARTITION_INDEPENDENT_BIGINT_SCIENTIFIC_AUDIT_2026-10-25.md.

New standalone Python scripts are archived as reproducibility implementations. The execution evidence for this run comes from direct exact Python calculations and a separate executed JavaScript BigInt oracle. These newly committed Python files were not run in remote CI in this round, and their own source-level replay remains pending. Do not interpret this as external independent replication.

Result status: PASS_BOUNDED_INTERNAL_E1_WITH_REMOTE_PYTHON_REPLAY_PENDING. New E2=0; E3=0; external independent replication=0. Original acceptance and 154-item catalogue evidence triage queue unchanged. R073 and PESEN v0.1 frozen.

Files: research/validation/r164_observational_partitions.py, research/validation/R164_OBSERVATIONAL_PARTITIONS_EXACT_RECEIPT_2026-10-25.json, research/evidence_audit/r164_b_independent_observational_oracle.py.
