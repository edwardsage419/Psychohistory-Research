#!/usr/bin/env python3
"""MKT175 deterministic synthetic probability calibration and temporal leakage tests."""
from fractions import Fraction as F

def brier(y, p):
    if not y or len(y) != len(p):
        raise ValueError("invalid data")
    return sum(((F(t)-F(q))**2 for t,q in zip(y,p)),F(0))/len(y)

def main():
    y=[1,1,0,0]
    weak=[F(51,100),F(51,100),F(49,100),F(49,100)]
    sharp=[F(9,10),F(9,10),F(1,10),F(1,10)]
    for p in (weak,sharp):
        if sum(int((q>=F(1,2))==bool(t)) for t,q in zip(y,p))!=4:
            raise ValueError("accuracy")
    if (brier(y,weak),brier(y,sharp))!=(F(2401,10000),F(1,100)):
        raise ValueError("Brier")
    seq=[0,0,0,0,0,0,1,1,1,1,1,1]
    train,future=seq[:8],seq[8:]
    pre=F(sum(train),len(train))
    leaked=F(sum(seq),len(seq))
    if (pre,leaked,brier(future,[pre]*4),brier(future,[leaked]*4))!=(F(1,4),F(1,2),F(9,16),F(1,4)):
        raise ValueError("temporal leakage example")
    print("PASS MKT175: equal accuracy, unequal Brier; 8/4 time split and hindsight leakage")
if __name__=="__main__":
    main()
