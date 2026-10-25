# B audit: independent generating-function validation of R157 scaling

Date: 2026-10-25. Protocol: research/validation/R157_PRODUCT_SCALING_IDENTIFIABILITY_PROTOCOL_FREEZE_2026-10-25.md, committed before calculation. Main method: Node.js exact finite convolution and archived 72-world replay. Audit method: independent Python standard-library Fraction formal generating-function coefficient multiplication.

## Separate derivation
With zero initial states, define the ordinary generating functions M(z), E(z), F(z). For H=1 and r=0, the transfer functions are:

M(z) = a z / ((1-z)(1-(1-a)z)).
E(z) = b z M(z) / (1-(1-b)z).
F(z) = c z E(z) / (1-(1-c)z).

The B program constructs truncated power-series products for t=0..12 using polynomial multiplication, independently of the main JavaScript algorithm and original R157 transition functions. It independently verifies the H^3(1-r) product identity, 936 exact product factorization cells, 2808 state scaling cells, 48 positive time-three cases and three negative controls. For a=b=c=1/4 it agrees with the main method's exact counterexample values P3=185/1048576 and P12=2345008149288796188925/37778931862957161709568.

Python source: `r157_b_independent_generating_functions.py`, Git blob `f5d0d9beaa318300a7fb2e86cce39260397aae47`; local execution SHA256 `a9da736ba7aab84b0642eaa63257df7c7d5fae7ed4a10d532dff06db8bc262a3`. Receipt SHA256 `b107efc4556f9a20685ae6ce1937d47b8fcdb9842ca13f6445601dec764a6c5b`. The archived source blob was matched byte-for-byte to the local script used for execution.

## Independent audit verdict
The mathematical all-time product confounding follows from linearity. It is a structural nonidentifiability example under product-only observations and fixed lag rates. The full component time series has more information. Finite grid uniqueness, if observed, cannot prove continuous parameter identifiability.

No real sample exists in this validation, so leakage, held-out prediction, probability calibration, uncertainty intervals and human independence cannot be scored. They are marked NOT_APPLICABLE_TO_E1 rather than PASS. There is no new E2 or E3, no independent external research team, and no historical risk prediction. No changes to R073, PESEN v0.1 or original239.

**Result: PASS_BOUNDED_INTERNAL_TWO_METHOD_E1**. Research acceptance remains limited to the constructed mechanism.
