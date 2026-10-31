# A: SocioPatterns Lyon hospital temporal contacts, source and timestamp gate

Date: 2026-10-31 UTC. Track A within R hourly research. Target key: (A,SocioPatterns-Hospital-Lyon-2010,official-2013-09-14,raw-timestamp-and-tie-semantics). Baseline main before S113 freeze: ce5d443b90e2d0fc3e78865e131e02fac7938e4f.

## Primary public source actually inspected

Official English dataset page: https://sociopatterns.org/datasets/hospital-ward-dynamic-contact-network/ (publication date 2013-09-14). Official linked compressed contact list: https://sociopatterns.org/assets/data/hospital_lyon_contacts.dat.gz. Associated original journal paper: *Estimating Potential Infection Transmission Routes in Hospital Wards Using Wearable Proximity Sensors*, PLOS ONE 8(9), e73970 (2013).

Official dataset description identifies 46 healthcare workers and 29 patients in a Lyon hospital ward, observations 2010-12-06 13:00 through 2010-12-10 14:00. This is a study-design count of 75, **not** a verified count of distinct IDs in raw contact rows. The declared raw row layout is `t i j Si Sj`, tab separated. `t` is seconds, each row indicates an active undirected proximity contact in interval [t-20s,t]. `i,j` are anonymous person IDs; `Si,Sj` are roles from NUR, PAT, MED, ADM. Multiple contact rows may share a timestamp.

License: official page explicitly states Creative Commons Attribution-NonCommercial-ShareAlike; research reuse must respect noncommercial, attribution and share-alike restrictions. No account purchase or private data required to inspect the public description. Raw compressed file is offered on the official page, but a browser retrieval attempt returned unsupported gzip content type, and a separate container download attempt for a related official 2013 SocioPatterns gzip also failed. No successful raw hospital archive acquisition this round. File SHA256, true row count, unique IDs, exact timestamp range, event duplications and parsing integrity therefore UNKNOWN. No data redistributed.

## R317 mechanism transfer gate

R317 S113 frozen artificial corpus has exactly one strictly ordered event per timestamp and three agents. The hospital dataset permits multiple contact edges at the same timestamp. Arbitrarily sorting tied rows into a strict sequence can invent within-interval two-hop transmission. For example, at a single t with contacts (0,1) and (1,2), a message initially at node0 may reach node1 by the end of the interval, while node2 cannot be declared reached at the same timestamp without an explicit within-interval ordering or simultaneous-transmission model. This is a synthetic semantic counterexample, not a measured hospital event.

Required next steps before E2: retrieve the official archive without payment, hash and safely decompress, verify five fields and units on every row, verify all distinct anonymous IDs and timestamp ties, freeze a simultaneous-event contact protocol, choose a leakage-safe time-blocked or independent-person evaluation split, and compare with a static aggregation baseline. Hospital proximity is a contact opportunity, not observed message adoption or infection; no observed R317 diffusion outcome is supplied by this metadata. R073 continuous 100-round human-human prisoner dilemma eligibility: HARD_NO_BY_TASK_TYPE.

Result: SOURCE_METADATA_VERIFIED; OFFICIAL_LICENSE_VERIFIED; RAW_DATA_NOT_OBTAINED; TIMESTAMP_TIE_GATE_OPEN; E2=0; E3=0. No new spending or Actions runs. Source language: English only.
