"""R153: project-constructed 3-zone doubly constrained interactions. E1 only."""
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from itertools import product
import json
getcontext().prec=75
LAYOUTS={'near':(0,1,4),'far':(0,2,6)}
ATTRACTIONS={'flat':(1,1,1),'column_bonus':(1,2,3)}
MARGINS={'m0':((10,20,30),(15,25,20)),'m1':((20,20,20),(10,30,20))}
EXPONENTS=(0,1,2)
MAX_ITERATIONS=450
RESIDUAL_TOL=D('1e-25')
METHOD_TOL=D('1e-24')
ROUND28=D('1e-28')

def vector(v,n=3,positive=True):
    if not isinstance(v,(tuple,list)) or len(v)!=n: raise ValueError('wrong vector length')
    if any(type(x) is not int for x in v): raise TypeError('integers only; bool and float rejected')
    if any((x<=0 if positive else x<0) for x in v): raise ValueError('nonpositive or negative argument')
    return tuple(v)

def validate_margins(r,c):
    r,c=vector(r),vector(c)
    if sum(r)!=sum(c): raise ValueError('margins disagree')
    return r,c

def kernel(layout,alpha,attraction):
    if layout not in LAYOUTS or attraction not in ATTRACTIONS: raise ValueError('unknown named setting')
    if type(alpha) is not int: raise TypeError('alpha integer')
    if alpha not in EXPONENTS: raise ValueError('unknown distance exponent')
    x=vector(LAYOUTS[layout],positive=False)
    if len(set(x))!=3: raise ValueError('duplicate geographic locations')
    a=vector(ATTRACTIONS[attraction])
    return tuple(tuple(D(a[j])/D((1+abs(x[i]-x[j]))**alpha) for j in range(3)) for i in range(3))

def positive_kernel(k):
    if not isinstance(k,(tuple,list)) or len(k)!=3 or any(not isinstance(row,(tuple,list)) or len(row)!=3 for row in k): raise ValueError('strictly positive 3x3 kernel required')
    out=[]
    for row in k:
        vals=[]
        for v in row:
            if type(v) is not D: raise TypeError('Decimal kernel entries required')
            if not v.is_finite() or v<=0: raise ValueError('strictly positive finite kernel required')
            vals.append(v)
        out.append(tuple(vals))
    return tuple(out)

def residual(t,r,c):
    row=[sum(t[i],D(0)) for i in range(3)]
    col=[sum((t[i][j] for i in range(3)),D(0)) for j in range(3)]
    return max([abs(row[i]-D(r[i])) for i in range(3)]+[abs(col[j]-D(c[j])) for j in range(3)])

def ipf_matrix_direct(k,r,c):
    k=positive_kernel(k);r,c=validate_margins(r,c)
    t=[list(row) for row in k]
    for iteration in range(1,MAX_ITERATIONS+1):
        for i in range(3):
            total=sum(t[i],D(0))
            t[i]=[v*D(r[i])/total for v in t[i]]
        for j in range(3):
            total=sum((t[i][j] for i in range(3)),D(0))
            for i in range(3): t[i][j]*=D(c[j])/total
        err=residual(t,r,c)
        if err<=RESIDUAL_TOL: return tuple(tuple(row) for row in t),iteration,err
    raise ArithmeticError('direct IPF did not meet prescored tolerance')

def ipf_independent_scalers(k,r,c):
    k=positive_kernel(k);r,c=validate_margins(r,c)
    v=[D(1)]*3
    for iteration in range(1,MAX_ITERATIONS+1):
        u=[D(r[i])/sum((k[i][j]*v[j] for j in range(3)),D(0)) for i in range(3)]
        v=[D(c[j])/sum((u[i]*k[i][j] for i in range(3)),D(0)) for j in range(3)]
        t=tuple(tuple(u[i]*k[i][j]*v[j] for j in range(3)) for i in range(3))
        err=residual(t,r,c)
        if err<=RESIDUAL_TOL: return t,iteration,err
    raise ArithmeticError('independent scaling did not meet prescored tolerance')

def origin_only(k,r):
    k=positive_kernel(k);r=vector(r)
    return tuple(tuple(D(r[i])*k[i][j]/sum(k[i],D(0)) for j in range(3)) for i in range(3))

def cross_ratio(t,i,j,p,q): return t[i][p]*t[j][q]/(t[i][q]*t[j][p])

