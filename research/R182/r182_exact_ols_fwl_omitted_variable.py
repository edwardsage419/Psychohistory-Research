"""R182 finite full factorial OLS omitted-variable and FWL exact proof.

All 240 worlds and 2880 observation rows are project-specified artificial
records. Coefficients are independently computed through rational normal
equations and separate subgroup demeaning, without floating-point solvers.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import csv
import json
import sys
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R182_OLS_FWL_240_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R182_EXACT_RESULTS.json"
RAW=HERE/"R182_ALL_2880_ARTIFICIAL_OBSERVATIONS.csv"
ACCEPT=HERE/"R182_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R182_Exact_240_OLS_FWL_Worlds.zip"

DESIGNS=(
 ("BALANCED",(2,2,2,2)),
 ("POSITIVE",(4,2,2,4)),
 ("NEGATIVE",(2,4,4,2)),
 ("STRONG_POSITIVE",(6,2,2,6)),
)
INTERCEPTS=(F(0),F(1))
TRUE_BETAS=(F(1,4),F(1,2))
GROUP_EFFECTS=(F(-2),F(-1),F(0),F(1),F(2))
NOISE_LEVELS=(F(0),F(1,4),F(1,2))
CELLS=((0,0),(0,1),(1,0),(1,1))


def worlds():
    for (design,counts),a,b,c,e in product(DESIGNS,INTERCEPTS,TRUE_BETAS,GROUP_EFFECTS,NOISE_LEVELS):
        yield design,counts,a,b,c,e


def generate(design,counts,a,b,c,e):
    if design not in dict(DESIGNS) or counts != dict(DESIGNS)[design]:
        raise ValueError("unregistered source cell design")
    if a not in INTERCEPTS or b not in TRUE_BETAS or c not in GROUP_EFFECTS or e not in NOISE_LEVELS:
        raise ValueError("unregistered artificial response parameters")
    rows=[]
    for (x,z),size in zip(CELLS,counts):
        if size<2 or size%2:
            raise ValueError("each source cell must have balanced plus/minus residuals")
        for idx in range(size):
            eps=e if idx<size//2 else -e
            y=a+b*x+c*z+eps
            rows.append({"x":F(x),"z":F(z),"y":y,"epsilon":eps,
                         "artificial_cell":f"{x},{z}",
                         "cell_record":idx})
    return rows


def solve_linear(matrix,rhs):
    """Gauss-Jordan exact elimination with singular rank rejection."""
    n=len(rhs)
    if n==0 or len(matrix)!=n or any(len(row)!=n for row in matrix):
        raise ValueError("invalid normal equation dimension")
    aug=[[F(v) for v in row]+[F(rhs[i])] for i,row in enumerate(matrix)]
    for col in range(n):
        pivot=next((i for i in range(col,n) if aug[i][col]!=0),None)
        if pivot is None:
            raise ValueError("rank deficient design, unique OLS unavailable")
        aug[col],aug[pivot]=aug[pivot],aug[col]
        scale=aug[col][col]
        aug[col]=[v/scale for v in aug[col]]
        for i in range(n):
            if i==col:
                continue
            amount=aug[i][col]
            aug[i]=[x-amount*y for x,y in zip(aug[i],aug[col])]
    return tuple(row[n] for row in aug)


def ols_normal_equations(rows,fields):
    if not rows:
        raise ValueError("empty source")
    columns=[lambda r:F(1)]+[lambda r,name=name:r[name] for name in fields]
    Gram=[[sum((f(row)*g(row) for row in rows),F(0)) for g in columns] for f in columns]
    cross=[sum((f(row)*row["y"] for row in rows),F(0)) for f in columns]
    return solve_linear(Gram,cross)


def mean(values):
    if not values:
        raise ValueError("empty group")
    return sum(values,F(0))/len(values)


def stratified_average(rows,key,value,group):
    return mean([r[value] for r in rows if r[key]==group])


def ols_independent_demeaning(rows):
    """Entirely separate Frisch Waugh Lovell and two-group mean algorithm."""
    xs=[r["x"] for r in rows]
    zs=[r["z"] for r in rows]
    ys=[r["y"] for r in rows]
    # Simple slope from the exact two conditional cell means.
    simple_beta=stratified_average(rows,"x","y",F(1))-stratified_average(rows,"x","y",F(0))
    simple_intercept=stratified_average(rows,"x","y",F(0))
    # Partial out z for x slope, independently partial out x for z slope.
    x_res=[r["x"]-stratified_average(rows,"z","x",r["z"]) for r in rows]
    y_res_z=[r["y"]-stratified_average(rows,"z","y",r["z"]) for r in rows]
    denom_x=sum((v*v for v in x_res),F(0))
    if denom_x==0:
        raise ValueError("x perfectly determined by z")
    beta=sum((v*w for v,w in zip(x_res,y_res_z)),F(0))/denom_x
    z_res=[r["z"]-stratified_average(rows,"x","z",r["x"]) for r in rows]
    y_res_x=[r["y"]-stratified_average(rows,"x","y",r["x"]) for r in rows]
    denom_z=sum((v*v for v in z_res),F(0))
    if denom_z==0:
        raise ValueError("z perfectly determined by x")
    gamma=sum((v*w for v,w in zip(z_res,y_res_x)),F(0))/denom_z
    intercept=mean(ys)-beta*mean(xs)-gamma*mean(zs)
    return (simple_intercept,simple_beta),(intercept,beta,gamma)


def residual_diagnostics(rows,fields,coefs):
    err=[]
    for r in rows:
        predicted=coefs[0]+sum((coefs[i+1]*r[name] for i,name in enumerate(fields)),F(0))
        err.append(r["y"]-predicted)
    orth={"intercept":str(sum(err,F(0)))}
    for name in fields:
        orth[name]=str(sum((r[name]*e for r,e in zip(rows,err)),F(0)))
    if any(F(v)!=0 for v in orth.values()):
        raise AssertionError("normal equation residuals not orthogonal")
    sse=sum((v*v for v in err),F(0))
    return {"SSE":str(sse),"residual_normal_equation_crossproducts":orth}


def estimate(design,counts,a,b,c,e):
    obs=generate(design,counts,a,b,c,e)
    low_a=ols_normal_equations(obs,("x",))
    high_a=ols_normal_equations(obs,("x","z"))
    low_b,high_b=ols_independent_demeaning(obs)
    if low_a!=low_b or high_a!=high_b:
        raise AssertionError("independent normal equation and FWL estimates do not match")
    if high_a!=(a,b,c):
        raise AssertionError("adjusted full linear model failed to recover artificial coefficients")
    n=len(obs)
    raw0=residual_diagnostics(obs,("x",),low_a)
    raw1=residual_diagnostics(obs,("x","z"),high_a)
    if F(raw1["SSE"])!=n*e*e or F(raw0["SSE"])<F(raw1["SSE"]):
        raise AssertionError("SSE identity and residual nesting failed")
    z0=stratified_average(obs,"x","z",F(0))
    z1=stratified_average(obs,"x","z",F(1))
    delta=z1-z0
    if low_a[1]!=b+c*delta:
        raise AssertionError("conditional omitted-variable bias identity failed")
    return obs,{
        "design":design,
        "cell_counts_in_00_01_10_11_order":list(counts),
        "observations":n,
        "true_a":str(a),"true_x_slope_b":str(b),
        "true_group_slope_c":str(c),"residual_amplitude_e":str(e),
        "observed_z_fraction_given_x0":str(z0),
        "observed_z_fraction_given_x1":str(z1),
        "z_group_imbalance_delta":str(delta),
        "omitted_variable_slope_prediction":str(b+c*delta),
        "simple_intercept":str(low_a[0]),"simple_x_coefficient":str(low_a[1]),
        "adjusted_intercept":str(high_a[0]),
        "adjusted_x_coefficient":str(high_a[1]),
        "adjusted_z_coefficient":str(high_a[2]),
        "simple_diagnostics":raw0,"adjusted_diagnostics":raw1,
        "simple_x_negative_despite_true_positive":low_a[1]<0,
        "independent_FWL_and_normal_equation_coefficients_equal":True,
    }


def archive():
    files=[Path(__file__).name,OUT.name,RAW.name,ACCEPT.name]
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
    print("R182_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


def run():
    cases=[]
    raw=[]
    for design,counts,a,b,c,e in worlds():
        obs,record=estimate(design,counts,a,b,c,e)
        idx=len(cases)
        cases.append(record)
        for i,r in enumerate(obs):
            raw.append({
                "world_index":idx,"design":design,
                "record_index":i,
                "x":str(r["x"]),"z":str(r["z"]),
                "y":str(r["y"]),"cell":r["artificial_cell"],
                "cell_record":r["cell_record"],"error_epsilon":str(r["epsilon"]),
                "true_a":str(a),"true_b":str(b),"true_c":str(c),
            })
    if len(cases)!=240 or len(raw)!=2880:
        raise AssertionError("frozen model world or original row count drifted")
    anchors=[c for c in cases if c["design"]=="STRONG_POSITIVE" and c["true_a"]=="0"
             and c["true_x_slope_b"]=="1/4" and c["true_group_slope_c"]=="-2"
             and c["residual_amplitude_e"]=="1/4"]
    if len(anchors)!=1 or anchors[0]["simple_x_coefficient"]!="-3/4" or anchors[0]["adjusted_x_coefficient"]!="1/4":
        raise AssertionError("prescored omission sign reversal did not replicate")
    with RAW.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(raw[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(raw)
    reversal_count=sum(int(w["simple_x_negative_despite_true_positive"]) for w in cases)
    result={
        "research_id":"R182",
        "stage":"E1_ARTIFICIAL_EXACT_OLS_FWL_OMITTED_VARIABLE",
        "protocol":"protocols/"+PROTO.name,
        "worlds":240,"original_observations":2880,
        "design_cell_size_sets":{k:list(v) for k,v in DESIGNS},
        "all_full_adjusted_slopes_equal_true":True,
        "all_two_independent_Fraction_OLS_methods_agree":True,
        "all_slope_omission_bias_identities_verified":True,
        "all_residuals_orthogonal_and_adjusted_SSE_never_worse":True,
        "simple_slope_negative_despite_positive_structural_b_count":reversal_count,
        "fixed_aggregate_sign_reversal":anchors[0],
        "all_worlds":cases,
        "source_artificial_CSV_sha256":sha256(RAW.read_bytes()).hexdigest(),
        "independent_true_randomized_experiment":False,
        "external_historical_prediction":False,
        "new_E2":0,"new_E3":0,
    }
    OUT.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accept={
        "research_id":"R182","state":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_OLS",
        "worlds":240,"original_rows":2880,
        "normal_equation_and_independent_FWL_OLS_exact":True,
        "fully_adjusted_original_structural_slopes_recovered":True,
        "all_exact_omitted_variable_identities_passed":True,
        "fixed_omitted_variable_sign_reversal_proven":True,
        "all_residuals_normal_equation_orthogonal":True,
        "simple_sign_reversal_worlds":reversal_count,
        "result_sha256":sha256(OUT.read_bytes()).hexdigest(),
        "source_rows_sha256":result["source_artificial_CSV_sha256"],
        "real_human_or_historical_data":False,
        "new_E2":0,"new_E3":0,
    }
    ACCEPT.write_text(json.dumps(accept,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R182_MACHINE_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R182_PRIMARY_SIGN_REVERSAL",json.dumps(anchors[0],sort_keys=True))
    return result


class TestExactOLS(unittest.TestCase):
    def test_240_worlds(self):
        self.assertEqual(len(list(worlds())),240)
    def test_2880_observation_universe(self):
        self.assertEqual(sum(sum(k) for des,k,a,b,c,e in worlds()),2880)
    def test_all_design_cells_even_positive(self):
        self.assertTrue(all(all(v>=2 and v%2==0 for v in sizes) for name,sizes in DESIGNS))
    def test_design_four(self):
        self.assertEqual(len(DESIGNS),4)
    def test_positive_structural_slopes(self):
        self.assertTrue(all(b>0 for b in TRUE_BETAS))
    def test_no_random_sampler(self):
        self.assertEqual(NOISE_LEVELS,(F(0),F(1,4),F(1,2)))
    def test_construct_all_cell_balanced_residuals(self):
        for name,counts,a,b,c,e in worlds():
            rows=generate(name,counts,a,b,c,e)
            for cell in CELLS:
                d=[r["epsilon"] for r in rows if (int(r["x"]),int(r["z"]))==cell]
                self.assertEqual(sum(d,F(0)),0)
    def test_OLS_simple_hand_exact(self):
        obs=generate("BALANCED",(2,2,2,2),F(0),F(1,4),F(0),F(0))
        self.assertEqual(ols_normal_equations(obs,("x",)),(F(0),F(1,4)))
    def test_OLS_complete_hand(self):
        obs=generate("POSITIVE",(4,2,2,4),F(1),F(1,2),F(-1),F(1,4))
        self.assertEqual(ols_normal_equations(obs,("x","z")),(F(1),F(1,2),F(-1)))
    def test_OLS_two_independent_methods_all_worlds(self):
        for des,k,a,b,c,e in worlds():
            rows=generate(des,k,a,b,c,e)
            s,f=ols_independent_demeaning(rows)
            self.assertEqual(s,ols_normal_equations(rows,("x",)))
            self.assertEqual(f,ols_normal_equations(rows,("x","z")))
    def test_FWL_exact_Beta_true_all(self):
        for des,k,a,b,c,e in worlds():
            obs=generate(des,k,a,b,c,e)
            self.assertEqual(ols_independent_demeaning(obs)[1][1],b)
    def test_adjusted_all_true_structural_coefficients(self):
        for des,k,a,b,c,e in worlds():
            obs=generate(des,k,a,b,c,e)
            self.assertEqual(ols_normal_equations(obs,("x","z")),(a,b,c))
    def test_balanced_no_confounded_slope(self):
        for a in INTERCEPTS:
            for b in TRUE_BETAS:
                for c in GROUP_EFFECTS:
                    obs=generate("BALANCED",(2,2,2,2),a,b,c,F(1,4))
                    self.assertEqual(ols_normal_equations(obs,("x",))[1],b)
    def test_c_zero_no_omission(self):
        for name,k in DESIGNS:
            rows=generate(name,k,F(0),F(1,4),F(0),F(1,2))
            self.assertEqual(ols_normal_equations(rows,("x",))[1],F(1,4))
    def test_strong_confounded_sign_reversal(self):
        obs=generate("STRONG_POSITIVE",(6,2,2,6),F(0),F(1,4),F(-2),F(1,4))
        self.assertEqual(ols_normal_equations(obs,("x",))[1],F(-3,4))
        self.assertEqual(ols_normal_equations(obs,("x","z"))[1],F(1,4))
    def test_noise_level_not_changing_slopes(self):
        for e in NOISE_LEVELS:
            rows=generate("NEGATIVE",(2,4,4,2),F(0),F(1,4),F(2),e)
            self.assertEqual(ols_normal_equations(rows,("x","z")),(0,F(1,4),2))
    def test_adjusted_sse_exact(self):
        for des,k,a,b,c,e in worlds():
            rows=generate(des,k,a,b,c,e)
            diag=residual_diagnostics(rows,("x","z"),(a,b,c))
            self.assertEqual(F(diag["SSE"]),len(rows)*e*e)
    def test_nested_model_sse(self):
        obs=generate("POSITIVE",(4,2,2,4),F(0),F(1,4),F(2),F(1,4))
        a=ols_normal_equations(obs,("x",))
        b=ols_normal_equations(obs,("x","z"))
        self.assertGreaterEqual(F(residual_diagnostics(obs,("x",),a)["SSE"]),
                                F(residual_diagnostics(obs,("x","z"),b)["SSE"]))
    def test_OLS_residual_x_z_orthogonal(self):
        obs=generate("NEGATIVE",(2,4,4,2),F(0),F(1,2),F(2),F(1,2))
        v=residual_diagnostics(obs,("x","z"),ols_normal_equations(obs,("x","z")))
        self.assertEqual(v["residual_normal_equation_crossproducts"],
                         {"intercept":"0","x":"0","z":"0"})
    def test_rank_singular_rejected(self):
        r=[{"x":F(0),"z":F(0),"y":F(0)},
           {"x":F(1),"z":F(1),"y":F(1)},
           {"x":F(1),"z":F(1),"y":F(2)}]
        with self.assertRaises(ValueError):
            ols_normal_equations(r,("x","z"))
    def test_fwl_rank_singular_rejected(self):
        r=[{"x":F(0),"z":F(0),"y":F(0)},{"x":F(1),"z":F(1),"y":F(1)}]
        with self.assertRaises(ValueError):
            ols_independent_demeaning(r)
    def test_zero_data_fails(self):
        with self.assertRaises(ValueError):
            ols_normal_equations([],("x",))
    def test_unknown_design_fails(self):
        with self.assertRaises(ValueError):
            generate("INVALID",(2,2,2,2),F(0),F(1,4),F(0),F(0))
    def test_invalid_noise_fails(self):
        with self.assertRaises(ValueError):
            generate("BALANCED",(2,2,2,2),F(0),F(1,4),F(0),F(1,3))
    def test_gaussian_exact_diagonal(self):
        self.assertEqual(solve_linear([[F(2),F(0)],[F(0),F(3)]],[F(1),F(1)]),
                         (F(1,2),F(1,3)))
    def test_gaussian_rank_fails(self):
        with self.assertRaises(ValueError):
            solve_linear([[1,2],[2,4]],[3,6])
    def test_manual_implied_omission_bias(self):
        self.assertEqual(F(1,4)+F(-2)*(F(3,4)-F(1,4)),F(-3,4))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
