#!/usr/bin/env python3
"""R135 exact symbolic witness validation, optional free SymPy >= 1.13.
Proves persistence of cooperative ESS witness (norm=152,strategy=10)
on assignment-error interval [1/50,2401/8502).
"""
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
import json
from pathlib import Path
import sympy as s

source=spec_from_file_location('bound',str(Path(__file__).with_name('r135_threshold_interval.py')))
c=module_from_spec(source);source.loader.exec_module(c)
a,h=s.symbols('a h', real=True)
ME=s.Rational(1,50)
A0=s.Rational(2401,8502)
AMIN=s.Rational(1,50)
d=c.NORMS[152]
p=c.RESIDENTS[10]

def tbits(z):
    return [a+(1-2*a)*((1-ME)*d[2*j]+ME*d[2*j+1] if bit else d[2*j+1])
            for j,bit in enumerate(z)]

def theta(z,own,other):
    return z[0]*own*other + z[1]*own*(1-other) + z[2]*(1-own)*other + z[3]*(1-own)*(1-other)

t=tbits(p)
resident_poly=s.factor(t[0]*h*h+(t[1]+t[2])*h*(1-h)+t[3]*(1-h)**2-h)
expected_poly=(100*a*h*h-50*h*h-198*a*h+49*h+50*a)/50
if s.simplify(resident_poly-expected_poly)!=0:
    raise ValueError('resident polynomial differs from independent expanded formula')

# All 15 competitor payoff equations. Resultants are exact, but can have
# roots from inadmissible stationary branches; absence of roots is sufficient.
rows=[]
for m in range(16):
    if m==10: continue
    mutant=c.RESIDENTS[m]
    tm=tbits(mutant)
    tg=tm[0]*h+tm[1]*(1-h)
    tb=tm[2]*h+tm[3]*(1-h)
    hm=tb/(1-tg+tb)
    gap=s.cancel(theta(p,h,h)-2*theta(p,h,hm)+theta(mutant,hm,h))
    numerator=s.together(gap).as_numer_denom()[0]
    resultant=s.factor(s.resultant(resident_poly,numerator,h))
    factors=s.factor_list(resultant)[1]
    open_roots=0
    endpoint_roots=0
    for f,mul in factors:
        poly=s.Poly(f,a)
        if poly.degree()==0:continue
        ct=poly.count_roots(AMIN,A0)
        endpoint=int(poly.eval(AMIN)==0)+int(poly.eval(A0)==0)
        open_roots+=int(ct)-endpoint
        endpoint_roots+=int(poly.eval(A0)==0)
    if open_roots!=0:
        raise ValueError(('competitor with intermediate zero',m,open_roots,resultant))
    # Fully rational 24-step bracket at a=.02. Use x derivative bound <=100
    # for b=2,c=1 and min(mu_a)=.02, as documented in the report.
    nd=d
    tm_base=c.source_t(nd,mutant,F(1,50))
    lo,hi=c.hr_bracket(c.source_t(nd,p,F(1,50)),steps=24)
    x=(lo+hi)/2
    tg0=tm_base[0]*x+tm_base[1]*(1-x)
    tb0=tm_base[2]*x+tm_base[3]*(1-x)
    hm0=tb0/(1-tg0+tb0)
    g=c.help_prob(p,x,x)-2*c.help_prob(p,x,hm0)+c.help_prob(mutant,hm0,x)
    lower=g-F(100,2**25)
    if lower<=0:
        raise ValueError(('baseline min gap not certified',m,lower))
    rows.append({'mutant':m,'resultant':str(resultant),
                 'roots_open_1_50_to_a0':int(open_roots),
                 'root_at_a0':bool(endpoint_roots),
                 'lower_payoff_margin_at_a_1_50':str(lower)})

if len(rows)!=15:raise ValueError('15 mutants not analyzed')
exceptional=next(r for r in rows if r['mutant']==0)
if '8502*a - 2401' not in exceptional['resultant']:
    raise ValueError('exact threshold factor missing')
resident_at_a0=s.factor(resident_poly.subs(a,A0))
if s.simplify(resident_at_a0.subs(h,s.Rational(49,74)))!=0:
    raise ValueError('threshold resident Hscore not exact')

# Rational exact boundary margins, supporting strict-ESS definition at equality.
hr=F(49,74)
equal=[]
for m in range(16):
    if m==10: continue
    z=c.RESIDENTS[m]
    tm=c.source_t(d,z,F(2401,8502))
    tg=tm[0]*hr+tm[1]*(1-hr)
    tb=tm[2]*hr+tm[3]*(1-hr)
    hm=tb/(1-tg+tb)
    gap=c.help_prob(p,hr,hr)-2*c.help_prob(p,hr,hm)+c.help_prob(z,hm,hr)
    if gap==0:equal.append(m)
    if gap<0:raise ValueError(('negative gap at threshold unexpectedly',m,gap))
if equal!=[0,2,8]:raise ValueError(('unexpected tie set',equal))

result={
  'source':'Ohtsuki and Iwasa 2004, doi:10.1016/j.jtbi.2004.06.005',
  'evidence':'new same-team mathematical E1; post-freeze sensitivity',
  'resident_norm_id':152,'resident_strategy_id':10,
  'baseline_assignment_error':'1/50',
  'critical_assignment_error':'2401/8502',
  'resident_Hscore_at_boundary':'49/74',
  'resident_exact_polynomial':str(resident_poly),
  'resultant_for_AllD_mutant':exceptional['resultant'],
  'number_mutants_checked':len(rows),
  'number_mutants_with_roots_strictly_between_baseline_and_a0':sum(x['roots_open_1_50_to_a0'] for x in rows),
  'zero_payoff_mutant_ids_at_a0':equal,
  'each_mutant_strictly_rejected_from_a_1_50_to_a0_exclusive':True,
  'mutants':rows
}
with Path(__file__).with_name('R135_THRESHOLD_SYMBOLIC_CERTIFICATE_20261113.json').open('w') as out:
    json.dump(result,out,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!='mutants'},indent=2))
