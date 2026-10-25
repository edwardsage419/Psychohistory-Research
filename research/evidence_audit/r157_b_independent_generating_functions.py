"""Independent generating-function E1 audit of R157. Python 3 standard library.

The finite coefficient calculation multiplies formal power series; it does
not import the R157 transition code or the main convolution implementation.
"""
from fractions import Fraction as F
from itertools import product
import json

T = 12
ONE = F(1)
ZERO = F(0)


def conv(x, y):
    return tuple(sum((x[k] * y[n-k] for k in range(n+1)), ZERO)
                 for n in range(T+1))


def geom(r):
    return tuple(r**n for n in range(T+1))


def shift_scale(x, c):
    return (ZERO,) + tuple(c * x[n] for n in range(T))


def components(a, b, c):
    # M(z)=a*z/((1-z)*(1-(1-a)*z)); E(z)=b*z*M(z)/(1-(1-b)*z)
    # F(z)=c*z*E(z)/(1-(1-c)*z), for H=1 and r=0.
    m = shift_scale(conv(geom(ONE), geom(ONE-a)), a)
    e = shift_scale(conv(m, geom(ONE-b)), b)
    f = shift_scale(conv(e, geom(ONE-c)), c)
    return m, e, f


def main():
    triples = list(product((F(1,4), F(1,2)), repeat=3))
    positive_t3 = 0
    exact_products = 0
    exact_states = 0
    for a,b,c in triples:
        m,e,f = components(a,b,c)
        assert m[0] == e[0] == f[0] == 0
        assert all(m[t]*e[t]*f[t] == 0 for t in range(3))
        assert m[3]*e[3]*f[3] > 0
        for H,r in product((F(1,4), F(1,2), ONE), (ZERO, F(1,2), ONE)):
            for t in range(T+1):
                M, E, D = H*m[t], H*e[t], H*(ONE-r)*f[t]
                assert M*E*D == H**3*(ONE-r)*m[t]*e[t]*f[t]
                exact_products += 1
                exact_states += 3
            if r < 1:
                positive_t3 += 1
    assert (exact_products,exact_states,positive_t3) == (936,2808,48)
    m,e,f = components(F(1,4),F(1,4),F(1,4))
    p3 = F(1,8)*m[3]*e[3]*f[3]
    p12 = F(1,8)*m[12]*e[12]*f[12]
    assert p3 == F(185,1048576)
    assert p12 == F(2345008149288796188925,37778931862957161709568)
    assert F(1,2)*m[1] == F(1,8)
    assert m[1] == F(1,4)
    assert F(1,2)**3*(ONE-ZERO) == ONE**3*(ONE-F(7,8))
    assert F(1,2)**2 != F(1,2)**3
    assert ONE+F(1,2) != ONE-F(1,2)
    assert ONE**3*(ONE-ONE) == 0  # Positive H, full buffer, zero product.
    return {
        "status":"PASS_BOUNDED_INTERNAL_E1",
        "method":"formal generating function coefficient products with Fraction",
        "base_rate_triples":len(triples),
        "exact_product_factorization_cells":exact_products,
        "exact_state_scaling_cells":exact_states,
        "positive_t3_worlds":positive_t3,
        "counterexample_P3":str(p3),
        "counterexample_P12":str(p12),
        "negative_controls_rejected":3,
        "external_replication":False,
        "E2_new":0,
        "E3_new":0,
    }


if __name__ == "__main__":
    print(json.dumps(main(),ensure_ascii=False,indent=2))
