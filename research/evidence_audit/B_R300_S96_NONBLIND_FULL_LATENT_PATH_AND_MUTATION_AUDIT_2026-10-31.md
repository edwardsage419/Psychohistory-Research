# B R300 S96 independent audit report

UTC date: 2026-10-30. Status: INTERNAL_NONBLIND_E1_MATH_PASS; FULL_SCIENTIFIC_ACCEPTANCE_PARTIAL. Plan frozen at commit cd0eb73dd9b52b9a98a0a40d9f9628257bc44752 before scored S96 results. R plan frozen at e7d5d6e7f9a82210fb5151c77a492303e1b20110.

## Actually executed
The archived independent JavaScript oracle `b_r300_s96_hidden_path_oracle_20261031.js` was executed in V8 against the real remote main CSV and JSON. This oracle does not import the R S96 generator and sums all 2^4 hidden paths for each four-observation prefix and 2^5 paths for the next observed bit, using its own exact BigInt rational implementation. It checks source key identity and all 7 exact numerical fields in every one of 288 rows, giving 2016 exact field comparisons, plus 18 independent group risk reconstructions and true prefix mass normalization. Result: PASS.

The archived R S96 generator was independently fetched from GitHub and re-executed in V8. Its generated CSV and JSON were both **byte-for-byte equal** to the persisted remote file content. Remote Git blobs: R script 538d760a865809f87b4db221d71ae2d82238001f, CSV da656be15a1ece59b2c4ad3c49495fe7146954e2, results JSON 9650a84a27042d1a9ab3800123db3214bbc96288, B script d85760743da1327f40b47c0dfc0c1336cf0ed939.

Original R300 historical parity: fetched original R300 result JSON Git blob 4d9405707ce4994554c0fff0d277d50196bf68dd; all 32 length-four prefix evidence and next-observation forecasts for the two unchanged true parameter pairs exactly matched the new S96 oracle candidate entries. No historical original file was edited.

Separate local Python 3 Fraction code, using hidden path enumeration rather than the R recursion, independently computed all 18 group expected risks and oracle values. Key examples: IID true world risk with candidate (stay3/4, emission3/4) = 1469576384287005/5782662820588808; persistent true world oracle risk = 105579273/430168816; persistent true world wrong (stay1/4, emission1) risk = 11/32. This is a third nonblind calculation route in the same assistant execution context.

## Frozen negative controls
Eight preselected mutations were actually injected and rejected: duplicate source, missing source, changed true prefix mass, changed true next probability, changed candidate next probability, changed conditional risk, changed aggregate expected risk, and false E2 promotion. All eight rejected. The duplicate/missing controls were rejected by cardinality before detailed source comparisons, while other mutations were rejected by exact field, group, or evidence-scope gates. This is detection coverage for those cases only.

## Scientific interpretation and limitations
The Brier risk is a population expectation under a fully known artificial generator. It is an independent *future observation variable* conditional on four artificial observations, not a fresh human experiment, fitted unknown-parameter HMM, or real held-out cohort. The same 16 observation prefixes are reused across nine candidate filters and must not be counted as 144 independent trajectories. Probability calibration on empirical data, confidence intervals for sampled populations, human E2 transfer, historical E3, and true external investigator replication are NOT_RUN. This was nonblind because the original R300 protocol and new R S96 outputs were visible to the auditor.

Evidence: E1 synthetic mathematical PASS in bounded scope, S96 scientific acceptance PARTIAL; original R300 CLOSED_BOUNDED_E1 acceptance unchanged. R073/PESEN v0.1 FROZEN. GitHub Actions NOT_RUN due to unverified free quota. No paid services or private data.
