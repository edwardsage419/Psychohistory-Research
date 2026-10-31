"""TH173 exact artificial latent-class audit. Standard library only.
Run: python3 th173_archive_audit.py. No real data or scientific E2/E3 claim.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt
import unittest


def pr(x, p):
    return p if x else 1-p


def prod(xs, rates):
    z = F(1)
    for x, r in zip(xs, rates):
        z *= pr(x, r)
    return z


def joint(p, f, t):
    assert len(f) == len(t) and all(0 <= z <= 1 for z in f+t)
    out = {x: p*prod(x, t)+(1-p)*prod(x, f)
           for x in product((0, 1), repeat=len(f))}
    assert sum(out.values()) == 1
    return out


def mom(d):
    k = len(next(iter(d)))
    m = [sum(v*x[i] for x, v in d.items()) for i in range(k)]
    c = {(i,j):sum(v*(x[i]-m[i])*(x[j]-m[j]) for x,v in d.items())
         for i in range(k) for j in range(i+1,k)}
    h = sum(v*prod_center(x,m) for x,v in d.items()) if k == 3 else None
    return m,c,h


def prod_center(x,m):
    z=F(1)
    for a,b in zip(x,m): z*=a-b
    return z


def root(q):
    a,b=isqrt(q.numerator),isqrt(q.denominator)
    if a*a!=q.numerator or b*b!=q.denominator: raise ValueError('irrational')
    return F(a,b)


def recover(d):
    m,c,h=mom(d)
    a,b,z=c[(0,1)],c[(0,2)],c[(1,2)]
    if min(a,b,z)<=0: raise ValueError('rank deficient')
    r=h*h/(a*b*z)
    s=root(r/(r+4))
    p=(1-s)/2 if h>0 else (1+s)/2 if h<0 else F(1,2)
    v=p*(1-p)
    delta=[root(a*b/(v*z)),root(a*z/(v*b)),root(b*z/(v*a))]
    f=[x-p*y for x,y in zip(m,delta)]
    t=[x+y for x,y in zip(f,delta)]
    assert all(0<=x<y<=1 for x,y in zip(f,t))
    assert joint(p,f,t)==d
    return p,f,t


def rank(mat):
    a=[list(row) for row in mat]; n=len(a); j=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(j,n) if a[i][col]),None)
        if pivot is None: continue
        a[j],a[pivot]=a[pivot],a[j]
        z=a[j][col]; a[j]=[v/z for v in a[j]]
        for i in range(n):
            if i!=j and a[i][col]:
                z=a[i][col]; a[i]=[v-z*w for v,w in zip(a[i],a[j])]
        j+=1
        if j==n: break
    return j


def jac(p,f,t):
    k=len(f); out=[]
    for x in product((0,1),repeat=k):
        row=[prod(x,t)-prod(x,f)]
        for rates,weight in ((f,1-p),(t,p)):
            for i in range(k):
                row.append(weight*(1 if x[i] else -1)*
                           prod(x[:i]+x[i+1:],rates[:i]+rates[i+1:]))
        out.append(row)
    return out


class Audit(unittest.TestCase):
    def setUp(self):
        self.a=joint(F(1,2),[F(1,5),F(1,4)],[F(4,5),F(3,4)])
        self.b=joint(F(1,4),[F(7,20),F(1,3)],[F(19,20),F(1)])
        self.p=F(1,3); self.f=[F(1,5),F(1,4),F(1,10)]
        self.t=[F(4,5),F(3,4),F(9,10)]
        self.d=joint(self.p,self.f,self.t)
    def test01(self): self.assertEqual(self.a,self.b)
    def test02(self): self.assertNotEqual(F(1,2),F(1,4))
    def test03(self): self.assertEqual(mom(self.a)[0],[F(1,2)]*2)
    def test04(self): self.assertEqual(mom(self.a)[1][(0,1)],F(3,40))
    def test05(self):
        self.assertEqual({x+y+z:self.a[x]*self.a[y]*self.a[z] for x,y,z in product(self.a,repeat=3)},
                         {x+y+z:self.b[x]*self.b[y]*self.b[z] for x,y,z in product(self.b,repeat=3)})
    def test06(self): self.assertEqual(len(self.a)**3,64)
    def test07(self):
        m,c,h=mom(self.d)
        self.assertEqual(m,[F(2,5),F(5,12),F(11,30)])
        self.assertEqual(c,{(0,1):F(1,15),(0,2):F(8,75),(1,2):F(4,45)})
        self.assertEqual(h,F(4,225))
    def test08(self): self.assertEqual(recover(self.d),(self.p,self.f,self.t))
    def test09(self): self.assertEqual(sum(self.d.values()),1)
    def test10(self): self.assertEqual(self.d,joint(1-self.p,self.t,self.f))
    def test11(self):
        q0={x:prod(x,self.f) for x in self.d}; q1={x:prod(x,self.t) for x in self.d}
        self.assertEqual(self.d,{x:F(1,3)*q1[x]+F(2,3)*q0[x] for x in self.d})
    def test12(self): self.assertNotEqual(self.p,F(1,2))
    def test13(self):
        q0={x:prod(x,self.f) for x in self.d}; q1={x:prod(x,self.t) for x in self.d}
        pos={x:(q1[x]+q0[x])/2 for x in self.d}
        neg={x:q1[x]/6+q0[x]*F(5,6) for x in self.d}
        self.assertEqual(self.d,{x:(pos[x]+neg[x])/2 for x in self.d})
        for i in range(3):
            self.assertGreater(sum(v*x[i] for x,v in pos.items()),sum(v*x[i] for x,v in neg.items()))
    def test14(self):
        q0={x:prod(x,self.f) for x in self.d}; q1={x:prod(x,self.t) for x in self.d}
        pos={x:(q1[x]+q0[x])/2 for x in self.d}
        self.assertEqual(mom(pos)[1][(0,1)],F(3,40))
    def test15(self):
        p=F(1,4); self.assertEqual(p/(p+(1-p)*F(1,3)),F(1,2))
    def test16(self):
        p=F(1,4); self.assertEqual(p*F(1,3)/(p*F(1,3)+(1-p)*F(1,3)),p)
    def test17(self):
        with self.assertRaises(ValueError):
            recover(joint(F(1,3),[F(1,5),F(1,4),F(1,2)],[F(4,5),F(3,4),F(1,2)]))
    def test18(self): self.assertTrue(all(0<=x<=1 for x in self.a.values()))
    def test19(self): self.assertEqual(rank(jac(F(1,2),[F(1,5),F(1,4)],[F(4,5),F(3,4)])),3)
    def test20(self): self.assertEqual(rank(jac(self.p,self.f,self.t)),7)
    def test21(self):
        self.assertLess(rank(jac(F(1,3),[F(1,5),F(1,4),F(1,2)],[F(4,5),F(3,4),F(1,2)])),7)


if __name__=='__main__': unittest.main(verbosity=2)
