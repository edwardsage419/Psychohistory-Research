#!/usr/bin/env python3
"""MKT115 synthetic reference-point stability and unit sensitivity, stdlib only."""
from math import sqrt, isclose
from itertools import product

POINTS = {'A': (0., 8.), 'B': (40., 4.), 'C': (100., 0.)}
SX, SY = 100., 8.
checks = 0

def check(condition, message):
    global checks
    checks += 1
    assert condition, message

def score(name, ref, sx=SX, sy=SY):
    x, y = POINTS[name]
    return ((x-ref[0])/sx)**2 + ((y-ref[1])/sy)**2

def winners(ref, sx=SX, sy=SY, tol=1e-11):
    vals = {name:score(name,ref,sx,sy) for name in POINTS}
    best = min(vals.values())
    return sorted(name for name,v in vals.items() if abs(v-best)<=tol)

def robustness_radius(ref, winner):
    """Euclidean radius in normalized reference coordinates to nearest rival halfspace."""
    chosen = score(winner,ref)
    radii=[]
    for rival in POINTS:
        if rival == winner: continue
        gap = score(rival,ref)-chosen
        vx=(POINTS[rival][0]-POINTS[winner][0])/SX
        vy=(POINTS[rival][1]-POINTS[winner][1])/SY
        radii.append(gap/(2*sqrt(vx*vx+vy*vy)))
    return min(radii)

# Exact bisectors:
# A=B: y=0.064x+4.72 ; B=C: y=0.096x-4.72 ; A=C: y=0.08x.
for x,y,expected in [(0,8,'A'),(40,4,'B'),(100,0,'C'),(0,0,'B')]:
    check(winners((x,y)) == [expected], f'wrong winner at {x,y}')
for x in [0,20,50,100]:
    check(isclose(score('A',(x,.064*x+4.72)),score('B',(x,.064*x+4.72)),abs_tol=1e-12),'AB bisector')
    check(isclose(score('B',(x,.096*x-4.72)),score('C',(x,.096*x-4.72)),abs_tol=1e-12),'BC bisector')
    check(isclose(score('A',(x,.08*x)),score('C',(x,.08*x)),abs_tol=1e-12),'AC bisector')
check(score('B',(50,4)) < score('A',(50,4)), 'B must win over A=C')
check(isclose(score('A',(50,4)),score('C',(50,4)),abs_tol=1e-12),'A=C at (50,4)')
threshold_AB=sqrt(1600/.75)
threshold_BC=sqrt(8400/.25)
check(isclose(threshold_AB, 46.18802153517, abs_tol=1e-10),'AB threshold')
check(isclose(threshold_BC, 183.30302779823, abs_tol=1e-10),'BC threshold')
for m, expected in [(20,'A'),(46,'A'),(50,'B'),(100,'B'),(180,'B'),(200,'C'),(1000,'C')]:
    check(winners((0,0),sx=m)==[expected],f'scale winner at {m}')
check(set(winners((0,0),sx=threshold_AB))=={'A','B'},'AB tie')
check(set(winners((0,0),sx=threshold_BC))=={'B','C'},'BC tie')
for ref in [(0.,8.),(40.,4.),(100.,0.),(0.,0.)]:
    winner=winners(ref)[0]
    radius=robustness_radius(ref,winner)
    check(radius>0,'positive radius')
    for dx,dy in product((-0.2,0,0.2),repeat=2):
        xx=ref[0]+dx*radius*SX
        yy=ref[1]+dy*radius*SY
        check(winners((xx,yy))==[winner],f'robustness at {ref} perturb {dx,dy}')
def decide(ref,approved,scale_approved):
    if not approved or not scale_approved: return 'ABSTAIN'
    w=winners(ref)
    return w[0] if len(w)==1 else 'TIE_REQUIRES_USER'
check(decide((0,0),False,True)=='ABSTAIN','no preference')
check(decide((0,0),True,False)=='ABSTAIN','no scale approval')
check(decide((0,0),True,True)=='B','approved')
print({'status':'PASS','assertions':checks,'synthetic_only':True,'scale_flip_thresholds':{'A_to_B':threshold_AB,'B_to_C':threshold_BC},'robust_radii':{str(r):robustness_radius(r,winners(r)[0]) for r in [(0.,8.),(40.,4.),(100.,0.),(0.,0.)]}})
