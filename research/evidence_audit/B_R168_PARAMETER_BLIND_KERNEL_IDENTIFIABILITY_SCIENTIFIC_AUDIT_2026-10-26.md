# B independent-method audit: R168 observable kernel sufficiency and executed mutations

Date 2026-10-26. Protocol frozen in commit `8cc8f44bf64bc630874f12c540c64e1a2ced0c4d`. Original archived R168 E1 JSON blob `053c7fb851638e4ec4f0838afff7ee78603d2818`.

## Different-method route
Main R168 third-method program derives A and B from original synthetic (u,f,m) and rebuilds the kernel. The B audit intentionally ignores all parameters, including population size and access mode. It reads only the two observable cells K[0,0] and K[2,1] of each archived kernel and reconstructs the remaining seven cells. This independently tests whether the **observable** full matrix contains information beyond the two effective probabilities.

The executed JavaScript BigInt exact rational program [source](r168_b_kernel_observable_reconstruction_20261026.js), blob `7e3845f6cf714d3a3ded316e134610c85cdd2da9`, checked **288/288** original matrix cells. Both parameter-blind observable pairs and full matrices yield 16 classes with identical class-size distributions `[5,4,4,4,2,2,2,1,1,1,1,1,1,1,1,1]`. Full [execution receipt](B_R168_OBSERVABLE_KERNEL_RECONSTRUCTION_RECEIPT_2026-10-26.json) preserves source identity and results.

## Actually executed negative controls
For each of 32 original kernels, the B script makes one mutant changing K[1,0] by +1/100 and a second mutant changing K[2,1] by +1/100. It recalculates the observable reconstruction and requires at least one exact mismatch for each mutated matrix. **64/64 mutants detected**, zero failures. These artificial mutants need not remain stochastic matrices; they verify algebraic integrity, not model misspecification power on realistic human behavior.

## Validation scope
The original synthetic E1 kernel has no empirical train/test partition. Leakage checks, probability calibration, out-of-sample scores, session bootstrap and human confidence intervals are inapplicable to this purely exact mathematical identity and were not invented. A complete transition matrix being observationally insufficient is stronger than merely observing one trajectory, but remains confined to the frozen project-authored process. The B route is a distinct internal method executed by the same project. No external research-team independent replication, new E2 human evidence, or E3 historical evidence was obtained. R073 and PESEN v0.1 remain frozen. Remote GitHub CI was not triggered or verified as passed.