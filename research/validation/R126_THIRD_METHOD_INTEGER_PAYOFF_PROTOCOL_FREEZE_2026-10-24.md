# R126 strict-reuse third-method integer-payoff audit protocol freeze

Date: 2026-10-24. State: FROZEN BEFORE THIRD-METHOD CODE AND DATA. Original239 05-002 Public Goods Game. Reuse existing R126; do not create another R series model.

## Source and reuse

Original R126 has already read Fehr and Gächter (2000), *Cooperation and Punishment in Public Goods Experiments*, AER 90(4):980–994, DOI 10.1257/aer.90.4.980, printed pp. 981–985, with source formulas Eq.(1)/(2), Table 2 nonlinear cost and Table 3 published aggregates. Existing R126 source Git blob `dc5cc7da900c8175dd14f4751f00e610e52250c7`, report blob `4ef8f1b48dc7191e2e66009d479af0ed5b136827`, existing final CI `39347160953` and 57 unit tests. The 112 real people are the paper's reported participants; this new audit obtains no individual records.

## Falsifiable third method and finite roster

For each of 625 integer contribution vectors in lexicographic `{0,5,10,15,20}^4` and eight fixed punishment matrices below, independently calculate all four final payoffs by exact integer numerator `(100-5*g_i+2*G)*(10-P_i)-50*C_i`, denominator 50, where `G=sum(g)`, `P_i=min(10,sum_{j != i} points[j][i])` and `C_i=sum_{j != i} cost(points[i][j])`. Freeze Table 2 sender cost `[0,1,2,4,6,9,12,16,20,25,30]`. Do not call the original R126 stage1, punishment, or group-surplus helpers in constructing third-method values. Compare all four exact fractions against the unchanged original R126 punishment_payoff and the sum against unchanged original independent_punishment_group_surplus. Archive 5000 complete constructed scenario rows with contribution vector, pattern ID, exact integer numerator of each payoff and total numerator, plus source-comparison boolean. No numerical tolerances.

The eight ordered matrices, each four rows of four sender-to-receiver points, are:
0 all zeros;
1 only sender0 to target3 =1;
2 only sender1 to target3 =2;
3 sender0/1/2 to target3 =6/7/10;
4 sender0 to target1 =3 and sender1 to target0 =4;
5 each sender i to target (i+1)%4 =1;
6 senders1/2/3 each to target0 =10;
7 sender1 to target0 =5, sender2 to target1 =3, sender3 to target2 =2.
All other cells zero; diagonal zero.

## Frozen acceptance and negative controls

Require exactly 625x8=5000 scenarios and 20,000 person-payoff comparisons. Independently verify no-punishment case g=(0,0,0,0) gives four 20; g=(20,20,20,20) gives four 32. For g=(20,20,20,0) and pattern1+2 combined (not one of eight single patterns), require final [23,22,24,154/5], group 499/5. For pattern3 with g=(20,20,20,0), require group 14, recipient payoff 0 and sender3 may be negative. Published Table3 final punishment displayed simple mean 12.4 versus printed Mean 12.3 remains unresolved, not corrected or called a new E2 estimate. Reject incorrect original Git source SHA and mutated CSV. Rerun all 57 original tests in Python 3.11 and 3.12 on free standard public Ubuntu runner. No paid API or large runner.

Ceiling `PASS_BOUNDED_INTERNAL_INTEGER_PAYOFF_E1`. No new human E2, historical E3, new behavioral punishment effect, original Wilcoxon replication, external team reproduction, or R073/PESEN changes. If any mismatch occurs preserve the failure, do not revise the frozen roster or acceptance criteria after results.
