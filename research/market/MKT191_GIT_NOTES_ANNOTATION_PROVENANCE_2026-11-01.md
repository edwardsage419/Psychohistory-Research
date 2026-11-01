# MKT191 Git notes annotation provenance and outcome adjudication
Date: 2026-11-01 UTC. Track: market. Key: (market,Git-notes,Git-2.47.3,mutable-outcome-annotation-and-clone-omission). Baseline main: caf6d580a54bbc5e0f2c6132f22a9d1833263878. Status: COMPLETE_BOUNDED.

## Original English sources and evidence
Git official manual https://git-scm.com/docs/git-notes describes notes as annotations to objects without touching those objects, default refs/notes/commits, overwrite via add -f, removal, and separate notes history. Git official https://git-scm.com/docs/git-fetch explains configured refspecs. This is an open-source candidate mechanism, not a tested life-planning vendor. Official documentation supports semantics; native local Git execution supports the bounded engineering counterexample. No external product efficacy validation.

## Input, state, algorithm, objective, feedback, privacy and cost
Input: synthetic forecast D1 with probability 0.8 and outcome UNVERIFIED; two successive notes claiming SELF_REPORTED_SUCCESS and INDEPENDENTLY_CONFIRMED_FAILURE. State: original Git commit SHA, note blob, refs/notes/commits tip, note history, ordinary clone refs. Algorithm: content-addressed objects with separately mutable notes ref; note overwrite and remove; ordinary clone using default fetch refspec. Objective: explore later outcome annotation without rewriting the original forecast commit. Git notes provide no independent truth adjudication, user calibration, causal attribution, or automatic feedback. Explainability is inspectable through git notes show and git log on the notes ref; ordinary history may omit notes and third-party witness is absent.

Local Git is free open source and was run on disposable synthetic files with no network or personal data. Git notes may contain sensitive annotations and be copied or retained in history. A local-only copy reduces automatic third-party exposure but does not prove secure deletion or privacy of later transfers. Git identities and timestamps are not independent identity/time attestation. No paid service, API, CI or GPU was used.

## Native experiment
Executed actual Git 2.47.3 with Python 3.13.5 subprocess and temporary local repository. Archived executable: research/market/mkt191_git_notes_audit_20261101.py. Eleven explicit assertions PASS.
1. Commit a forecast. Add note SELF_REPORTED_SUCCESS. Original commit hash and decision.json remain unchanged.
2. Force overwrite note to INDEPENDENTLY_CONFIRMED_FAILURE. Notes ref hash changes; original forecast commit stays identical.
3. Remove current note. The note is absent from normal lookup; previous notes commits remain accessible through the notes ref history before pruning.
4. Clone the repository with ordinary git clone. Forecast commit is present; default clone does not fetch refs/notes/commits. This is a tested default behavior in the temporary environment, not a claim about every custom fetch configuration.

The string INDEPENDENTLY_CONFIRMED_FAILURE is deliberately an unsupported artificial claim. The program demonstrates that writing this label is easy and provides no independent outcome confirmation. A notes commit may itself be rewritten or pruned in later operations; that was not tested in this round.

## Implications and limits
Candidate future requirements: separately identify forecast event, annotation author and authorization, independently verified outcome source, note ref presence, external checkpoint, amendment history, and erasure obligations. Never infer truth from note text or Git hash. This is a NONBLIND E1 engineering experiment, no E2 human data, no E3 independent historical population, no claim of decision-product readiness. No changes to R series, frozen protocols, PESEN, or utility weights.

Next: inspect open-source attestations with verifiable issuer authorization and a privacy-preserving outcome dispute process; retain separate verification of empirical predictive calibration.