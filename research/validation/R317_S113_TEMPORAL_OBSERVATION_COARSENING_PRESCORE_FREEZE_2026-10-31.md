# R317 S113: finite temporal observation coarsening, prescore freeze v1

UTC date: 2026-10-31. Track r. Baseline main: ce5d443b90e2d0fc3e78865e131e02fac7938e4f. Original frozen R317 protocol: protocols/R317_TEMPORAL_NETWORKS_THREE_CONTACT_81_SOURCE_STRICT_TIME_FREEZE_2026-10-24.md (Git blob b1e014a0645ba535d4619920432fd579f4db9bf2). Original 81 contact rows Git blob 926c1fee6a473da6bbedb9746cf109f5a3a3eb16. Original 81 origin outcomes Git blob af19d64d8132f351861fecb074bcd3aae1e261c9. No changes to original R317 acceptance.

## Frozen finite universe and target

Use all 27 lexicographic schedules of three instantaneous undirected contacts on nodes {0,1,2}, contact identities 0=(0,1), 1=(0,2), 2=(1,2), with times 1,2,3 and repeats permitted. For every schedule and each ordered distinct origin-target pair (six pairs), target Y=1 iff a message initially at origin t=0 reaches target via strictly increasing contact times, one hop per event. Exactly 162 labeled instances. Source events and outcome labels must be independently rebuilt and checked against the pinned original source rows/outcomes; a mismatch is FAIL. No future event leakage within a contact; a newly informed node can forward only at later contact.

## Prespecified observation maps and scoring

Every observation key includes the ordered origin and target identities. Compare six event-information channels: FULL ordered contact triple; MULTISET sorted triple with multiplicity; STATIC unique set of edges, no times or multiplicity; FIRST first contact edge only; LAST last contact edge only; DISTINCT_COUNT number of unique edges only. Also evaluate PAIR_ONLY origin-target identities with no contact information as baseline.

Assign equal weight 1/27 to each artificial schedule; do not claim this is a real sampling distribution. For each map and each key, calculate n1 reachable and n0 unreachable. Bayes oracle majority-class accuracy = sum(max(n1,n0))/162 with ties resolved predict 0. Exact oracle Brier = sum(n1*n0/(n1+n0))/162 (Fraction). Count mixed-label groups, distinct observation keys, and compare information losses relative to FULL. The oracle is computed using the complete artificial universe and is descriptive in-sample mathematical discrimination, not an empirical out-of-sample prediction or measured human calibration. No fitting, parameter tuning, or selecting observation maps after results.

## Mandatory independent B checks

An independent Python implementation must recompute each outcome by enumerating time-increasing subsequences of event indices, independently construct all observation groups and Fraction scores, verify 162 labels, original 81 schedule-origin outcomes, source uniqueness, every group partition, and invariant FULL accuracy=1 and FULL Brier=0. Eight prespecified corruption classes: duplicate schedule, missing schedule, modified contact, altered reachability label, altered group count, altered accuracy, altered Brier, and improper E2 evidence promotion. Reject via explicit exceptions in Python normal and optimized execution. Keep any failing exploratory runs visible. A second implementation may be JavaScript or Python but must not import the primary scorer. Report internal nonblind scope; no external independent replication.

## Evidence and governance

Evidence grade E1 finite artificial only. E2 human and E3 historical zero. R073 and PESEN v0.1 frozen. Do not change original239 crosswalk v7.8, 154 pending queue, any original R317 file, other track files or prior acceptance. A track separately searches public empirical temporal contacts or long human-human repeated games, checks license, time units and source access, and records blockers. No paid service or GitHub Actions dispatch; CI status NOT_RUN unless independently observed. New files only in research/validation/, research/data_scout/, research/evidence_audit/, research/coordination/r/. Codex PRs unmerged are review evidence only.