def hall_feasible(support,r,c):
    if not isinstance(support,(tuple,list)) or len(support) not in (2,3): raise ValueError('2x2 or 3x3 support needed')
    n=len(support)
    if any(not isinstance(row,(tuple,list)) or len(row)!=n for row in support): raise ValueError('square support required')
    r,c=vector(r,n),vector(c,n)
    if sum(r)!=sum(c): raise ValueError('mismatched flow totals')
    for row in support:
        for v in row:
            if type(v) is not int: raise TypeError('support counts must be integer')
            if v<0: raise ValueError('negative support')
    for mask in range(1,1<<n):
        rows=[i for i in range(n) if (mask>>i)&1]
        neighbors={j for i in rows for j in range(n) if support[i][j]>0}
        if sum(r[i] for i in rows)>sum(c[j] for j in neighbors): return False
    return True

def exact_two_by_two_witness():
    k=((F(3),F(1)),(F(1),F(1)))
    t=((F(3,2),F(1,2)),(F(3,2),F(3,2)))
    assert tuple(map(sum,t))==(2,3)
    assert tuple(sum(t[i][j] for i in range(2)) for j in range(2))==(3,2)
    assert cross_ratio(t,0,1,0,1)==cross_ratio(k,0,1,0,1)==3
    return {'kernel':[[str(x) for x in row] for row in k],
            'balanced':[[str(x) for x in row] for row in t],
            'cross_product_ratio':'3'}

def spec_cases():
    for layout,alpha,attr,margin in product(LAYOUTS,EXPONENTS,ATTRACTIONS,MARGINS):
        yield layout,alpha,attr,margin

def as28(t): return format(t.quantize(ROUND28),'f')

def run_case(layout,alpha,attr,margin):
    if margin not in MARGINS: raise ValueError('unknown margin scheme')
    r,c=MARGINS[margin]
    k=kernel(layout,alpha,attr)
    t,it,err=ipf_matrix_direct(k,r,c)
    u,it2,err2=ipf_independent_scalers(k,r,c)
    diff=max(abs(t[i][j]-u[i][j]) for i in range(3) for j in range(3))
    assert diff<=METHOD_TOL
    off=origin_only(k,r)
    offcols=tuple(sum((off[i][j] for i in range(3)),D(0)) for j in range(3))
    margin_gap=sum((abs(offcols[j]-D(c[j])) for j in range(3)),D(0))
    difference=sum((abs(t[i][j]-off[i][j]) for i in range(3) for j in range(3)),D(0))
    return {'layout':layout,'exponent':alpha,'attraction':attr,'margin':margin,
        'origin_budgets':list(r),'destination_budgets':list(c),
        'balanced_flow_28dp':[[as28(x) for x in row] for row in t],
        'origin_only_flow_28dp':[[as28(x) for x in row] for row in off],
        'origin_only_destination_gap_28dp':as28(margin_gap),
        'rerouting_L1_gap_28dp':as28(difference),
        'direct_iterations':it,'independent_scaler_iterations':it2,
        'direct_max_balance_residual':str(err),
        'independent_max_balance_residual':str(err2),
        'max_algorithm_disagreement':str(diff),
        'two_implementations_agree_to_frozen_tolerance':True}

def output():
    cases=[run_case(*sp) for sp in spec_cases()]
    assert len(cases)==24
    invariant=True
    for layout in LAYOUTS:
        for alpha in EXPONENTS:
            for margin in MARGINS:
                a=run_case(layout,alpha,'flat',margin)
                b=run_case(layout,alpha,'column_bonus',margin)
                aa=a['balanced_flow_28dp'];bb=b['balanced_flow_28dp']
                if not all(abs(D(aa[i][j])-D(bb[i][j]))<=METHOD_TOL for i in range(3) for j in range(3)): invariant=False
    assert invariant
    return {'research_id':'R153','model':'project synthetic double-constrained spatial flows',
        'original_author_historical_data_reproduced':False,
        'source_Wilson1971_full_pdf_visually_read':False,
        'source_SinkhornKnopp1967_print_pages_visually_read':[343,344],
        'new_E2':0,'new_E3':0,'scenarios_count':24,
        'decimal_precision':getcontext().prec,'residual_tolerance':str(RESIDUAL_TOL),
        'agreement_tolerance':str(METHOD_TOL),
        'all_column_multiplier_effects_absorbed_by_destination_constraint':invariant,
        'exact_2x2_rational_witness':exact_two_by_two_witness(),
        'structural_zeros_equal_margins_feasible':hall_feasible(((1,0),(0,1)),(1,1),(1,1)),
        'structural_zeros_mismatched_margins_infeasible':not hall_feasible(((1,0),(0,1)),(2,1),(1,2)),
        'scenarios':cases}

def canonical_json(): return json.dumps(output(),sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n'

if __name__=='__main__': print(canonical_json(),end='')
