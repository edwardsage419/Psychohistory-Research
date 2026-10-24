# R340 original239 04-007 SIS Epidemic Model: frozen prescore two-node CTMC protocol

Date: 2026-10-24. State: FROZEN_BEFORE_SOURCE_GENERATION. Scientific scope: constructed two-node continuous-time SIS generator E1 only.

## Sources and reuse

Pastor-Satorras and Vespignani (2001), DOI 10.1103/PhysRevLett.86.3200; Van Mieghem (2011), DOI 10.1007/s00607-011-0155-y. See docs/ORIGINAL_239_04-007_SIS_EPIDEMIC_REUSE_PREAUDIT_2026-10-24.md. Early R001–R064 ZIP strict reuse audit OPEN. No human or real epidemic data.

## Frozen exact universe

Two undirected adjacent nodes. States ordered 00,01,10,11 with bits indicating infection. Recovery rate gamma=1 per infected node. Infection of a susceptible node occurs at rate beta times its number of infected neighbors. Fix beta in exact fractions {1/2,1,2}. Construct the 4 by 4 continuous-time generator Q for each beta: for distinct states i,j, Q_ij equals the sum of the single-node infection/recovery transition rates from i to j; Q_ii is minus the sum of off-diagonal rates. Enumerate all 3 x 4 x 4 = 48 original artificial generator entries as CSV atoms, in beta, origin state, destination state order. Store exact rational numerator/denominator strings or Python Fraction representation in a frozen specified column; no floating point rounding. Save all matrices and first-event probabilities as JSON with canonical ordering. Python 3.11 and 3.12 standard library only.

F1: 3 beta worlds, 4 states each, 48 original source entries.
F2: 00 is absorbing for all beta; its generator row is all zero.
F3: 01 and 10 each have one infection transition at beta and one recovery transition at 1; 11 has two distinct recovery transitions each rate 1.
F4: every generator row sums exactly zero; all off-diagonal rates nonnegative.
F5: from 01, probability the next event is infection is beta/(1+beta), giving 1/3,1/2,2/3 for the three beta values. Complementary recovery probabilities 2/3,1/2,1/3.
F6: independent no-import Fraction audit must recreate all source bytes and reject deliberate CSV and JSON tampering.
F7: GitHub Actions python311, python312, independent all success before formal E1 acceptance.
F8: source commit follows this protocol freeze commit. R073 and PESEN v0.1 unchanged.

## Limits

Potential acceptance PASS_BOUNDED_E1_CONSTRUCTED_TWO_NODE_SIS_GENERATOR_ONLY. A two-node finite chain has disease-free absorbing state and cannot establish scale-free epidemic threshold behavior, metastable prevalence, large-network persistence, real infection dynamics, human E2, historical E3 or original 2001 empirical replication. Catalogue linkage is provenance only. No scientific acceptance until source, audit and CI verified. Complete R series before taxonomy and fusion; personal decision system deferred.
