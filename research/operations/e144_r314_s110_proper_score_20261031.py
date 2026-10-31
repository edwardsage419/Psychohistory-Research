#!/usr/bin/env python3
"""E144 independent exact Bayes Brier under observation coarsening, E1 only."""
from collections import defaultdict
from fractions import Fraction as F

SEEDS={'P3':(1,2,1),'K3':(2,2,2),'S4':(3,1,1,1)}
EXPECTED={
 'P3':(F(1,6),F(67,288),F(67,288)),
 'K3':(F(1,8),F(29,120),F(27,110)),
 'S4':(F(23,80),F(5879,26928),F(2321,10512)),
}
def distribution(degrees,coarse):
 n=len(degrees)
 groups=defaultdict(lambda:[F(0),F(0)])
 for i in range(n):
  updated=list(degrees)+[1]
  updated[i]+=1
  for j in range(n+1):
   final=updated+[1]
   final[j]+=1
   key=max(final) if coarse else (i,j)
   p=F(degrees[i],sum(degrees))*F(updated[j],sum(updated))
   q=F(1,n*(n+1))
   groups[key][0]+=p
   groups[key][1]+=q
 for idx in (0,1):
  if sum((v[idx] for v in groups.values()),F(0))!=1:
   raise ValueError("probability mass")
 return groups
def score(groups):
 tv=sum((abs(p-q) for p,q in groups.values()),F(0))/2
 brier=sum((p*q/(2*(p+q)) for p,q in groups.values()),F(0))
 return tv,brier
def main():
 total=0
 for seed,degrees in SEEDS.items():
  full=distribution(degrees,False)
  maximum=distribution(degrees,True)
  tv,b0=score(full)
  tv3,b3=score(maximum)
  if (tv,b0,b3)!=EXPECTED[seed] or tv!=tv3 or b0>b3:
   raise ValueError("wrong proper-score result")
  total+=len(full)
  print(seed,"paths",len(full),"TV",tv,"full_Brier",b0,"max_Brier",b3,"extra",b3-b0)
 if total!=44 or EXPECTED['K3'][2]-EXPECTED['K3'][1]!=F(1,264) or EXPECTED['S4'][2]-EXPECTED['S4'][1]!=F(135,54604):
  raise ValueError("universe or loss difference")
 print("PASS E144: 44 paths, 3 seeds, exact TV and Brier")
if __name__=="__main__":
 main()
