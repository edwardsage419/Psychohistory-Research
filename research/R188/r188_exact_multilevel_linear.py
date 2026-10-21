"""R188 exact hierarchical linear decomposition, 180 complete artificial worlds.

Groups are identified explicitly: six groups of eight individuals each. The
independent pooled/group-within/between/contextual and fixed quasi-demeaning
estimators are all rational; no variance components are estimated. This is an
E1 structural algebra audit, not an applied random-intercept model fit.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R188_MULTILEVEL_180_WORLDS_8640_ROWS_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R188_EXACT_RESULTS.json"
RAW=HERE/"R188_ALL_8640_HIERARCHICAL_ARTIFICIAL_ROWS.csv"
ACCEPT=HERE/"R188_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R188_180_Exact_Multilevel_Linear_Worlds.zip"

N_GROUPS=6
N_PER_GROUP=8
DESIGNS=(
    ("BALANCED",(4,4,4,4,4,4)),
    ("WEAK_BETWEEN",(2,2,4,4,6,6)),
    ("STRONG_BETWEEN",(2,2,2,6,6,6)),
)
A_VALUES=(F(0),F(1))
WITHIN_B_VALUES=(F(1,4),F(1,2))
CONTEXT_C_VALUES=(F(-4),F(-2),F(0),F(2),F(4))
E_VALUES=(F(0),F(1,4),F(1,2))
THETAS=(F(0),F(1,2),F(3,4),F(1))


def worlds():
    for (name,k),a,b,c,e in product(DESIGNS,A_VALUES,WITHIN_B_VALUES,CONTEXT_C_VALUES,E_VALUES):
        yield name,k,a,b,c,e


def average(vals):
    vals=list(vals)
    if not vals:
        raise ValueError("empty mean source")
    return sum(vals,F(0))/len(vals)


def generate(name,exposures,a,b,c,e):
    if name not in dict(DESIGNS) or dict(DESIGNS)[name]!=exposures:
        raise ValueError("outside fixed six-group exposure design")
    if a not in A_VALUES or b not in WITHIN_B_VALUES or c not in CONTEXT_C_VALUES or e not in E_VALUES:
        raise ValueError("source parameters outside preregistered grid")
    rows=[]
    for group,k in enumerate(exposures):
        if not (0<k<N_PER_GROUP and k%2==0 and (N_PER_GROUP-k)%2==0):
            raise ValueError("each group needs positive even within-cell counts")
        bar=F(k,N_PER_GROUP)
        for x,size in ((0,N_PER_GROUP-k),(1,k)):
            for j in range(size):
                eps=e if j<size//2 else -e
                y=a+b*x+c*bar+eps
                rows.append({
                    "group":group,"x":F(x),"xbar":bar,
                    "y":y,"epsilon":eps,
                    "within_exposure_cell":j,
                    "group_intercept_alias_u":c*bar,
                })
    if len(rows)!=N_GROUPS*N_PER_GROUP:
        raise AssertionError("source hierarchy row count unexpected")
    return rows


def group_means(rows):
    out={}
    for g in range(N_GROUPS):
        subset=[r for r in rows if r["group"]==g]
        if len(subset)!=N_PER_GROUP:
            raise ValueError("incomplete original group")
        mx=average(r["x"] for r in subset)
        my=average(r["y"] for r in subset)
        out[g]=(mx,my)
    return out


def solve(matrix,right):
    n=len(right)
    if n not in (2,3) or len(matrix)!=n or any(len(row)!=n for row in matrix):
        raise ValueError("wrong model matrix")
    aug=[[F(v) for v in row]+[F(right[i])] for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if aug[i][j]!=0),None)
        if pivot is None:
            raise ValueError("rank-deficient normal equations")
        aug[j],aug[pivot]=aug[pivot],aug[j]
        scale=aug[j][j]
        aug[j]=[v/scale for v in aug[j]]
        for i in range(n):
            if i==j:continue
            d=aug[i][j]
            aug[i]=[v-d*w for v,w in zip(aug[i],aug[j])]
    return tuple(a[-1] for a in aug)


def direct_normal_equation(rows,fields):
    cols=[lambda row:F(1)]+[lambda row,name=field:row[name] for field in fields]
    matrix=[[sum((p(r)*q(r) for r in rows),F(0)) for q in cols] for p in cols]
    right=[sum((p(r)*r["y"] for r in rows),F(0)) for p in cols]
    return solve(matrix,right)


def pooled_two_paths(rows):
    left=average(r["y"] for r in rows if r["x"]==0)
    right=average(r["y"] for r in rows if r["x"]==1)
    from_group_means=(left,right-left)
    normal=direct_normal_equation(rows,("x",))
    if from_group_means!=normal:
        raise AssertionError("pooled conditional means and normal equations differ")
    return normal


def within_two_paths(rows):
    groupbar=group_means(rows)
    centered_num=F(0)
    centered_den=F(0)
    alt_num=F(0)
    alt_den=F(0)
    group_slopes=[]
    for g in range(N_GROUPS):
        part=[r for r in rows if r["group"]==g]
        mx,my=groupbar[g]
        centered_num+=sum(((r["x"]-mx)*(r["y"]-my) for r in part),F(0))
        centered_den+=sum(((r["x"]-mx)**2 for r in part),F(0))
        one=average(r["y"] for r in part if r["x"]==1)
        zero=average(r["y"] for r in part if r["x"]==0)
        k=int(mx*N_PER_GROUP)
        w=F(k*(N_PER_GROUP-k),N_PER_GROUP)
        alt_num+=w*(one-zero)
        alt_den+=w
        group_slopes.append(one-zero)
    if centered_den<=0 or centered_den!=alt_den:
        raise AssertionError("invalid group within variation")
    beta=centered_num/centered_den
    if beta!=alt_num/alt_den or any(v!=beta for v in group_slopes):
        raise AssertionError("independent within FE and within subgroup mean slopes differ")
    return beta,groupbar


def between_two_paths(groupbar):
    gx=[groupbar[g][0] for g in range(N_GROUPS)]
    gy=[groupbar[g][1] for g in range(N_GROUPS)]
    xmean=average(gx);ymean=average(gy)
    den=sum(((x-xmean)**2 for x in gx),F(0))
    if den==0:
        try:
            solve([[F(N_GROUPS),sum(gx,F(0))],
                   [sum(gx,F(0)),sum((x*x for x in gx),F(0))]],
                  [sum(gy,F(0)),sum((x*y for x,y in zip(gx,gy)),F(0))])
        except ValueError:
            return None
        raise AssertionError("constant cluster covariate should be rank deficient")
    slope=sum(((x-xmean)*(y-ymean) for x,y in zip(gx,gy)),F(0))/den
    constant=ymean-slope*xmean
    normal=solve([[F(N_GROUPS),sum(gx,F(0))],
                  [sum(gx,F(0)),sum((x*x for x in gx),F(0))]],
                 [sum(gy,F(0)),sum((x*y for x,y in zip(gx,gy)),F(0))])
    if (constant,slope)!=normal:
        raise AssertionError("between covariance regression and normal equations differ")
    return normal


def analytic_within_between_variance(exposures):
    shares=[F(k,N_PER_GROUP) for k in exposures]
    mx=average(shares)
    vb=average((x-mx)**2 for x in shares)
    vw=average(x*(1-x) for x in shares)
    if vw<=0 or vw+vb!=mx*(1-mx):
        raise AssertionError("binary exposure total-variance decomposition invalid")
    return vb,vw


def quasi_demeaning_two_paths(rows,theta,a,b,c,exposures,groupbar):
    if theta not in THETAS:
        raise ValueError("unregistered quasi-demeaning")
    x=[r["x"]-theta*groupbar[r["group"]][0] for r in rows]
    y=[r["y"]-theta*groupbar[r["group"]][1] for r in rows]
    if theta==1:
        numerator=sum((v*w for v,w in zip(x,y)),F(0))
        denominator=sum((v*v for v in x),F(0))
        if denominator<=0:
            raise AssertionError("within FE denominator zero")
        direct=numerator/denominator
    else:
        mx,my=average(x),average(y)
        direct=sum(((v-mx)*(w-my) for v,w in zip(x,y)),F(0))/sum(((v-mx)**2 for v in x),F(0))
    vb,vw=analytic_within_between_variance(exposures)
    scale=(1-theta)**2
    independent_formula=b+c*scale*vb/(vw+scale*vb)
    if direct!=independent_formula:
        raise AssertionError("direct quasi demeaned OLS and independent within-between identity differ")
    return direct


def adjusted_contextual(rows,a,b,c,groupbar,within_beta,between):
    if between is None:
        with_expected_error=False
        try:
            direct_normal_equation(rows,("x","xbar"))
        except ValueError:
            with_expected_error=True
        if not with_expected_error:
            raise AssertionError("balanced contextual xbar must be rank deficient")
        return None
    full=direct_normal_equation(rows,("x","xbar"))
    # Second fully independent path from between and FE identities.
    ib=between[1]-within_beta
    ia=average(r["y"] for r in rows)-within_beta*average(r["x"] for r in rows)-ib*average(r["xbar"] for r in rows)
    if full!=(a,b,c) or full!=(ia,within_beta,ib):
        raise AssertionError("direct contextual OLS and between/within independent estimate differ")
    return full


def verify_hierarchical_alias(rows,a,b,c,e):
    """Latent context c*xbar and arbitrary group-intercept u yield identical y."""
    for r in rows:
        predicted=a+b*r["x"]+r["group_intercept_alias_u"]+r["epsilon"]
        if predicted!=r["y"] or r["group_intercept_alias_u"]!=c*r["xbar"]:
            raise AssertionError("group intercept representation does not match contextual model")


def evaluate_world(name,exposures,a,b,c,e,original_rows):
    rows=generate(name,exposures,a,b,c,e)
    verify_hierarchical_alias(rows,a,b,c,e)
    pooled=pooled_two_paths(rows)
    within,bar=within_two_paths(rows)
    between=between_two_paths(bar)
    context=adjusted_contextual(rows,a,b,c,bar,within,between)
    vb,vw=analytic_within_between_variance(exposures)
    if within!=b or pooled[1]!=b+c*vb/(vw+vb):
        raise AssertionError("true within or pooled omitted context coefficient wrong")
    if between is not None and between[1]!=b+c:
        raise AssertionError("true between group slope does not equal b+c")
    residual=[r["y"]-(a+b*r["x"]+c*r["xbar"]) for r in rows]
    if sum((v*v for v in residual),F(0))!=len(rows)*e*e:
        raise AssertionError("full source residual SSE wrong")
    if sum(residual,F(0))!=0 or sum((r["x"]*v for r,v in zip(rows,residual)),F(0))!=0:
        raise AssertionError("original source residual x orthogonality wrong")
    for g in range(N_GROUPS):
        if sum((residual[i] for i,r in enumerate(rows) if r["group"]==g),F(0))!=0:
            raise AssertionError("original source error not orthogonal to group intercept")
    slopes={str(theta):quasi_demeaning_two_paths(rows,theta,a,b,c,exposures,bar) for theta in THETAS}
    if slopes["0"]!=pooled[1] or slopes["1"]!=within:
        raise AssertionError("pooled and FE endpoints of quasi-demeaning failed")
    if name=="BALANCED" and (between is not None or context is not None or any(value!=b for value in slopes.values())):
        raise AssertionError("all-between-equal negative control failed")
    index=len(original_rows)//(N_GROUPS*N_PER_GROUP)
    for r in rows:
        original_rows.append({
            "world_index":index,"design":name,
            "group_id":r["group"],
            "x":str(r["x"]),"xbar_group":str(r["xbar"]),
            "observed_y":str(r["y"]),"original_cell_error":str(r["epsilon"]),
            "true_a":str(a),"true_within_b":str(b),"true_context_c":str(c),
            "alternative_unrestricted_group_intercept":str(r["group_intercept_alias_u"]),
        })
    return {
        "design":name,"group_exposure_count_k":[int(v) for v in exposures],
        "original_rows":len(rows),"groups":N_GROUPS,"rows_per_group":N_PER_GROUP,
        "true_a":str(a),"true_within_b":str(b),"true_context_c":str(c),
        "original_error_magnitude":str(e),
        "V_between_binary_exposure":str(vb),
        "V_within_binary_exposure":str(vw),
        "pooled_intercept":str(pooled[0]),
        "pooled_x_slope":str(pooled[1]),
        "within_FE_x_slope":str(within),
        "between_xbar_slope":str(between[1]) if between is not None else "UNIDENTIFIED_NO_BETWEEN_VARIATION",
        "contextual_adjusted_a_b_c":[str(v) for v in context] if context is not None else "UNIDENTIFIED_NO_BETWEEN_VARIATION",
        "quasi_demeaning_theta_to_slope":{key:str(v) for key,v in slopes.items()},
        "pooled_negative_with_true_positive_within":pooled[1]<0,
        "residual_SSE_exact":str(len(rows)*e*e),
        "unrestricted_group_intercept_and_contextual_observational_alias":True,
        "independent_direct_OLS_and_within_between_identity_valid":True,
    }


def run():
    world_rows=[]
    original=[]
    for params in worlds():
        world_rows.append(evaluate_world(*params,original))
    if len(world_rows)!=180 or len(original)!=8640:
        raise AssertionError("frozen full 180-world hierarchy universe changed")
    anchors=[v for v in world_rows if v["design"]=="STRONG_BETWEEN"
             and v["true_a"]=="0" and v["true_within_b"]=="1/4"
             and v["true_context_c"]=="-4" and v["original_error_magnitude"]=="1/4"]
    if len(anchors)!=1:
        raise AssertionError("locked confounded source missing")
    t=anchors[0]
    if not (t["pooled_x_slope"]=="-3/4" and t["within_FE_x_slope"]=="1/4"
            and t["between_xbar_slope"]=="-15/4"
            and t["quasi_demeaning_theta_to_slope"]==
            {"0":"-3/4","1/2":"-3/52","3/4":"33/196","1":"1/4"}):
        raise AssertionError("prescored within-between sign reversal and sensitivity failed")
    with RAW.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(original[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(original)
    neg=sum(int(w["pooled_negative_with_true_positive_within"]) for w in world_rows)
    out={
        "research_id":"R188",
        "stage":"E1_ARTIFICIAL_EXACT_MULTILEVEL_LINEAR_WITHIN_BETWEEN",
        "world_count":180,"original_artificial_rows":8640,
        "actual_group_count_each_world":N_GROUPS,
        "within_group_rows_each_world":N_PER_GROUP,
        "quasi_demeaning_theta":[str(x) for x in THETAS],
        "direct_quasi_demeaning_sensitivity_fits":180*len(THETAS),
        "pooled_negative_within_true_positive_worlds":neg,
        "fixed_strong_confounded_intercept_alias":t,
        "all_fe_and_groupmeans_independent_fraction_routes_equal":True,
        "all_contextual_and_group_intercept_equivalence":True,
        "all_singular_between_negative_controls_correct":True,
        "all_original_data_rows_sha256":sha256(RAW.read_bytes()).hexdigest(),
        "all_worlds":world_rows,
        "real_human_or_history_sample":False,
        "new_E2":0,"new_E3":0,
    }
    RESULT.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    a={
        "research_id":"R188",
        "state":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MULTILEVEL_LINEAR",
        "worlds":180,"raw_artificial_rows":8640,"hierarchical_slope_sensitivity_fits":720,
        "pooled_and_group_fixed_effect_two_exact_routes":True,
        "between_and_contextual_singular_inputs_fail_closed":True,
        "quasi_demeaning_closed_analytic_identity_exact":True,
        "strong_between_pooled_sign_reversal_but_FE_positive":True,
        "unrestricted_group_effect_contextual_alias_verified":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "original_rows_sha256":out["all_original_data_rows_sha256"],
        "new_E2":0,"new_E3":0,"human_or_historical_data":False,
    }
    ACCEPT.write_text(json.dumps(a,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R188_MACHINE_ACCEPTANCE",json.dumps(a,sort_keys=True))
    print("R188_PRIMARY_MULTILEVEL_SIGN_REVERSAL",json.dumps(t,sort_keys=True))
    return out


def archive():
    files=[Path(__file__).name,RESULT.name,RAW.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in files:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R188_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestMultilevelExact(unittest.TestCase):
    def test_full_180_worlds(self):
        self.assertEqual(len(list(worlds())),180)
    def test_8640_original_rows(self):
        self.assertEqual(sum(N_GROUPS*N_PER_GROUP for _ in worlds()),8640)
    def test_group_count_six(self):
        self.assertEqual(N_GROUPS,6)
    def test_group_size_eight(self):
        self.assertEqual(N_PER_GROUP,8)
    def test_four_quasi_demeaning_levels(self):
        self.assertEqual(THETAS,(F(0),F(1,2),F(3,4),F(1)))
    def test_all_group_cell_exposures_even(self):
        for name,counts in DESIGNS:
            self.assertTrue(all(k%2==0 and 0<k<N_PER_GROUP for k in counts))
    def test_original_group_within_balanced_errors(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            for g in range(N_GROUPS):
                for x in (0,1):
                    cell=[r["epsilon"] for r in rows if r["group"]==g and r["x"]==x]
                    self.assertEqual(sum(cell,F(0)),0)
    def test_pooled_two_algorithms_all_worlds(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            self.assertEqual(pooled_two_paths(rows),direct_normal_equation(rows,("x",)))
    def test_within_two_algorithms_all_worlds(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            self.assertEqual(within_two_paths(rows)[0],b)
    def test_between_true_slope_for_separated_designs(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            between=between_two_paths(group_means(rows))
            if name=="BALANCED":
                self.assertIsNone(between)
            else:
                self.assertEqual(between[1],b+c)
    def test_contextual_full_OLS_recovery_nonconstant(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            if name=="BALANCED":
                with self.assertRaises(ValueError):
                    direct_normal_equation(rows,("x","xbar"))
            else:
                self.assertEqual(direct_normal_equation(rows,("x","xbar")),(a,b,c))
    def test_between_and_within_variance_decomposition(self):
        for name,counts in DESIGNS:
            vb,vw=analytic_within_between_variance(counts)
            self.assertEqual(vb+vw,F(1,4))
    def test_strong_between_variance(self):
        self.assertEqual(analytic_within_between_variance(DESIGNS[2][1]),(F(1,16),F(3,16)))
    def test_balanced_between_variance_zero(self):
        self.assertEqual(analytic_within_between_variance(DESIGNS[0][1])[0],0)
    def test_weak_between_variance(self):
        self.assertEqual(analytic_within_between_variance(DESIGNS[1][1])[0],F(1,24))
    def test_all_theta_direct_vs_independent_analytic(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            gm=group_means(rows)
            for theta in THETAS:
                quasi_demeaning_two_paths(rows,theta,a,b,c,counts,gm)
    def test_original_source_hierarchical_context_alias(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            verify_hierarchical_alias(rows,a,b,c,e)
    def test_primary_sign_reversal_pooled(self):
        args=("STRONG_BETWEEN",DESIGNS[2][1],F(0),F(1,4),F(-4),F(1,4))
        rows=generate(*args)
        self.assertEqual(pooled_two_paths(rows)[1],F(-3,4))
        self.assertEqual(within_two_paths(rows)[0],F(1,4))
    def test_primary_theta_half(self):
        args=("STRONG_BETWEEN",DESIGNS[2][1],F(0),F(1,4),F(-4),F(1,4))
        rows=generate(*args)
        self.assertEqual(quasi_demeaning_two_paths(rows,F(1,2),*args[2:5],args[1],group_means(rows)),F(-3,52))
    def test_primary_theta_three_quarters(self):
        args=("STRONG_BETWEEN",DESIGNS[2][1],F(0),F(1,4),F(-4),F(1,4))
        rows=generate(*args)
        self.assertEqual(quasi_demeaning_two_paths(rows,F(3,4),*args[2:5],args[1],group_means(rows)),F(33,196))
    def test_primary_between_slope(self):
        rows=generate("STRONG_BETWEEN",DESIGNS[2][1],F(0),F(1,4),F(-4),F(0))
        self.assertEqual(between_two_paths(group_means(rows))[1],F(-15,4))
    def test_all_balanced_quasi_slope_equals_within(self):
        for a,b,c,e in product(A_VALUES,WITHIN_B_VALUES,CONTEXT_C_VALUES,E_VALUES):
            rows=generate("BALANCED",DESIGNS[0][1],a,b,c,e)
            for theta in THETAS:
                self.assertEqual(quasi_demeaning_two_paths(rows,theta,a,b,c,DESIGNS[0][1],group_means(rows)),b)
    def test_zero_context_no_bias_all(self):
        for name,counts in DESIGNS:
            rows=generate(name,counts,F(0),F(1,4),F(0),F(1,2))
            self.assertEqual(pooled_two_paths(rows)[1],F(1,4))
    def test_group_source_alternative_u_exact_all(self):
        rows=generate("WEAK_BETWEEN",DESIGNS[1][1],F(1),F(1,4),F(-2),F(1,4))
        for r in rows:
            self.assertEqual(r["y"],F(1)+F(1,4)*r["x"]+r["group_intercept_alias_u"]+r["epsilon"])
    def test_invalid_design_rejected(self):
        with self.assertRaises(ValueError):
            generate("NOT_A_DESIGN",DESIGNS[0][1],F(0),F(1,4),F(0),F(0))
    def test_invalid_noise_rejected(self):
        with self.assertRaises(ValueError):
            generate("BALANCED",DESIGNS[0][1],F(0),F(1,4),F(0),F(1,3))
    def test_invalid_rank_normal_equations(self):
        with self.assertRaises(ValueError):
            solve([[1,1],[1,1]],[0,0])
    def test_invalid_theta_rejected(self):
        rows=generate("BALANCED",DESIGNS[0][1],F(0),F(1,4),F(0),F(0))
        with self.assertRaises(ValueError):
            quasi_demeaning_two_paths(rows,F(1,4),F(0),F(1,4),F(0),DESIGNS[0][1],group_means(rows))
    def test_exact_group_degenerate_between_is_unknown(self):
        rows=generate("BALANCED",DESIGNS[0][1],F(0),F(1,4),F(2),F(0))
        self.assertIsNone(between_two_paths(group_means(rows)))
    def test_full_OLS_residual_exact(self):
        rows=generate("STRONG_BETWEEN",DESIGNS[2][1],F(1),F(1,4),F(4),F(1,2))
        self.assertEqual(sum((r["epsilon"]**2 for r in rows),F(0)),F(12))
    def test_quasi_theta_one_reproduces_FE(self):
        rows=generate("WEAK_BETWEEN",DESIGNS[1][1],F(1),F(1,4),F(-2),F(1,4))
        self.assertEqual(quasi_demeaning_two_paths(rows,F(1),F(1),F(1,4),F(-2),DESIGNS[1][1],group_means(rows)),F(1,4))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
