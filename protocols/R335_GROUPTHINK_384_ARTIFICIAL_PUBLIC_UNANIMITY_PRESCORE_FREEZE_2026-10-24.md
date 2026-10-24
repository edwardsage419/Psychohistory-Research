# R335 prescore freeze: artificial public unanimity and decision information gate

Date 2026-10-24. Original239 03-013 Groupthink Accounts. Status: PROTOCOL_FROZEN_BEFORE_OUTCOMES.

## English sources, reuse and scientific limits

Janis (1972), *Victims of Groupthink*, Houghton Mifflin; Janis (1982), *Groupthink: Psychological Studies of Policy Decisions and Fiascoes*, second edition. Esser (1998), *Alive and Well after 25 Years: A Review of Groupthink Research*, DOI 10.1006/obhd.1998.2758. Aldag and Fuller (1993), *Beyond Fiasco: A Reappraisal of the Groupthink Phenomenon*, DOI 10.1037/0033-2909.113.3.533, disputes strong claims of theory validity. R306 group polarization, R307 private/public minority influence, R304 social identity, R305 self categorization and R308 collective efficacy are related but none inspected implements the exact public unanimity, alternative search and truth feedback gate below. Early ZIP full content reuse remains OPEN. All numerical transitions here are project-created and do not claim to encode Janis' complete theory.

## Artificial universe and fixed algorithms

Enumerate truth t in {0,1}, private signals s1,s2,s3 in {0,1}^3, leader proposal l in {0,1}, imposed public pressure p in {0,1}, independent information audit e in {0,1}, in this exact nested order. There are 2*8*2*2*2=128 complete artificial conditions. For each condition emit three policy rows in order OPEN, PRESSURE, AUDIT, totaling 384 original artificial records. Each row fields: policy,truth,s1,s2,s3,leader,pressure,audit,public1,public2,public3,decision,correct. CSV uses CRLF and fixed ordering.

Define majority M=1 if s1+s2+s3>=2, else 0. OPEN publicly reports all three private signals and chooses M. PRESSURE publicly reports (l,l,l) and chooses l when p=1, otherwise behaves like OPEN. AUDIT publicly reports as PRESSURE; if p=1 and e=1, it overrides decision to known t, otherwise chooses PRESSURE's decision. Audit uses a hypothetical perfect truth oracle; it is an explicit upper-bound thought experiment, not an implementable human institution. The outcome correct is 1 iff decision=t.

For each of 128 conditions, store a JSON record with all six exogenous fields and the OPEN, PRESSURE and AUDIT decisions, correct indicators, and public unanimity indicators. JSON schema R335_frozen_public_unanimity_v1, indent=2, ensure_ascii=False and trailing newline.

## Frozen falsifiers

F1: exactly 384 CSV records, 128 condition summaries, all values binary except policy names.
F2: under p=1, PRESSURE has unanimous public reports in all 64 conditions; in 48 of those the three private signals are nonunanimous.
F3: when p=0, OPEN and PRESSURE have identical public reports and decisions in all 64 conditions.
F4: with p=1, PRESSURE decision differs from OPEN majority in exactly 32 of 64 conditions.
F5: AUDIT differs from PRESSURE decision in exactly 16 of the 32 p=1,e=1 conditions; AUDIT is correct in 80/128 conditions, versus OPEN 64/128 and PRESSURE 64/128. This result follows from the invented perfect truth oracle and exhaustive independent truth enumeration.
F6: independent no-import source auditor reproduces every row and condition, compares byte exact source and results, rejects a deliberately changed CSV decision and a deliberately changed JSON correct indicator.

Fail E1 acceptance if any prespecified falsifier fails. Passing means only finite deterministic arithmetic and observational public-unanimity counterexamples. It does not identify Janis' groupthink in real groups, validate historical decisions, show general causal effects, reproduce original author data, establish human E2 or historical E3. Keep R073/PESEN v0.1 frozen; finish R series before classification and fusion. Personal decision system deferred.
