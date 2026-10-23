#!/usr/bin/env python3
"""R243 exact finite Rademacher Euler-Maruyama-style noise PATH SURROGATE.

CRITICAL: increments ±1/2 match Gaussian Brownian dt=1/4 only in their first
two moments. They are NOT Brownian increments or exact continuous-time SDE
solutions. Full 4-bit source space, no Monte Carlo. Do not conflate diffusion
path laws with latent state changes or stochastic sensor readings.
"""
from __future__ import annotations
import csv,hashlib,itertools,json,unittest,argparse
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0);ONE=F(1);DT=F(1,4)
FREEZE="4733342e3fd16083468541f557f3bb2bffa3ce69"
STEPS=(0,1,2,3,4)
PATHS=tuple(itertools.product((-1,1),repeat=4))
WORLDS=(
"ADDITIVE_SYMMETRIC","ADDITIVE_NEGATIVE_SIGMA","ADDITIVE_DOUBLE_SIGMA",
"ADDITIVE_DRIFT_ONE","COMMON_SHOCK_REPEAT",
"STATIC_HIDDEN_STOCHASTIC_SENSOR","HIDDEN_DOUBLE_SCALE",
"MULTIPLICATIVE_EM_ZERO_DRIFT","MULTIPLICATIVE_EM_POSITIVE_DRIFT"
)
POINTWISE_ALIASES=("ADDITIVE_SYMMETRIC","STATIC_HIDDEN_STOCHASTIC_SENSOR","HIDDEN_DOUBLE_SCALE")

def validate(world,eps):
    if world not in WORLDS:raise ValueError("unknown finite noise world")
    if len(eps)!=4 or any(x not in (-1,1) for x in eps):
        raise ValueError("noise increment path not in frozen support")

def simulate(world,eps):
    """Step recurrence uses true hidden state and frozen observed sensor."""
    validate(world,eps)
    h=ONE if world.startswith("MULTIPLICATIVE") else ZERO
    hidden=[h];visible=[h]
    for i,e in enumerate(eps):
        z=F(e,2)
        if world=="ADDITIVE_NEGATIVE_SIGMA":h-=z
        elif world in ("ADDITIVE_DOUBLE_SIGMA","HIDDEN_DOUBLE_SCALE"):h+=2*z
        elif world=="ADDITIVE_DRIFT_ONE":h+=DT+z
        elif world=="COMMON_SHOCK_REPEAT":h+=F(eps[0],2)
        elif world=="STATIC_HIDDEN_STOCHASTIC_SENSOR":h=h
        elif world=="MULTIPLICATIVE_EM_ZERO_DRIFT":h*=ONE+z
        elif world=="MULTIPLICATIVE_EM_POSITIVE_DRIFT":h*=ONE+F(1,8)+z
        else:h+=z
        hidden.append(h)
        if world=="STATIC_HIDDEN_STOCHASTIC_SENSOR":
            y=sum((F(eps[j],2) for j in range(i+1)),ZERO)
        elif world=="HIDDEN_DOUBLE_SCALE":y=h/2
        else:y=h
        visible.append(y)
    return tuple(hidden),tuple(visible)

def independent_closed_observed(world,eps):
    """Independent explicit formula: does not call the source simulator."""
    validate(world,eps)
    result=[]
    for n in STEPS:
        if world in ("ADDITIVE_SYMMETRIC","STATIC_HIDDEN_STOCHASTIC_SENSOR","HIDDEN_DOUBLE_SCALE"):
            y=sum((F(eps[j],2) for j in range(n)),ZERO)
        elif world=="ADDITIVE_NEGATIVE_SIGMA":
            y=-sum((F(eps[j],2) for j in range(n)),ZERO)
        elif world=="ADDITIVE_DOUBLE_SIGMA":
            y=sum((F(eps[j]) for j in range(n)),ZERO)
        elif world=="ADDITIVE_DRIFT_ONE":
            y=F(n,4)+sum((F(eps[j],2) for j in range(n)),ZERO)
        elif world=="COMMON_SHOCK_REPEAT":
            y=F(n*eps[0],2)
        elif world.startswith("MULTIPLICATIVE"):
            d=F(1,8) if world=="MULTIPLICATIVE_EM_POSITIVE_DRIFT" else ZERO
            y=ONE
            for j in range(n):y*=ONE+d+F(eps[j],2)
        else:raise AssertionError("no frozen formula")
        result.append(y)
    return tuple(result)

def source_atom(world,eps):
    h,y=simulate(world,eps)
    if y!=independent_closed_observed(world,eps):
        raise AssertionError("independent noise source path formula inconsistent")
    d=tuple(y[n+1]-y[n] for n in range(4))
    return dict(
      world=world,
      oracle_original_epsilon_1=eps[0],oracle_original_epsilon_2=eps[1],
      oracle_original_epsilon_3=eps[2],oracle_original_epsilon_4=eps[3],
      observed_y0=y[0],observed_y1=y[1],observed_y2=y[2],
      observed_y3=y[3],observed_y4=y[4],
      observed_increment1=d[0],observed_increment2=d[1],
      observed_increment3=d[2],observed_increment4=d[3],
      oracle_true_hidden_h0=h[0],oracle_true_hidden_h1=h[1],
      oracle_true_hidden_h2=h[2],oracle_true_hidden_h3=h[3],
      oracle_true_hidden_h4=h[4],
      original_path_probability=F(1,16)
    )

