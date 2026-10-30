# R292 S88 scientific report: noisy perceived control attenuates predictive information

Date: 2026-10-30 UTC. Track: R primary. Evidence: E1 artificial exact; internal nonblind; S88 scientific status PARTIAL.

## Freeze and original scope

The S88 prescore design was committed first at `19f1992f73d7dc6b525d1a523b36d9dd24659bbf`. Original R292 protocol and all eight original artificial worlds remain unchanged. Original R292 formal bounded E1 status CLOSED_BOUNDED_E1 remains intact. Ajzen 1991 TPB is the first-party conceptual anchor: https://people.umass.edu/aizen/obhdp.html ; DOI 10.1016/0749-5978(91)90020-T. All numerical coefficients and proxy noise regimes are synthetic research constructions.

## Actual generated materials and exact arithmetic

New standalone JS generator: `research/validation/r292_s88_noisy_perceived_control_20261030.js`.
Source CSV: `research/validation/R292_S88_ALL_1536_NOISY_CONTROL_SOURCE_CELLS.csv`.
Exact JSON: `research/validation/R292_S88_EXACT_RESULTS.json`.

Eight frozen R292 worlds crossed with three prespecified measurement error rates e=0,1/4,1/2. Each world enumerates 64 labelled (A,N,C,I,F,Z) cells, including zero-probability cells. Total 24 worlds, 1536 cells. Source mass is 1 in each world. For e=0, each world has 32 positive cells and 32 zero cells; for e=1/4 or 1/2 all 64 cells have positive mass. All arithmetic uses exact integer weights and rational output.

The action target B=I*F is scored before I and F are observed. ORACLE_ANC knows true latent C; FULL_ANZ sees the noisy Z; TRA_AN sees A,N; CONSTANT sees neither. All are exact Bayes forecasts for their respective information sets, evaluated over an independent draw from the frozen DGP. No fitted empirical parameters.

Define V=(c+4kappa)^2/1024 + kappa^2(a^2+n^2)/4096 and t=1-2e. Exact analytic result:
* R(TRA_AN)-R(FULL_ANZ)=t^2 V.
* R(FULL_ANZ)-R(ORACLE_ANC)=(1-t^2)V.
* R(CONSTANT)-R(TRA_AN)=(a^2+n^2)/1024.

Thus at e=1/4 the additional predictive value of observed control falls to one quarter of its original value, while three quarters of its original advantage over the oracle is lost. At e=1/2 the observed control score adds zero Brier improvement over A,N, even if true C is predictive. This result depends on the symmetric, nondifferential misclassification mechanism frozen here.

## Selected exact world results

| Profile | kappa | e | Oracle Brier | Noisy ANZ Brier | AN Brier | AN minus ANZ |
|---|---:|---:|---:|---:|---:|---:|
| BALANCED | 1 | 0 | 689/4096 | 689/4096 | 791/4096 | 51/2048 |
| BALANCED | 1 | 1/4 | 689/4096 | 1531/8192 | 791/4096 | 51/8192 |
| BALANCED | 1 | 1/2 | 689/4096 | 791/4096 | 791/4096 | 0 |
| CONTROL_NULL | 1 | 0 | 347/2048 | 347/2048 | 95/512 | 33/2048 |
| CONTROL_NULL | 1 | 1/4 | 347/2048 | 1487/8192 | 95/512 | 33/8192 |
| CONTROL_NULL | 1 | 1/2 | 347/2048 | 95/512 | 95/512 | 0 |
| CONTROL_NULL | 0 | any | 95/512 | 95/512 | 95/512 | 0 |

CONTROL_NULL kappa=0 is the negative control. In CONTROL_NULL kappa=1, C enters feasibility information without entering the intention equation, but noisy measurement attenuates the observed control signal.

## Validation, interpretation and limits

The R generator ran in V8 and produced all source rows and result bytes. Independent B audit re-read persisted GitHub source CSV and result JSON, reconstructed conditional probabilities by grouped weighted outcomes without importing the R generator, checked 6144 conditional forecast cells, all 24 exact risks, eight original R292 baseline comparisons, and rejected eight malformed controls. Internal nonblind method verification passed. Original Node CLI from the archived file NOT_RUN. No new GitHub Actions triggered; external independent replication NOT_RUN. S88 formal scientific acceptance remains PARTIAL.

These results show an exact synthetic information loss under measurement error. They do not identify real-world perceived control as a causal driver, prove that subjective scores measure feasibility, or estimate actual human predictive performance. E1 only, new E2=0, E3=0, R073/PESEN v0.1 frozen. Original 239 catalogue and 154-item pending queue unchanged. Further work: original Node CLI execution and receipt verification, independently fielded human data, sensitivity to asymmetric and differential measurement error under a new prospective protocol.
