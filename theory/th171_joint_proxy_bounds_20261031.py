"""TH171 exact arithmetic on 3ie 2019 published tables A8 and A9.
Descriptive sample bounds only; no microdata or causal identification.
"""
from fractions import Fraction as F

DATA = {
    "NREGS": ((1724, 1181, 2273), (290, 971, 1080), (0, 0, 1037), (0, 0, 388), 7519),
    "SSP": ((774, 411, 682), (213, 393, 277), (2, 0, 396), (0, 0, 159), 2750),
}

def bounds(triple):
    yes, no, missing = triple
    assert min(triple) >= 0 and sum(triple) > 0
    return F(yes, sum(triple)), F(yes + missing, sum(triple))

def diff(a, b):
    lo_a, hi_a = bounds(a)
    lo_b, hi_b = bounds(b)
    return lo_a - hi_b, hi_a - lo_b

def subtract(a, b):
    out = tuple(x-y for x,y in zip(a,b))
    assert min(out) >= 0
    return out

def run():
    for name, (carded, uncarded, district7, district7_control, total) in DATA.items():
        assert sum(carded) + sum(uncarded) == total
        assert sum(district7) == (1037 if name == "NREGS" else 398)
        assert sum(district7_control) == (388 if name == "NREGS" else 159)
        assert carded[1] > 0 and uncarded[0] > 0
        assert sum(carded) == (5178 if name == "NREGS" else 1867)
        assert sum(uncarded) == (2341 if name == "NREGS" else 883)
        assert carded[2] + uncarded[2] == (3353 if name == "NREGS" else 959)
        assert carded[0] + uncarded[0] == (2014 if name == "NREGS" else 987)
        contrast = diff(carded, uncarded)
        assert contrast[0] < 0 < contrast[1]
        assert contrast == ((F(-1528988,6060849),F(7855357,12121698)) if name == "NREGS" else (F(-231388,1648561),F(887977,1648561)))
        remainder = subtract(carded, district7)
        assert bounds(remainder) == ((F(1724,4141),F(2960,4141)) if name == "NREGS" else (F(772,1469),F(1058,1469)))
        print(name, "cardedGP", bounds(carded), "uncardedGP", bounds(uncarded), "contrast", contrast, "exclude7", bounds(remainder))
    print("PASS: published margins and exact descriptive bounds; no statistical inference")

if __name__ == "__main__":
    run()
