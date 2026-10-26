# R199 hidden-label probabilistic Brier under label switching: third-method prescore freeze

Date: 2026-10-27. Additive internal E1 mathematical question. The original R199 prescore protocol, 24-world scientific acceptance, and six-model fitting and Viterbi results remain unchanged.

## Frozen universe

Use exactly two of the original R199 true HMM mechanisms: BASE with a=3/4, r=3/4, and LABEL_SWAPPED with a=3/4, r=1/4. Initial X1 is fair. Each X[t+1] equals X[t] with probability a; Yt equals Xt with probability r. Include full visible sequence lengths L=3 and L=4. This yields four true-source settings. Enumerate every binary observed Y1..YL and every latent X1..XL. No fitted parameters or selected hyperparameters.

## Frozen comparison and outcomes

Compare three prespecified probabilities for each latent Xt conditional on the complete Y sequence: (1) TRUE_LABEL_POSTERIOR computed under the true model, (2) OPPOSITE_LABEL_POSTERIOR computed using the other label-swapped model, and (3) UNCONDITIONAL_HALF fixed at 1/2. Score the actual artificial hidden Xt using binary Brier loss, averaged uniformly over the L positions and over the complete true joint (X,Y) distribution. Report exact risk for each of four settings, true versus opposite excess Brier, and true versus half improvement. Also verify exact equality of all observed-sequence probability masses under BASE and LABEL_SWAPPED and complementarity of all per-time hidden posteriors.

The main calculation uses forward-backward smoothing; the independent B calculation must enumerate all latent X paths and directly compute the full joint Brier. All arithmetic rational and exact. Primary identity: opposite-minus-true risk equals the source-weighted average over Y and t of (1-2 P_true(Xt=1|Y)) squared. Negative control: deliberate label reversal must be detected, while the observed-data likelihood alone cannot distinguish the labels. No after-score adjustment.

This is an in-sequence artificial hidden-state inference test with full observation Y, not a new independent future-outcome prediction test. Human E2=0, historical E3=0, external independent replication=0. R073 and PESEN v0.1 remain frozen. No paid computing or unverified CI.
