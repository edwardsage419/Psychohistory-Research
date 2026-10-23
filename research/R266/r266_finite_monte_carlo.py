#!/usr/bin/env python3
"""R266 finite Monte Carlo design audit: 5328 artificial source atom types.

The enumerator and the independent convolution use different computation paths.
There are no actual human observations and no pseudo-random observations.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
FREEZE = "634230df411eca00badadaa0c593f28ae08773c8"
VALUES = (0, 1, 2, 3)
DESIGNS = ("IID", "ANTITHETIC")
FUNCTIONS = ("THRESHOLD_Q1", "THRESHOLD_HALF", "THRESHOLD_Q3", "SYMMETRIC_EXTREMES")
WORLDS = tuple((f, n) for f in FUNCTIONS[:3] for n in (2, 4)) + tuple(
    ("SYMMETRIC_EXTREMES", n) for n in (2, 4, 6)
)
ZERO, ONE = F(0), F(1)


def event(name, u):
    if name not in FUNCTIONS or u not in VALUES:
        raise ValueError("unfrozen event/source")
    if name == "THRESHOLD_Q1":
        return int(u == 0)
    if name == "THRESHOLD_HALF":
        return int(u <= 1)
    if name == "THRESHOLD_Q3":
        return int(u <= 2)
    return int(u in (0, 3))


def validate(name, n, design):
    if (name, n) not in WORLDS or design not in DESIGNS:
        raise ValueError("unfrozen world/design")


def success_count(name, origin, design):
    if design == "IID":
        return sum(event(name, x) for x in origin)
    return sum(event(name, u) + event(name, 3 - u) for u in origin)


def draw_count(n, design):
    return n if design == "IID" else n // 2


def source_rows(name, n, design):
    """Route A: enumerate the entire primitive sample-space, no convolution."""
    validate(name, n, design)
    k = draw_count(n, design)
    mass = F(1, 4 ** k)
    for origin in itertools.product(VALUES, repeat=k):
        hit = success_count(name, origin, design)
        estimate = F(hit, n)
        truth = F(sum(event(name, u) for u in VALUES), 4)
        yield dict(world=f"{name}_N{n}", function=name, evaluations=n,
                   design=design, primitive_independent_draws=k,
                   original_source_tuple=";".join(str(u) for u in origin),
                   exact_source_mass=mass, event_success_count=hit,
                   estimate=estimate, true_integral=truth,
                   squared_error=(estimate-truth)**2)


def enumerated_pmf(name, n, design):
    pmf = defaultdict(lambda: ZERO)
    rows = 0
    for row in source_rows(name, n, design):
        pmf[row["estimate"]] += row["exact_source_mass"]
        rows += 1
    assert sum(pmf.values(), ZERO) == ONE
    assert rows == 4 ** draw_count(n, design)
    return dict(pmf), rows


def convolution_pmf(name, n, design):
    """Route B: marginal polynomial convolution; never call source_rows."""
    validate(name, n, design)
    single = defaultdict(lambda: ZERO)
    for u in VALUES:
        successes = (event(name, u) if design == "IID"
                     else event(name, u) + event(name, 3-u))
        single[successes] += F(1, 4)
    distribution = {0: ONE}
    for _ in range(draw_count(n, design)):
        nxt = defaultdict(lambda: ZERO)
        for old_count, old_prob in distribution.items():
            for new_count, new_prob in single.items():
                nxt[old_count + new_count] += old_prob * new_prob
        distribution = dict(nxt)
    return {F(k, n): v for k, v in distribution.items() if v}


def moments(pmf, truth):
    mean = sum((x * prob for x, prob in pmf.items()), ZERO)
    variance = sum(((x-mean)**2 * prob for x, prob in pmf.items()), ZERO)
    bias = mean - truth
    mse = sum(((x-truth)**2 * prob for x, prob in pmf.items()), ZERO)
    assert variance + bias*bias == mse
    return mean, variance, bias, mse


def formula_moments(name, n):
    """Third route: four-point marginal covariance and independent-pair sums."""
    validate(name, n, "IID")
    marg = [event(name, u) for u in VALUES]
    p = F(sum(marg), 4)
    product = F(sum(event(name, u) * event(name, 3-u) for u in VALUES), 4)
    covariance = product - p*p
    iid = p*(1-p)/n
    anti = (p*(1-p)+covariance)/n
    return p, covariance, iid, anti


def world_result(name, n):
    p, covariance, expect_iid, expect_anti = formula_moments(name, n)
    designs = {}
    for design in DESIGNS:
        pmf_a, rows = enumerated_pmf(name, n, design)
        pmf_b = convolution_pmf(name, n, design)
        if pmf_a != pmf_b:
            raise AssertionError("independent exact PMFs disagree")
        mean, variance, bias, mse = moments(pmf_a, p)
        target = expect_iid if design == "IID" else expect_anti
        if (mean, variance, bias, mse) != (p, target, ZERO, target):
            raise AssertionError("pre-registered formula mismatch")
        designs[design] = dict(
            source_atoms=rows, primitive_independent_draws=draw_count(n, design),
            function_evaluations=n, exact_mean=str(mean),
            exact_variance=str(variance), exact_bias=str(bias),
            exact_MSE=str(mse),
            exact_complete_estimator_PMF={str(k): str(v) for k,v in sorted(pmf_a.items())},
            exact_PMF_independent_convolution_verified=True)
    return dict(world=f"{name}_N{n}", function=name, evaluations=n,
                true_integral=str(p), antithetic_pair_covariance=str(covariance),
                antithetic_over_IID_variance_ratio=str(expect_anti/expect_iid),
                designs=designs)


def frozen_claims():
    assert len(WORLDS) == 9
    assert sum(4**n for _,n in WORLDS) == 5184
    assert sum(4**(n//2) for _,n in WORLDS) == 144
    for name,n in WORLDS:
        result=world_result(name,n)
        p=F(result["true_integral"])
        cov=F(result["antithetic_pair_covariance"])
        ratio=F(result["antithetic_over_IID_variance_ratio"])
        if name in ("THRESHOLD_Q1","THRESHOLD_Q3"):
            assert p in (F(1,4), F(3,4))
            assert cov==F(-1,16) and ratio==F(2,3)
        elif name=="THRESHOLD_HALF":
            assert p==F(1,2) and cov==F(-1,4) and ratio==ZERO
        else:
            assert name=="SYMMETRIC_EXTREMES"
            assert p==F(1,2) and cov==F(1,4) and ratio==F(2)
        assert result["designs"]["IID"]["exact_mean"] == str(p)
        assert result["designs"]["ANTITHETIC"]["exact_mean"] == str(p)
    return True


def emit():
    frozen_claims()
    src_path=HERE/"R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv"
    names=("world","function","evaluations","design",
           "primitive_independent_draws","original_source_tuple",
           "exact_source_mass","event_success_count","estimate",
           "true_integral","squared_error")
    with src_path.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=names,lineterminator="\n")
        writer.writeheader()
        for fn,n in WORLDS:
            for design in DESIGNS:
                for row in source_rows(fn,n,design):
                    writer.writerow({k:str(row[k]) for k in names})
    results=dict(research_id="R266",original_catalogue_id="11-026",
                 prescore_freeze_commit=FREEZE,
                 evidence="E1_EXACT_FINITE_ARTIFICIAL_SAMPLE_SPACES_ONLY",
                 frozen_world_count=9,
                 original_complete_IID_source_types=5184,
                 original_complete_ANTITHETIC_source_types=144,
                 original_complete_total_source_types=5328,
                 all_18_exact_PMFs_independently_convolved=True,
                 antithetic_can_worsen_variance_for_symmetric_event=True,
                 no_real_stochastic_trial_executed=True,
                 no_real_human_E2=0,no_real_historical_E3=0,
                 R073="FROZEN",PESEN_v0_1="FROZEN",
                 worlds=[world_result(*w) for w in WORLDS])
    result_path=HERE/"R266_EXACT_FINITE_MC_RESULTS.json"
    result_path.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R266",prescore_freeze_commit=FREEZE,
                 frozen_worlds=9,complete_source_types=5328,
                 independently_verified_PMF_comparisons=18,
                 source_sha256=hashlib.sha256(src_path.read_bytes()).hexdigest(),
                 results_sha256=hashlib.sha256(result_path.read_bytes()).hexdigest(),
                 no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R266_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt


class Tests(unittest.TestCase):
    def test_all_frozen(self): self.assertTrue(frozen_claims())
    def test_worlds(self): self.assertEqual(len(WORLDS),9)
    def test_source_count(self): self.assertEqual(sum(4**n+4**(n//2) for _,n in WORLDS),5328)
    def test_invalid_function(self):
        with self.assertRaises(ValueError): event("FAKE",0)
    def test_invalid_source(self):
        with self.assertRaises(ValueError): event("THRESHOLD_Q1",4)
    def test_invalid_design(self):
        with self.assertRaises(ValueError): list(source_rows("THRESHOLD_Q1",2,"NONEXISTENT"))
    def test_invalid_world(self):
        with self.assertRaises(ValueError): world_result("THRESHOLD_Q1",6)
    def test_event_symmetric(self):
        self.assertTrue(all(event("SYMMETRIC_EXTREMES",u)==event("SYMMETRIC_EXTREMES",3-u) for u in VALUES))
    def test_source_anticorrelated(self):
        self.assertEqual(formula_moments("THRESHOLD_HALF",2)[1],-F(1,4))
    def test_source_positively_correlated(self):
        self.assertEqual(formula_moments("SYMMETRIC_EXTREMES",2)[1],F(1,4))


def world_case(name,n,design,kind):
    def checker(self):
        rows=list(source_rows(name,n,design))
        pmf, sz=enumerated_pmf(name,n,design)
        if kind=="mass":
            self.assertEqual(sum((r["exact_source_mass"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({r["original_source_tuple"] for r in rows}),len(rows))
        elif kind=="count":
            self.assertEqual(sz,4**draw_count(n,design))
        elif kind=="pmf":
            self.assertEqual(pmf,convolution_pmf(name,n,design))
        elif kind=="moments":
            p,cov,v1,v2=formula_moments(name,n)
            self.assertEqual(moments(pmf,p),(p,v1 if design=="IID" else v2,ZERO,v1 if design=="IID" else v2))
        elif kind=="success":
            self.assertTrue(all(0<=r["event_success_count"]<=n and r["estimate"]==F(r["event_success_count"],n) for r in rows))
        elif kind=="square":
            self.assertTrue(all(r["squared_error"]==(r["estimate"]-r["true_integral"])**2 for r in rows))
        else:
            raise AssertionError("invalid test")
    return checker


for name,n in WORLDS:
    for design in DESIGNS:
        for kind in ("mass","unique","count","pmf","moments","success","square"):
            setattr(Tests,f"test_{name.lower()}_n{n}_{design.lower()}_{kind}",
                    world_case(name,n,design,kind))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:
        unittest.main(argv=["r266"],verbosity=2)
    else:
        print(json.dumps(emit(),indent=2))
