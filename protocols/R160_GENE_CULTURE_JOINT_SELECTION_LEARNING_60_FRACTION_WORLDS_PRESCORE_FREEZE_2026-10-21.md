# R160 precomputation freeze: bounded two-state genetic and cultural frequency feedback

Date: 2026-10-21. Original catalogue P2 / 07-002 Gene Culture Coevolution. Verified parent main `3445e1c12d3114b18384caff3e6e6a465037674a`, R159 CLOSED_BOUNDED_E1. **All parameter cases and mathematical tests frozen before program implementation.**

## Sources read and scope of replication
Feldman & Laland (1996), "Gene-culture coevolutionary theory", *Trends in Ecology & Evolution* 11(11):453–457, DOI [10.1016/0169-5347(96)10052-5](https://www.sciencedirect.com/science/article/pii/0169534796100525), original publisher abstract directly verified. Feldman & Zhivotovsky (1992), "Gene-culture coevolution: toward a general theory of vertical transmission", *PNAS* 89(24):11935–11938, DOI [10.1073/pnas.89.24.11935](https://pmc.ncbi.nlm.nih.gov/articles/PMC50672/), original peer-reviewed public full-text page and abstract verified. Laland, Odling-Smee & Myles (2010), "How culture shaped the human genome", *Nature Reviews Genetics* 11:137–148, DOI [10.1038/nrg2734](https://www.nature.com/articles/nrg2734), original Nature publisher review abstract and key points verified. These works discuss *joint* genetic and cultural transmission and culture-dependent selection across generations. **Do not claim to implement their original complete equations, original estimates or original empirical data**. The novel equations here are a project-authored synthetic 2×2 frequency demonstration, with asexual inherited binary gene tag, no Mendelian genetics, mating, migration, demography, fitness data or actual culture groups. All identifiers G0/G1 and C0/C1 are fictional, with no reference to human populations or demographic identities.

## 60 frozen joint distributions and four exact generations
Representation: joint p(g,c), g,c∈{0,1}, entries \(p_{00},p_{01},p_{10},p_{11}\) sum to one. Five initial rows in order (00,01,10,11):
I0 uniform=(1/4,1/4,1/4,1/4);
I1 positive association=(3/8,1/8,1/8,3/8);
I2 negative association=(1/8,3/8,3/8,1/8);
I3 C0-only=(1/2,0,1/2,0);
I4 C1-only=(0,1/2,0,1/2).
Parameter grids: fitness-coupling s∈{0,1/2}; cultural majority copying h∈{0,1/2,1}; cultural horizontal updating u∈{0,1/4}. **5×2×3×2=60 worlds**, each t=0,..,4 inclusive (five 2×2 joint tables).

Stage 1 normalized project-specific haploid selection, with \(w_{gc}=1+s\cdot g c\) (only artificial G1,C1 pair receives weight 1+s):
\(Z=1+s\,p_{11}\), \(a_{gc}=w_{gc}p_{gc}/Z\).
Stage 2 cultural horizontal replacement at share u, preserving postselection genetic marginal \(a_g=\sum_c a_{gc}\). Postselection cultural C1 fraction \(v=a_{01}+a_{11}\), independent 3-demonstrator majority \(C(v)=3v^2-2v^3\), model target \(q=(1-h)v+hC(v)\). Updated joint
\(p'_{g1}=(1-u)a_{g1}+u a_g q\),
\(p'_{g0}=(1-u)a_{g0}+u a_g(1-q)\).
Do **not** identify q as a measured population behavior, or fitness coupling as genetic advantage in any real person.

Primary replay method: direct exact Fraction formulas.
Independent arithmetic oracle: enumerate four class weights (00,01,10,11) without using primary update, enumerate eight sample triples for cultural-majority q, and accumulate final output by summing retained and replacement mass for each g,c. The oracle does not call primary model, and both return four Fraction cells; all 60×5 tables, both marginals, and association D=p11−P(G1)P(C1) must agree by exact equality. All tables sum to exactly 1 and remain in [0,1].

## Prespecified counterexamples and checks
1. I1 and I2 both have genetic G1=1/2 and cultural C1=1/2 but opposite D=+1/8,−1/8. With s=1/2, u=0, next G1=11/19 versus 9/17. Therefore marginal frequencies alone fail to fix gene response under this toy joint fitness rule. **This does not prove genetic effects in real societies.**
2. For s=0, G1 marginal exactly conserved for every generation and every h,u; culture-only copying cannot alter gene marginal in this constructed transmission equation.
3. If u=0, cultural copying parameter h is entirely inactive; histories for all h must match exactly when s and initial distribution held fixed. This is a structural partial parameter-identification control.
4. For s=0, I1 and I2 at baseline C1=1/2, u=1/4, any h, the C1 and G1 marginals remain 1/2 while |D| contracts from 1/8 to 3/32 in one generation.
5. For initial I3 with no C1, no C1 ever appears under the project mutation-free update even if s>0,h>0,u>0. For initial I4 all C1, its frequency remains 1; new variants cannot appear without a mutation/innovation term (this protocol excludes one).
6. At u=0 and s=0 all joint tables stay exactly constant. If s>0 and 0<G1<1 and P11>0, the gene G1 fraction strictly rises after selection under the chosen w, regardless of h,u (as culture-stage switching preserves gene totals).
7. Extreme C1=1/2 and s=0 steady state with u>0 and h arbitrary preserves trait marginals but erases gene-culture covariance gradually; this demonstrates that marginals do not identify the full joint distribution.
8. Reject input matrix dimension errors, negative or above-one frequencies, total mass ≠1, invalid rate fractions or types, negative horizon or bool. No floats permitted in the exact oracle.

## Acceptance and archive
At least 60 distinct named scenario tests and >=20 separate negative/edge tests, deterministic entire JSON ledger with five 2×2 snapshots and their gene/culture marginals and covariance, 2 Python versions (3.11/3.12) real tests, canonical four SHA256 (source/test/JSON/ZIP), complete standard-library ZIP to permanent GitHub main and independent readback before closure. Frozen evidence grade **E1 computational algebra only**. E2 new 0, E3 new 0; R073 and PESEN v0.1 frozen. Next planned original catalog is R161 P1/07-003 Conformist Transmission, subject to verification after closure. Research continues all R models first, then classification and fusion.
