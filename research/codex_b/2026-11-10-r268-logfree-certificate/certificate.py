"""Independent R268 rational certificates, with no log/exp or archived labels.

Proof scope is the frozen q0=1/5, zero/one model-parameter counts and n=4,6,10.
The exponential series order controls verification precision, never the model.
No original research program imported; all data-generating worlds are artificial.
"""
from fractions import Fraction as F
from math import factorial

SIZES = (4, 6, 10)
PS = (F(1, 5), F(1, 2), F(4, 5))
Q0 = F(1, 5)
METHODS = ("M0_FIXED", "M1_MLE", "AIC_SELECTED", "BIC_SELECTED")


def require(condition, reason):
    if not condition: raise ValueError(reason)


def e2_bounds(order=3):
    """Strict L<exp(2)<U by positive series and geometric upper tail.

    First omitted term is 2^(m+1)/(m+1)!. Each following term ratio is at
    most 2/(m+2), and subsequent ratios decrease strictly. No transcendental
    numerical approximation is used.
    """
    require(type(order) is int and order >= 1, "INVALID_SERIES_ORDER")
    lower = sum((F(2**j, factorial(j)) for j in range(order+1)), F(0))
    omitted = F(2**(order+1), factorial(order+1))
    upper = lower+omitted/(1-F(2, order+2))
    return lower, upper


def likelihood_ratio_squared(n, k):
    require(type(n) is int and n in SIZES and type(k) is int and 0 <= k <= n, "UNFROZEN_STATE")
    q = F(k, n)
    # Fraction's x**0=1 is precisely the frozen boundary likelihood extension.
    ratio = (q**k*(1-q)**(n-k))/(Q0**k*(1-Q0)**(n-k))
    return ratio*ratio


def certify(n, k, order=3):
    r = likelihood_ratio_squared(n, k)
    lower, upper = e2_bounds(order)
    if r < lower:
        aic, margin_a = "M0_FIXED", (lower-r)/lower
    elif r > upper:
        aic, margin_a = "M1_FITTED", (r-upper)/r
    else:
        raise ValueError("UNRESOLVED_AIC_BOUND")
    bic = "M1_FITTED" if r > n else "M0_FIXED"
    margin_b = (r-n)/r if r > n else F(n-r, n)
    # ln(x)>=(x-1)/x gives these exact lower bounds on SCORE separation.
    return {"n": n, "k": k, "likelihood_ratio_squared": r,
            "e2_lower": lower, "e2_upper": upper, "AIC": aic, "BIC": bic,
            "AIC_margin_lower_bound": margin_a, "BIC_margin_lower_bound": margin_b,
            "BIC_exact_tie": r == n}


def count_distribution(p, n):
    require(type(p) is F and p in PS and type(n) is int and n in SIZES, "UNFROZEN_COUNT_WORLD")
    mass = [F(1)]
    for _ in range(n):
        updated = [F(0)]*(len(mass)+1)
        for k, value in enumerate(mass):
            updated[k] += value*(1-p)
            updated[k+1] += value*p
        mass = updated
    require(sum(mass, F(0)) == 1 and len(mass) == n+1, "COUNT_MASS_FAILURE")
    return mass


def world_metrics(p, n):
    mass = count_distribution(p, n)
    selection = {"AIC": F(0), "BIC": F(0), "disagree": F(0)}
    risks = {name: F(0) for name in METHODS}
    for k, weight in enumerate(mass):
        decision = certify(n, k)
        a, b = decision["AIC"], decision["BIC"]
        selection["AIC"] += weight*int(a == "M1_FITTED")
        selection["BIC"] += weight*int(b == "M1_FITTED")
        selection["disagree"] += weight*int(a != b)
        mle = F(k, n)
        forecasts = (Q0, mle, mle if a == "M1_FITTED" else Q0, mle if b == "M1_FITTED" else Q0)
        # Explicitly integrate the two independent future outcomes, not the old
        # binomial script's p*(1-p)+(q-p)^2 implementation.
        for method, q in zip(METHODS, forecasts):
            for y, future_mass in ((0, 1-p), (1, p)):
                risks[method] += weight*future_mass*(q-y)**2
    baseline = p*(1-p)
    return {"selection": selection, "risk": risks,
            "excess": {name: value-baseline for name, value in risks.items()},
            "AIC_minus_BIC": risks["AIC_SELECTED"]-risks["BIC_SELECTED"]}
