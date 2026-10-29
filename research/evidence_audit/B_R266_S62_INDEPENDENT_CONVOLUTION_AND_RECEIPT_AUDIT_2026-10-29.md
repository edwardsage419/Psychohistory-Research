# B track: R266 S62 independent count convolution and persisted-receipt audit

UTC date: 2026-10-29. Target key: (B,R266,S62,score-coverage-independent-count-oracle).
Review scope: original R266 protocol and finite-world result, R266 S62 freeze `6cdc35c36bdf6d2f06761dff5b04a8af8aa1bd8b`, new R result and its archived JSON. The reviewer had read the original R266 and the new S62 R results. This is NONBLIND INTERNAL computational audit.

## Independent method and executed checks

The R route enumerates 5,328 complete source tuples from original GitHub-fetched CSV and computes coverage directly. The B route does not import R code or source tuples. It derives one-draw success-count distributions from each of four frozen functions, then convolves them n times for IID and n/2 times for paired antithetic designs. It independently derives the true estimator variance and expected IID plug-in variance from the resulting count PMF.

The archived B script `research/evidence_audit/r266_s62_independent_convolution_gate.js` was evaluated in V8 against the newly generated R receipt, using the exact archived R and B source text fetched from GitHub. B recomputation matched all 18 rows and 180 fields exactly, with no discrepancies. Five injected counterexamples were actually rejected: changed coverage, omitted row, duplicated row, E2 evidence promotion, and boolean false in an integer field.

The frozen SYMMETRIC_EXTREMES_N6 counterexample independently matches: IID score coverage 31/32, antithetic 3/4, IID naive/actual variance ratio 5/6, antithetic ratio 1/3. Both methods preserve the zero-variance case with null ratio.

The original source identity was separately checked offline: a Python standard-library reconstruction of the original nine-world 5,328-row CSV produced exactly 419,791 bytes and SHA256 `5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a`, identical to original R266 machine receipt. The regeneration source is archived at `research/evidence_audit/r266_s62_original_source_sha_rebuild.py`. This verifies deterministic source reproduction; it is not an additional externally collected dataset.

## Scientific validity and outstanding gates

The frozen target and score formula were committed before new calculations. Original R266 was previously known; no full blind review claim. Source data are synthetic enumerations; independence of actual participants, held-out human prediction, probabilistic calibration in human populations, bootstrap uncertainty and historical transfer are not applicable or NOT_RUN. For the finite enumerated probability space the coverage and estimator moments are exact, with no Monte Carlo sampling uncertainty.

Native Node execution of the two archived JS CLI programs against actual checked-out files remains NOT_RUN; the performed check used V8 direct function execution. The newly archived Python SHA regeneration script was authored from the locally executed reconstruction algorithm; the exact GitHub archived script has not been re-executed from a checkout. New GitHub Actions and external-team replication are NOT_RUN. These open gates do not negate the bounded mathematical counterexample but prevent claiming full archival CLI acceptance.

Original R266 closed bounded E1 status remains unchanged. New E2 human=0, E3 history=0; R073 and PESEN v0.1 frozen. No paid service or Actions triggered. Account bill and free-runner balance not independently verified.
