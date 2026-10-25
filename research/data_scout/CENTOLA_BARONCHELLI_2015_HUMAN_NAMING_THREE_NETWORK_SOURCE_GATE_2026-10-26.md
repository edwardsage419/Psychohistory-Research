# A public human naming-game data source gate: Centola and Baronchelli 2015

Date: 2026-10-26 Asia/Singapore. Status: `THREE_PUBLIC_TEXT_FILES_READABLE / PERSON_ROUND_IDENTITY_MISSING / LICENSE_UNVERIFIED / R170_E2_BLOCKED`. This is a newly identified human social-convention experiment source, not a new R073 repeated-prisoner's-dilemma dataset.

## Official provenance and what was actually read

Authors: Damon Centola and Andrea Baronchelli (2015), *The spontaneous emergence of conventions: an experimental study of cultural evolution*, PNAS, DOI https://doi.org/10.1073/pnas.1418838112. The original Network Dynamics Group at University of Pennsylvania publishes an English project page and three links under “Experimental Data for Each Condition, N=48”: https://ndg.asc.upenn.edu/experiments/emergence-of-social-norms/ . Institutional author manuscript: https://openaccess.city.ac.uk/id/eprint/6625/ .

Direct official plain-text files opened and inspected through the public web source:
1. Spatial network: https://ndg.asc.upenn.edu/wp-content/uploads/2016/04/Centola_Baronchelli_2015_spatial_net_n48.dat_.txt (web text view 746 numbered lines, 0 through 745).
2. Random small-world network: https://ndg.asc.upenn.edu/wp-content/uploads/2016/04/Centola_Baronchelli_2015_random_net_n48.dat_.txt (559 numbered lines, 0 through 558).
3. Homogeneous mixing: https://ndg.asc.upenn.edu/wp-content/uploads/2016/04/Centola_Baronchelli_2015_hom_mixing_n48.dat_.txt (770 numbered lines, 0 through 769).

The source page labels each condition N=48. The text-view line counts are observations of the rendering; they are not independently downloaded raw-byte row counts. Each inspected line appears to contain two human-supplied naming responses followed by a value such as 0.0 or 1.0. Some lines contain `nan` and `RESPONSE_NOT_GIVEN`. Responses vary in capitalization and occasionally contain spaces; a naive whitespace split cannot safely recover two columns in all cases. The exact codebook for the third field, handling of `nan`, raw-byte SHA256 and original delimiter grammar remain unverified. No raw files were redistributed.

## Field, time, identity, license and replication gates

* Observable behavioral outcome: paired names and an apparent agreement indicator are available in publicly readable text. Human naming behavior is more directly relevant to R170 than unrelated color-word or simulated prisoner-dilemma data.
* Time: line order is visible, but an explicit event timestamp, round ID or session/participant ID is absent from the inspected three-column lines. Line order must not be assumed to be complete chronology without the author codebook.
* Independent units: the page describes three network conditions with N=48. A row is an interaction, not an independent participant or independent experiment. Unique people, pairings and number of independent sessions cannot be reconstructed from the visible fields.
* License: official download links are public, but no explicit dataset reuse license was identified on the project page. Redistribution and derivative use require license clarification; this audit records links only.
* Source identity: this experiment is Centola and Baronchelli 2015. It is distinct in authors and design from the R170 artificial four-agent two-token model and distinct from the previously catalogued Montero/R073 repeated-game source. This audit does not claim a fifth R073-compatible experiment.
* Reproducibility: raw-byte hashes, a trustworthy parser for free-text names, event order, identities, topology adjacency and held-out independent sessions are outstanding.

## Eligibility decision

`R170_DIRECT_E2_PREDICTION = BLOCKED`: original R170 has four fixed nodes, exactly two tokens, explicit latent inventories and known channel-flip probabilities. The human experiment has 48-person conditions, open-ended names, uncertain participant/round IDs, and no observed latent inventories. Using R170 frozen probabilities as if they were participant-level forecasts would require an unapproved observation mapping and parameter refit. No such scoring was performed. R073 frozen repeated-prisoner's-dilemma scoring is inapplicable. E2 scored=0, E3 historical=0.

Next A step: obtain source codebook or original field dictionary, verify legal reuse, download and hash raw bytes in an approved free environment, recover independent experiment/session identities and then freeze a separate eligible predictive evaluation before examining outcome scores. No paid access, private data, accounts or extra computing services were used.
