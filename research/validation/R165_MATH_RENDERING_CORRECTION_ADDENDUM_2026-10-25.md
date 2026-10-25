# R165 formula rendering correction

Date: 2026-10-25 Asia/Singapore. This addendum corrects display escaping in \`R165_HETEROZYGOSITY_AUTOCOV_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md\`. Some TeX delimiter backslashes were lost during text serialization. The original file is retained unchanged. No equation, test result, numerical value or scientific conclusion is amended.

The frozen process is:

$$
q_t=(1-\mu)p_t+\frac{\mu}{2},
\qquad
K_{t+1}\mid K_t\sim\operatorname{Binomial}(N,q_t).
$$

With $H_t=\mathbb E[2p_t(1-p_t)]$, the exact recursion is:

$$
H_{t+1}=aH_t+b,\quad
a=\left(1-\frac1N\right)(1-\mu)^2,\quad
b=\left(1-\frac1N\right)\mu\left(1-\frac{\mu}{2}\right).
$$

The finite-time and positive-innovation stationary solutions are:

$$
H_t=a^tH_0+b\frac{1-a^t}{1-a},
\qquad
H_*=\frac{(1-1/N)\mu(1-\mu/2)}
{1-(1-1/N)(1-\mu)^2}.
$$

For stationary $\mu>0$, integer lag $s\ge0$:

$$
\operatorname{Cov}(p_t,p_{t+s})
=(1-\mu)^s\frac{1-2H_*}{4}.
$$

All formulas are exact for the original R165 artificial two-token binomial process. They are not estimates from human data. The preregistration, original R165 evidence status and freeze constraints remain unchanged.
