# B track independent method audit: R293 S89

Date 2026-10-30 UTC. Track B. Evidence E1 synthetic, internal nonblind. Scope is R293 S89 new four worlds only, plus baseline parity against original R293. Protocol freeze commit a0a862befbf99ad5e350cdd2ae83aec02df6c2c4; data/result commit 24881b95b1fee8dc33b4a9a9674ad43302c69e3c.

## Actual execution

Independent Python 3.13.5 standard-library audit was executed locally using a separately generated full 2112-row source CSV and matching exact result JSON. Local source CSV is 278377 bytes, SHA256 a6632e8ddeded5efe7e82a1dc5a7f9c67bd6a0168f7d3f7a1e96e46bc29c16fd, Git blob 61e7c480fca45972760e37c72ed3e8e148603b13. Local JSON is 17786 bytes, SHA256 47f2bac6dbe2231f5bb33630e388a52741807b6159d5e9854d70347b0c5d4f9b, Git blob 33fadc22d56f2fbb85cc34401c79668b31808a51. Both Git blob identities match the exact remote newly created blobs.

The independent route uses latent covariance algebra Cov(Vi+S,Vj+S) = Cov(Vi,Vj) + Cov(Vi,S) + Cov(S,Vj) + Var(S), with Cov(Vi,S) equal to plus or minus twice Cov(Vi,b0). It does not import the R generator or enumerate its moment calculations. It checks all 800 exact covariance entries in four worlds, all 2112 source identities/probabilities, shift dependency, latent/raw/centered vectors, original R293 centered covariance baseline, and evidence boundaries. Result: PASS.

Eight explicit mutation controls were injected and rejected: duplicate source, missing source, wrong response-style shift, wrong probability, wrong raw score, wrong centered score, wrong covariance output, and unsupported E2 evidence promotion. All eight rejected in the local native Python execution.

## Limitations

The independent script was run locally against exact-byte-equivalent independently generated files; the newly persisted GitHub B script has not yet been executed from its remote checkout, and the archived R JavaScript file has not yet been executed using native Node CLI. Therefore remote-checkout native end-to-end execution is NOT_RUN. This is a nonblind independent mathematical implementation inside the same research workflow, not an external team replication. Formal S89 scientific acceptance PARTIAL. No new E2 or E3, no human survey, no external team, no CI. R073 and PESEN v0.1 frozen. Prior R281 S77 frozen failure retained.