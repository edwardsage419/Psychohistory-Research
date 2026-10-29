# A: Mao et al. 2017 long-run human Prisoner's Dilemma source gate

Date: 2026-10-30 UTC. Status: SOURCE_PAPER_AND_CODE_CONFIRMED; RAW_DATA_BLOCKED.

Primary paper: Mao, Dworkin, Suri, Watts (2017), *Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner's Dilemma*, Nature Communications 8:13800, DOI https://doi.org/10.1038/ncomms13800, full text https://pmc.ncbi.nlm.nih.gov/articles/PMC5241863/.

The paper states 94 completing participants, 20 consecutive weekdays, up to 400 **separate ten-round supergames** per person, approximately 375 supergames per completer and 374,251 individual decisions in aggregate. Two human players interact in each ten-round supergame; pairings vary across games. The experimental time unit must retain participant ID, day, game number, within-game round (1..10), partner/matching and action history; treating 400 games as one uninterrupted 4,000-round dyad would be invalid.

The paper explicitly directs readers to its public data archive https://osf.io/64z8u/ and original experiment code https://github.com/TurkServer/long-run-cooperation. OSF landing-page access returned HTTP 403 in this run; the OSF API file-list route also could not be retrieved. Therefore no raw data file, schema, unique participant key, missingness, partner ID, checksum, or dataset-specific reuse license was independently verified. The article itself is CC BY 4.0, which must not be imputed to the unseen OSF data. No personal nonpublic data were accessed.

GitHub source-code repository verified public at commit 4d8ed83e7745e1ffe82ce9403064e3558fabfa6f; its README Git blob cf0ff6024113f02dbb05858735e4b4a1b3a8eeb2 documents the experiment and random rematching interface. The GitHub tree did not expose the original participant-level data file or a standalone LICENSE file. Software reuse rights remain unverified.

R073 frozen direct eligibility: NO. The 10-round within-pair horizon does not satisfy the frozen two-person 100-round same-game design, even though individual participants completed many distinct games. General longitudinal E2 learning analyses: potentially valuable after authorized raw records, stable IDs, pairing history, license and predeclared split rules are recovered.

Next: retry public OSF file listing without registration or paid access; if still blocked, retain BLOCKED and prioritize a separate publicly downloadable human dataset. No raw participant data redistributed, new E2 predictions=0.
