# R159 Precode frozen protocol: 48 artificial cultural transmission worlds with conformist majority and unbiased copying

Date 2026-10-21. Original catalog **P1 / 07-001 Dual Inheritance Theory**. R158 CLOSED_BOUNDED_E1, baseline main commit 8ae900208c33db352fa9c454ed48b38ece73b2c9. Sequence: all R models first, then classification and fusion.

## Directly verified original author sources and scope
* Cavalli-Sforza, L. L. & Feldman, M. W. (1981), *Cultural Transmission and Evolution: A Quantitative Approach*, Princeton University Press [original publisher book entry](https://www.jstor.org/stable/j.ctvx5wbt8). Publisher description says the authors separately analyze modes of cultural transmission (including parent-child, peer-peer and teacher-student) using quantitative analogues of inheritance.
* Boyd, Robert & Richerson, Peter J. (1985), *Culture and the Evolutionary Process*, University of Chicago Press [publisher book with original table of contents](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html), chapters on the cultural inheritance system, guided variation and biased transmission.
* Henrich, Joseph & Boyd, Robert (1998), *The Evolution of Conformist Transmission and the Emergence of Between-Group Differences*, *Evolution and Human Behavior* 19(4):215–241 DOI [10.1016/S1090-5138(98)00018-X](https://doi.org/10.1016/S1090-5138(98)00018-X), [original publisher abstract](https://www.sciencedirect.com/science/article/pii/S109051389800018X), [author university record](https://henrich.fas.harvard.edu/publications/evolution-conformist-transmission-and-emergence-between-group-differences). Authors discuss conformism, learning, and among-group variation.
Full original book chapters and original 1998 equations/datasets were not rederived. Experiment is **project authored toy single-frequency cultural-copying process**, not reproduction of gene-culture coevolution, genetic inheritance, dual-path selection or original 1998 model. Original theory includes much more than one frequency curve. No real cultural behavior data; E1 only.

## Frozen 48 synthetic cultural trajectories
Artificial binary cultural trait A has fraction p in [0,1], with no genotype, payoffs, household structure or geography. Start at p0∈{1/4,2/5,3/5,3/4}. "Conformist" independent three-sample majority probability C(p)=p³+3p²(1−p), equivalently 3p²−2p³. A synthetic copying mixture h∈{0,1/4,1/2,1} chooses conformist imitation with rate h and unbiased random copying with 1−h. A symmetric artificial innovation/reset share u∈{0,1/10,1/4} replaces that temporary selection with the equiprobable cultural trait 1/2. One-generation update
p[t+1] = (1−u)*((1−h)p[t]+h C(p[t])) + u/2.
Exactly 4×4×3=48 preregistered worlds, time t=0,...,6 inclusive (7 observations).

## Independent exact mathematics and controls
Method 1 exact Fraction polynomial C(p)=3p²−2p³ and update.
Method 2 enumerate all eight triples of {0,1} as independent social exemplars and accumulate \(\sum_{b_1+b_2+b_3\ge2}p^{\sum b}(1-p)^{3-\sum b}\); implement this evaluator separately without calling method 1 or using its intermediate frequency results, then iterate the same defined mixture. Both full 48×7 trajectories must be strictly Fraction equal; result JSON must include full p[t], sample majority rates, parameters and method identity.

Prespecified mathematical tests:
1. For every p∈[0,1], 0≤C(p)≤1, symmetry C(1−p)=1−C(p), and C(1/2)=1/2.
2. With h=0,u=0, p stays constant in all 7 periods.
3. With h>0,u=0, all p0<1/2 strictly decrease and all p0>1/2 strictly increase; this follows C(p)<p below half and C(p)>p above half (only in this constructed independent triple sampling).
4. With h=0,u>0, \(p_t=1/2+(1-u)^t(p_0-1/2)\) verified exactly for all matched cases.
5. With p0=1/2, every h and u keeps p_t exactly 1/2, so even a complete constant half-frequency history cannot identify these parameters under this model (specific counterexample only).
6. With p0=0 or1 and u=0, p is absorbing; u>0 breaks that absorption. These are special tests outside the 48 frozen main cases.
7. For equal initial p and h, positive u shifts the one-step output toward half relative to u=0; do not claim it always dominates multiple-generation conformism.
8. External people, family, spatial cluster, genetic dynamics and empirical validation excluded. Avoid describing any protected group or political identity as a selected trait.

## Acceptance
Implement two independent Fraction routes, ≥48 named full-world tests plus additional distinct boundary tests, deterministic complete 48-case JSON, source/tests ZIP, CI on Python 3.11 and 3.12 and immutable four SHA256, permanent archive to GitHub main with readback before bounded E1 closure. R073/PESEN v0.1 remain FROZEN; next candidate must be looked up from original catalog rather than invented.
