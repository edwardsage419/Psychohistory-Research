#!/usr/bin/env python3
"""Synthetic E1: missing and observed zero are different data states."""
from fractions import Fraction

def slope(x, y):
    pairs = [(Fraction(a), Fraction(b)) for a, b in zip(x, y) if b is not None]
    n = len(pairs)
    assert n >= 2
    mx = sum(a for a, _ in pairs) / n
    my = sum(b for _, b in pairs) / n
    return sum((a-mx)*(b-my) for a,b in pairs) / sum((a-mx)**2 for a,_ in pairs)

x = [1,2,3,4]
manual_scale = [1,2,None,None]
quantity_autozero = [1,2,0,0]
assert slope(x, manual_scale) == Fraction(1)
assert slope(x, quantity_autozero) == Fraction(-1,2)
assert sum(v is None for v in manual_scale) == 2
assert all(v is not None for v in quantity_autozero)
assert [v for v in quantity_autozero if v is not None] == quantity_autozero
print({'n_days':4,'observed_scale_days':2,'slope_missing_ignored':str(slope(x,manual_scale)),
       'slope_zero_imputed':str(slope(x,quantity_autozero)), 'assertions':5,'status':'PASS'})
