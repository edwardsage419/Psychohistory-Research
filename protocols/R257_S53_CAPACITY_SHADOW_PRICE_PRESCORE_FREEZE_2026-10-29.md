# R257 S53 capacity sensitivity prescore protocol

Date: 2026-10-29. Evidence class E1, finite artificial mathematical mechanisms only. This is an addendum to original R257, whose final acceptance and original 225 candidate atoms remain frozen. No new real human E2 or historical E3. R073 and PESEN v0.1 remain frozen.

## Predeclared research question

Does a capacity constraint's exact KKT multiplier equal a finite one sided change in the optimal value when the capacity changes? Distinguish the local derivative from coarse finite differences and identify an off grid active set transition.

## Frozen input and exclusion

Read the original R257 eight strictly convex triangle projection worlds, with unchanged targets (a,b) and baseline capacities C0. Objective f=(x-a)^2+(y-b)^2, constraints x>=0, y>=0, x+y<=C. The ninth original nonconvex world is an explicit negative control excluded from any convex multiplier sufficiency claim. The original 225 grid candidates are unchanged; new capacity scenarios are mathematical counterfactuals and are not additional original source atoms.

## Frozen design

For each of eight convex worlds evaluate the exact continuous optimum and minimum at C in {C0-1/4,C0-1/16,C0,C0+1/16,C0+1/4}. All capacities remain positive. Compute four one sided secant slopes at h in {1/4,1/16}: L_h=[v(C0)-v(C0-h)]/h, R_h=[v(C0+h)-v(C0)]/h. Independently compute baseline KKT capacity multiplier lambda. Compare lambda with the exact local derivative -lambda, where the active set is stable in a neighborhood. Do not equate coarse finite differences with the local derivative. For the interior off grid world check the capacity threshold a+b=4/5 and the case C0-h<4/5<C0. Include convex monotonicity checks L_h<=R_h<=0, and independent global lower bound v(C)>=v(C0)-lambda(C-C0) for the five capacities. Record the number of exact evaluations and failures.

## Independent B verification

Before inspecting the generated R receipt, calculate all five capacity values using a separate one dimensional boundary formula or complete vertex/face minimization, compare exact rational objectives and points, and inject an intentionally incorrect value into a comparator. Audit causal interpretation, future information leakage, absence of heldout human data, and external replication status.

## Acceptance and limits

PASS requires exact rational checks for all 40 capacity evaluations, 32 secants, eight baseline multipliers, negative control, and source identity consistency. All claims remain E1. No claim of empirical utility measurement, policy impact, out of sample prediction, uncertainty interval from human sampling, or independent external replication. CI must not run unless its no cost status is confirmed.