def sources(world):
    if world not in WORLDS:raise ValueError("world not frozen")
    rows=tuple(source_atom(world,eps) for eps in PATHS)
    if len(rows)!=16 or sum((r["original_path_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("full finite noise paths not enumerated")
    return rows

def visible_path_joint(world):
    out=defaultdict(F)
    for r in sources(world):
        p=tuple(r["observed_y"+str(i)] for i in STEPS)
        out[p]+=r["original_path_probability"]
    return dict(sorted(out.items()))

def independent_visible_path_joint(world):
    out=defaultdict(F)
    for eps in PATHS:out[independent_closed_observed(world,eps)]+=F(1,16)
    return dict(sorted(out.items()))

def observed_moments(world,n):
    if n not in STEPS:raise ValueError("outside frozen four-step horizon")
    rows=sources(world)
    avg=sum((r["original_path_probability"]*r["observed_y"+str(n)] for r in rows),ZERO)
    var=sum((r["original_path_probability"]*(r["observed_y"+str(n)]-avg)**2 for r in rows),ZERO)
    return avg,var

def independent_moments(world,n):
    """Analytical moment propagation with independent Rademacher source bits."""
    if n not in STEPS or world not in WORLDS:raise ValueError("unknown horizon or world")
    if world=="COMMON_SHOCK_REPEAT":return ZERO,F(n*n,4)
    if world.startswith("MULTIPLICATIVE"):
        d=F(1,8) if world=="MULTIPLICATIVE_EM_POSITIVE_DRIFT" else ZERO
        mu=(ONE+d)**n
        var=((ONE+d)**2+F(1,4))**n-mu*mu
        return mu,var
    drift=ONE if world=="ADDITIVE_DRIFT_ONE" else ZERO
    sigma=F(2) if world=="ADDITIVE_DOUBLE_SIGMA" else ONE
    return F(n,4)*drift,F(n,4)*sigma*sigma

def full_fourth_noise_moment():
    return sum((F(1,16)*sum(F(e,2) for e in path)**4 for path in PATHS),ZERO)

def validate_aliases():
    one=visible_path_joint("ADDITIVE_SYMMETRIC")
    for w in POINTWISE_ALIASES[1:]:
        if visible_path_joint(w)!=one:
            raise AssertionError("measurement and latent scale observation law diverged")
        for eps in PATHS:
            if simulate(w,eps)[1]!=simulate("ADDITIVE_SYMMETRIC",eps)[1]:
                raise AssertionError("pointwise source observation alias diverged")
    if visible_path_joint("ADDITIVE_NEGATIVE_SIGMA")!=one:
        raise AssertionError("signed diffusion noise is not distribution-identical")
    for eps in PATHS:
        comp=tuple(-e for e in eps)
        if simulate("ADDITIVE_NEGATIVE_SIGMA",eps)[1]!=simulate("ADDITIVE_SYMMETRIC",comp)[1]:
            raise AssertionError("negative diffusion sign requires epsilon complement bijection")
    assert observed_moments("COMMON_SHOCK_REPEAT",1)==observed_moments("ADDITIVE_SYMMETRIC",1)
    assert observed_moments("COMMON_SHOCK_REPEAT",4)[1]==F(4)
    assert observed_moments("ADDITIVE_SYMMETRIC",4)[1]==ONE
    assert observed_moments("STATIC_HIDDEN_STOCHASTIC_SENSOR",4)==(ZERO,ONE)
    assert all(r["oracle_true_hidden_h4"]==ZERO for r in sources("STATIC_HIDDEN_STOCHASTIC_SENSOR"))
    assert full_fourth_noise_moment()==F(5,2)
    return True

def result_for_world(world):
    rows=sources(world)
    joint=visible_path_joint(world)
    if joint!=independent_visible_path_joint(world):
        raise AssertionError("source and independent closed source path laws disagree")
    moment=[observed_moments(world,n) for n in STEPS]
    for n,(mu,var) in enumerate(moment):
        if (mu,var)!=independent_moments(world,n):
            raise AssertionError("observed moments fail independent algebraic closure")
    if world=="MULTIPLICATIVE_EM_ZERO_DRIFT":
        assert moment[4]==(ONE,F(369,256))
    if world=="ADDITIVE_DRIFT_ONE":assert moment[4]==(ONE,ONE)
    return dict(
        world=world,full_original_noise_path_source_atoms=16,
        observable_path_support_size=len(joint),
        observed_mean_by_step=[str(x[0]) for x in moment],
        observed_variance_by_step=[str(x[1]) for x in moment],
        exact_full_observed_five_point_path_joint={
            ",".join(str(z) for z in k):str(v) for k,v in joint.items()
        },
        artificial_oracle_terminal_hidden_h4_by_epsilon_source=[
            str(r["oracle_true_hidden_h4"]) for r in rows
        ],
        independent_closed_formula_path_integral=True,
        independent_analytical_first_two_moments=True
    )

def generate():
    validate_aliases()
    res=dict(
       research_id="R243",original_catalogue_id="11-003",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_RADEMACHER_EULER_STYLE_SURROGATE_NOT_BROWNIAN_SDE",
       frozen_worlds=9,full_original_epsilon_path_atoms=144,
       discrete_time_step="1/4",epsilon_increment_variance="1/4",
       epsilon_increment_fourth_moment="1/16",
       same_variance_gaussian_increment_fourth_moment="3/16",
       four_step_artificial_terminal_fourth_moment=str(full_fourth_noise_moment()),
       same_variance_gaussian_terminal_fourth_moment="3",
       exact_same_observed_full_path_pairs=[
           ["ADDITIVE_SYMMETRIC","ADDITIVE_NEGATIVE_SIGMA"],
           ["ADDITIVE_SYMMETRIC","STATIC_HIDDEN_STOCHASTIC_SENSOR"],
           ["ADDITIVE_SYMMETRIC","HIDDEN_DOUBLE_SCALE"]
       ],
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[result_for_world(w) for w in WORLDS]
    )
    src=HERE/"R243_ALL_144_ORIGINAL_FOUR_NOISE_INCREMENT_PATHS.csv"
    fields=list(sources("ADDITIVE_SYMMETRIC")[0])
    with src.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for world in WORLDS:
            for row in sources(world):
                writer.writerow({k:str(row[k]) for k in fields})
    path=HERE/"R243_EXACT_RESULTS.json"
    path.write_text(json.dumps(res,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec=dict(
       research_id="R243",original_catalogue_id="11-003",
       frozen_worlds=9,all_four_bit_noise_sources=144,
       discrete_noise_is_not_gaussian_Brownian=True,
       independent_full_path_and_first_two_moment_calculation=True,
       signed_sigma_distribution_alias=True,
       stochastic_sensor_sourcewise_alias=True,
       source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R243_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_144_source_paths(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),144)
    def test_four_bit_sources(self):self.assertEqual(len(PATHS),16)
    def test_all_observation_aliases(self):self.assertTrue(validate_aliases())
    def test_noise_different_gaussian_fourth(self):
        self.assertEqual(full_fourth_noise_moment(),F(5,2))
        self.assertNotEqual(full_fourth_noise_moment(),F(3))
    def test_multiv_zero(self):self.assertEqual(observed_moments("MULTIPLICATIVE_EM_ZERO_DRIFT",4),(ONE,F(369,256)))
    def test_ito_em_drift_mean(self):
        self.assertEqual(observed_moments("MULTIPLICATIVE_EM_POSITIVE_DRIFT",4)[0],F(9,8)**4)
    def test_additive_drift(self):
        self.assertEqual(observed_moments("ADDITIVE_DRIFT_ONE",4),(ONE,ONE))
    def test_common_shock_var(self):
        self.assertEqual(observed_moments("COMMON_SHOCK_REPEAT",4)[1],F(4))
    def test_opposite_sigma(self):
        self.assertEqual(visible_path_joint("ADDITIVE_SYMMETRIC"),visible_path_joint("ADDITIVE_NEGATIVE_SIGMA"))
    def test_static_hidden(self):
        self.assertTrue(all(r["oracle_true_hidden_h4"]==ZERO for r in sources("STATIC_HIDDEN_STOCHASTIC_SENSOR")))
    def test_bad_source(self):
        with self.assertRaises(ValueError):source_atom("ADDITIVE_SYMMETRIC",(1,1,0,1))

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_path_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({tuple(r["oracle_original_epsilon_"+str(i)] for i in (1,2,3,4)) for r in rows}),16)
        elif kind=="positive":
            self.assertTrue(all(r["original_path_probability"]>0 for r in rows))
        elif kind=="closed_path":
            for eps in PATHS:
                self.assertEqual(simulate(world,eps)[1],independent_closed_observed(world,eps))
        elif kind=="joint":
            self.assertEqual(visible_path_joint(world),independent_visible_path_joint(world))
        elif kind=="moments":
            for n in STEPS:self.assertEqual(observed_moments(world,n),independent_moments(world,n))
        elif kind=="increments":
            for row in rows:
                self.assertEqual(tuple(row["observed_increment"+str(i)] for i in (1,2,3,4)),
                    tuple(row["observed_y"+str(i)]-row["observed_y"+str(i-1)] for i in (1,2,3,4)))
        elif kind=="result":
            self.assertEqual(result_for_world(world)["full_original_noise_path_source_atoms"],16)
        else:raise AssertionError("not an approved test")
    return t
for _w in WORLDS:
    for _kind in ("mass","unique","positive","closed_path","joint","moments","increments","result"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    args=ap.parse_args()
    if args.test:unittest.main(argv=["r243"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
