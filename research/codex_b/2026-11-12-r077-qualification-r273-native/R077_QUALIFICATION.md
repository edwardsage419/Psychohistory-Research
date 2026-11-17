# R077 source qualification — bounded BLOCKED handoff

track:Codex B; subflow:R077 actual source qualification and dual-run readiness
run_date:2026-11-12 task round; actual command UTC times in execution evidence
observed_head:d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c
status:BLOCKED_CURRENT_RAW_REQUALIFICATION_AND_HUMAN_SCORE_AUTHORIZATION
evidence_scope:static original-paper/code/metadata inspection and Git identity;
no new raw human download, row reconstruction, fitting or scoring.
output_paths:this file,DOUBLE_RUN_CHECKLIST.md,evidence/r077-version-chain.json.
commit_sha:final delivery/HANDOFF; CI:NOT_RUN; added_cost:0.

## What is confirmed, and where each digest comes from

Official landing page https://zenodo.org/records/15462528 remains readable through
the web tool. It lists v1, published2025-05-19, and these author file descriptors:

| File | Official listed MD5 | Scope this round |
| --- | --- | --- |
| cleandata.dta | 4cce04ea68b7a0492c242b206efebe53 | Listed1.5MB; download timed out, HEAD blocked |
| number1.do | 0ee6ace76d2ea9a8daf7ab1f7ef026e6 | Listed23.7kB; text fetch unavailable |
| number2.do | 563263f55bb3a7a1910b3b38e85fe22c | Listed13.0kB; static text readable, not executed |
| power.do | 3464cb2e28d3e05d6296d09f88b159cf | Listed855bytes; text fetch unavailable |

Spaces in the official filenames are retained at source; compact table labels
above identify those same three scripts. Listed MD5s are NOT newly recomputed
file digests. Exact cleandata size1514315bytes andSHA256
1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985 are frozen
historical identities, not a successful new binary read. Current API/export
retrieval failed; no renewed claim of complete source-byte qualification.

The R073 original Git tree at4743f74d8a03a031b8f70aff64956f8ad5155182 is readable
through the existing GitHub connector. fix.csv blob3bf78bf85f6642afee18d6f1965dca7272582f40,
988279bytes andrand.csv blobf5a86cd033b739da45d3fc7c5019068f612146a2,1112614bytes
still match the frozen protocol. This is current metadata, not new CSV row access.
Do not substitute Dryad's final release without original-byte equivalence proof.

Current main programs match historical identities: R073c8a0b47f, R07770889bd1,
B28candidateb050fcf1; archived9835byte result13946754 and SHA256
8d8b8413e3e55cb5d856f34b873ee20c2ba470e04190bb8577f931d25ba509a4 unchanged.
Full blobs/lengths/digests in evidence/r077-version-chain.json. B31 integer audit
157872ea6315ef92d4ea7938e01ff4761afb3a55 is available at fixed Git commit03cf49d8,
but PR31 is still OPEN/draft and its code is not on main. This is a reviewable
version chain, not scientific adoption or a reason to bypass A's veto.

## Official paper, code dependencies and license boundary

Original paper: Drouvelis & Pearce2025,European Economic Review178:105075,
DOI https://doi.org/10.1016/j.euroecorev.2025.105075 . The publisher's version
is freely readable via the author's institution:
https://pure-oai.bham.ac.uk/ws/portalfiles/portal/268946923/DrouvelisM2025Intelligence.pdf
Read title/license, design/procedure and data-availability footnote. The ARTICLE
states CC BY4.0. The institution confirms its version-of-record status. This
article license is not automatically a verified license for separate Zenodo DTA
or Stata files. Zenodo's rendered Rights/License field gives no specific terms;
the Open label alone does not establish all reuse/redistribution permissions.
No conclusion that private reading is necessarily unlawful is made.

The paper's full comparison also uses the earlier Proto etal dataset. Zenodo
explicitly requires obtaining that original study separately for full replication.
Readable number2.do imports cleandata and depends on matrices created elsewhere
in the author's multi-script workflow. It is not a stand-alone reproduction of
every published table. Prior author-code audit identifies experimentaldata.dta
as a separate older-study dependency; its terms are not newly established here.
R077's seven-model transfer does NOT require importing that older target study,
running the author's regressions or buying Stata. Its existing Python path
reconstructs its own histories; .do files were inspected, not executed/copied.

There is a concrete qualification question for the scientific owner: the paper
reports26sessions/260subjects, whereas the frozen R077 path pools15values of
Session and distinguishes a26-valued sessionid field. Existing project audits
acknowledge those two field cardinalities; they do not by themselves reconcile
the paper's independent-session meaning. We do NOT replace15 by26, alter1040
targets, infer that the old result is wrong, or change CLOSED_BOUNDED. If a new
source read reveals a grouping-interpretation change is necessary, ChatGPT/owner
must dispose of it scientifically under a separate protocol decision.

## Bounded access checks and alternatives — STOP point reached

One bounded campaign used the official landing/API, JSON export and DataCite
registration metadata, institutional paper and author-code links. API/export/
DataCite web reads failed; a direct runtime DataCite GET and DTA HEAD both returned
URLError/tunnel403. One web DTA download attempt timed out. The institutional PDF
and number2.do text succeeded. No repeated retries, alternative data cohorts,
paid platform, author contact, successful raw-byte recovery or model scoring followed.

Verified free alternative: the institutional publisher PDF supports paper method
and ARTICLE-license checks. It is not a verified replacement DTA or data license.
No free compliant alternate copy of the exact DTA was verified. Failed endpoints
do not establish global unavailability. Current raw-use terms remain UNKNOWN;
full15/1040raw recovery remains NOT_RUN. Future matching bytes could enable
deterministic reconstruction, but the anonymous score archive cannot do so alone.

Specific missing conditions:
1.Current exact data bytes and current permitted-use scope for DTA/source CSVs;
  do not assume a paper license governs all external files.
2.Qualified original participant/session/game/time/pair mapping on those bytes,
  including the independent-unit question above; retain all historical gates.
3.Explicit separate owner/ChatGPT authorization for old/exact/integer real-data
  comparison, environment/cost disposition and approved anonymous publication.

R077 historical vote impact remains UNKNOWN. This audit closes the bounded
source/permission investigation for this round, not these external/scientific
blockers. Do not repeatedly probe the same endpoints. Continue another real P0
computing task. No new human/E2/E3 evidence or revised frozen result is produced.
