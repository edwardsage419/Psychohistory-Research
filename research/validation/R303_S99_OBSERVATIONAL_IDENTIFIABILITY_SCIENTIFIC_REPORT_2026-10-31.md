# R303 S99 scientific report: exact observational equivalence

Date: 2026-10-31 UTC. Target (r,R303,S99-v1,observational-equivalence-and-latent-acquisition-identifiability). Prospective S99 freeze commit: `47c82ad9419913b121ae64d655a806eccd071b55`, created before S99 computation. Original R303 freeze: `5adc32ae7c91c150fe82bb16f99a059d2a62e991`. Original 486 sources and original bounded E1 acceptance remain untouched.

## Question and methods

Under the original project's synthetic R303 equations, can the six exact observable response probabilities from three vicarious consequences and two expression phases uniquely determine latent observational acquisition? Exhaustively enumerate 3^4=81 tuples of A,R,P,M in {0,1/2,1}. Define latent acquisition L=A*R, available response V=A*R*P, spontaneous response S_C=V*M*c_C and incentivized response I_C=V, with original c_C=(1,1/2,1/4). Each tuple generates a six-dimensional exact Fraction signature. The S99 protocol froze class grouping, negative controls, witness and summary metrics before execution. All worlds are artificial.

## Exact results

* 81 artificial gate tuples collapse into **13 distinguishable observable signatures**.
* Class-size histogram: **6 singleton classes, 6 classes with 3 members, 1 class with 57 members**. The 57-member class has all six observed probabilities zero, since V=0.
* **7 of 13 classes** contain more than one latent acquisition L; **75 of 81 artificial tuples** lie in these classes. Maximum within-class L spread is **1**.
* All 13 classes have a single V. Exactly one class, the zero-V class, contains multiple M values. Thus exact incentivized responses reveal V; for V>0, the rewarded spontaneous response divided by V reveals M under the assumed model and known consequence. A,R,P remain generally confounded.
* Prespecified witness: (A,R,P,M)=(1/2,1,1,1) yields L=1/2; (1,1,1/2,1) yields L=1. Both give the same six observable probabilities (1/2,1/2,1/4,1/2,1/8,1/2).

The 57 zero-output worlds include mechanisms with L=0 and with L>0 but P=0. Even perfect knowledge of all six probabilities cannot distinguish these latent mechanisms in the stipulated model. Additional measurements or interventions on attention, retention or production would be necessary for stronger identification; no such experiment is performed here.

## Reproduction and scientific status

The archived Python generator uses exact rational arithmetic, emits 81-row CSV, 13-class JSON and SHA256 receipt. Local Python `--test` ran 3 tests PASS; `--emit` generated files. Independently coded B Python auditor, without importing R generator, used a separate algebraic partition by (V,M) for V>0 and one zero-V class; all 81 tuples and 13 classes PASS. Eight prespecified mutation controls all rejected. Original R303 486 archived source-phase rows were separately read from main Git blob `e42d2df75f4876c2735ece421d2e55efaed8eb31`; all 486 had unique world-phase keys and agreed with original L,V and observable equations. These are internal nonblind checks, not external independent replication.

R CSV SHA256: `bce83b3dfdd06dc31933e4c26113510916581caedc127d91b2fd724d8ea83c18`. R JSON SHA256: `f31348fe3f3e7777be19f8159afc1d28ec97f68396aecc01d5933fbc41b593e5`.

A01 scope PASS; A02 original R303 source and frozen equations PASS within synthetic scope; A03 local execution PASS, CI NOT_RUN; A04 counterexample and 8 negative mutations PASS; A05 inference limited to E1; A06 archive and remote commit to be verified after commit. **S99 scientific status PARTIAL**. No original Bandura child-level data, no observed learning or individual latent state measurement, no probability calibration on humans, no external replication. The 75/81 ratio is a finite grid count, not an empirical prevalence. Original R303 `CLOSED_BOUNDED_E1` unchanged. New E2=0, E3=0; R073 and PESEN v0.1 frozen.

Original study: Bandura (1965), DOI:10.1037/h0022070. This project's product-gate equations are not Bandura's fitted equations.
