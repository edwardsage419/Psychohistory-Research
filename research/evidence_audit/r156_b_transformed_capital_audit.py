"""Independent R156 curvature replay through square-root capital dynamics."""
from fractions import Fraction as Q
import json
import sys

def audit(receipt):
    n=0; mutant=0; stationary=0
    for row in receipt['rows']:
        k=Q(row['k0']); s=Q(row['s']); d=Q(row['delta'])
        if row['alpha']=='1':
            v=k*(s-d)
            a=k*(s-d)**2
        else:
            x=Q({1:1,4:2,9:3}[row['k0']])
            xp=(s-d*x)/2
            xpp=-d*xp/2
            v=2*x*xp
            a=2*xp*xp+2*x*xpp
            wrong=2*xp*xp
            if d and xp:
                assert wrong!=a
                mutant+=1
        assert v==Q(row['v']) and a==Q(row['a'])
        stationary+=int(v==0)
        n+=1
    assert n==96 and stationary==15 and mutant==30
    return {'compared_rows':n,'exact_mismatches':0,'stationary_worlds':stationary,'concave_omitted_x_second_derivative_mutants_detected':mutant,'method':'independent_square_root_stock_derivative','evidence':'E1_INTERNAL_ONLY'}
if __name__=='__main__':
    with open(sys.argv[1],encoding='utf-8') as f: data=json.load(f)
    print(json.dumps(audit(data),sort_keys=True,indent=2))
