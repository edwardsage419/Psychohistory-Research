# A track: Nay and Vorobeychik human iterated PD curated data source gate

Date: 2026-11-01 Asia/Singapore. Target key: (A,NayVorobeychik2016,JohnNay/datafsm_master_c2e55eab,curated_PD_R073_session_identity_gate).
Status: PUBLIC_CURATED_SOURCE_AND_51_FIELD_SCHEMA_VERIFIED; ORIGINAL_BINARY_NOT_PARSED; R073_ELIGIBILITY_NOT_ESTABLISHED.

## Actual source reads
Published paper: John J. Nay and Yevgeniy Vorobeychik (2016), Predicting Human Cooperation, PLOS ONE 11(5):e0155656, DOI 10.1371/journal.pone.0155656, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0155656 .
Curated R package source: https://github.com/JohnNay/datafsm . GitHub repository default branch master, MIT package license; README and package metadata accessible. Data documentation was actually read: man/NV_games.Rd blob be625b217505dd05781f5bd9c12925df673a7ac0, R/data.R blob 2a1dc849c34036026f45d1238d586376b876ec5f. Public binary data/NV_games.rda exists, size 761556 bytes, Git blob 36a961908385a7fe33ba688479b5dfc7b0a6b609. Binary bytes and original underlying experiments were not decoded or verified.

The documented object has 168386 rows and 51 variables spanning 30 game-structure variants from eight experiment families: AM, BR, DB, DF, DO, FO, FR, KS. Fields include period, my.decision, other.decision1..9, my.decision1..9, own/opponent payoff lags, payoff matrix parameters r/t/s/p, risk, delta, error, infin, contin, group and data. Each record is described as a decision/round. No reliable per-person identity, dyad key, session identifier, or contiguous 100-round session identifier is documented in the 51-column schema. The paper's total is decisions across heterogeneous experiments, not one continuous match.

## Rights and access
The public package is MIT licensed, with LICENSE.md blob c3cb9e0116916537880c87633bb506051d53d4ae. Original experimental data reuse rights may differ from package software terms; verify original author data license before redistributing binary. No paid account, private source, or paid API accessed. Full R .rda parsing, observed max period, missingness, group distribution, original source-to-curated identity, and true subject/dyad/session join remain OPEN.

## R073 and possible E2
R073 requires a truly independent human-human dyadic session of 100 consecutive rounds, with identity and full prior actions, frozen model and scoring. These conditions cannot be established from this curated documentation. Current gate: R073_ELIGIBILITY_NOT_ESTABLISHED; no data concatenation across groups, games, or source studies; no R073 rescore. The curated data may support a future separate prescored human behavior study with game-structure holdout if row-level identities and data rights can be established. Human E2 scoring this run = 0, historical E3 = 0.

Next: safely decode .rda with free open-source R/pyreadr in a controlled environment if available, audit actual columns and group/period maxima, trace source-specific participant/session keys, and independently check data rights. If no identity can be recovered, retain an explicit R073 negative gate. No empirical claims before this.
