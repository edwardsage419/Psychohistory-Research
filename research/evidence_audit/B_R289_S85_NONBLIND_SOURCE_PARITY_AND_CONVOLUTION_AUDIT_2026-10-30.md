# B track: R289 S85 exact source parity, convolution and negative controls

Date 2026-10-30 UTC. Target (B,R289,S85-prescore-f0182369,paired-full-training-threshold-selection). Internal nonblind E1 audit. Original R289 scientific acceptance unchanged.

## Prior reading and fixed identities
Original source research/R289/R289_ALL_486_ORIGINAL_SEQUENTIAL_OFFER_SOURCES.csv Git blob 261d821044278d05db1d15e85e20cef8aafbe5a4, original R289 Python source blob 426a63a793ca84c474c8a6a1a2c378efde4db601, original result JSON blob 4b245b160db5e9808916dc9251e888f8683c6ee2.
Prescore S85 commit f018236900fa00368c8980db5402ce4267d59c7c.
New R JS source Git blob 89470060567b42ecb1483b35eb00320a17563ba8; new 243-row CSV Git blob 62a2bd969497fb9abd6ffa772d55016d22ce0da3; exact JSON Git blob 76b288491d7eaabe92dbfae7f9746baa9d41a06a. Independent Python B source Git blob bed482d31e3ffe445f26ca2661d21260c3bc2496.

## Actual checks performed
1. Executed the new R source in V8. It enumerated all 243 paired source rows and 81/6561 ordered training histories per DGP and training length, with integer weighted exact arithmetic. It checked original R289 population H3/H5/first-only means.
2. Executed a separate signed-difference polynomial convolution in V8, with m=1 and m=2, agreeing on six P(select H5) and six training tie probabilities.
3. Read the actual GitHub-persisted original 486-row CSV and new 243-row ledger. Independently checked all 486 original threshold/source pairs, their source probabilities and net rewards against the derived paired rows; checked all 243 differences and six independent probability convolutions. Original source coverage 486/486, derived 243/243, all matched. This is source parity, not an independent blind original-paper replication.
4. Independently wrote and executed a standard-library Python Fraction route locally, with 81 offer combinations per DGP and exact difference PMF convolution. The local Python --test command reported 9 positive assertions PASS; its six world summaries matched all R probabilities and means. The archived Python source file was created in GitHub, but its exact remote bytes have NOT been run in a native Python process.
5. Fetched the persisted R JS source, CSV and JSON again from GitHub. Re-executed the remote JS in V8; generated CSV 6689 characters and JSON 5043 characters were EXACTLY byte-equivalent to persisted content in the UTF-8 response. Six negative controls rejected: duplicate source, missing source, source weight alteration, payoff alteration, signed-difference alteration and wrong tie policy. All training ties remain in denominators and select H3.

## Methodological audit
No target/test outcome enters the training threshold selection; independent test expectation is integrated analytically using the fixed true DGP. Training has paired full-information episodes, which cannot generally be obtained from ordinary early-stopped online search without observing unchosen offers. This is a key applicability limitation. Population-optimal H3/H5 is an oracle of fixed policy means only, not a clairvoyant future-offer oracle.
More training from 1 to 2 episodes increases finite-sample wrong-selection probabilities in UNIFORM (25/81 to 2819/6561) and LOW_HEAVY (55/256 to 19569/65536), while decreasing in HIGH_HEAVY (93/128 to 4533/8192). The exact finite-sample nonmonotonicity is retained as a negative finding, without extrapolating to arbitrary sample sizes.
No independent real human observations, no probabilistic calibration study, no causal inference, no resampling confidence intervals required for this exhaustive finite artificial distribution. No new E2 or E3 predictions. External independent research team replication remains 0.

## Gates
A01 PASS bounded question; A02 PASS fixed original blob and full source parity; A03 OPEN native Node on archived R JS and native Python on archived B source; A04 PASS six mutation controls and ties; A05 PASS E1-only scope; A06 OPEN external independent replication and full native archive execution. S85 SCIENTIFIC_ACCEPTANCE=PARTIAL.
No paid resources, GitHub Actions or cloud compute started. Billing/quota not independently checked. R073 and PESEN v0.1 FROZEN.
