#!/usr/bin/env python3
"""Independent R304 full 432-option minimal-group audit; no import of original production model."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R304"
SOURCE=ROOT/"R304_ALL_432_ORIGINAL_MINIMAL_GROUP_ALLOCATION_OPTIONS.csv"
RESULT=ROOT/"R304_EXACT_SOCIAL_IDENTITY_ALLOCATION_RESULTS.json"
RECEIPT=ROOT/"R304_MACHINE_RECEIPT.json"
LEVELS=(Q(0),Q(1,2),Q(1))
LABELS=("A_INGROUP","B_INGROUP")
MENUS={"EQUAL_TOTAL_A_FAVORED":(10,6),"EQUAL_TOTAL_B_FAVORED":(6,10),
       "LOWER_TOTAL_A_FAVORED":(9,3),"LOWER_TOTAL_B_FAVORED":(3,9)}
WORLDS=list(itertools.product(LEVELS,LEVELS,LEVELS,LABELS,tuple(MENUS)))
OPTIONS=("BASE","ALTERNATIVE")
ALLFIELDS=("option","recipient_A_points","recipient_B_points","total_points",
  "ingroup_recipient","outgroup_recipient","ingroup_points","outgroup_points",
  "ingroup_minus_outgroup","absolute_inequality","identity_utility_term",
  "inequality_penalty_term","overall_utility","actor_personal_reward",
  "chosen_option","tie_select_BASE","choice_total_points",
  "aggregate_points_forgone","chosen_alt_lower_aggregate")

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def load():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def label(w):
    s,d,e,ingroup,menu=w
    return f"salience={s}|differentiation={d}|inequity={e}|label={ingroup}|menu={menu}"
def independent_delta(w):
    s,d,e,ingroup,menu=w
    altA,altB=MENUS[menu]
    relative=(altA-altB) if ingroup=="A_INGROUP" else altB-altA
    return (altA+altB-16)+s*d*relative-e*abs(relative)

def recompute(w,option):
    s,d,e,label,menu=w
    a,b=(8,8) if option=="BASE" else MENUS[menu]
    ingroupA=label=="A_INGROUP"
    group_effect=(a-b) if ingroupA else b-a
    total=a+b
    dispersion=abs(group_effect)
    identity=s*d*group_effect
    inequity=e*dispersion
    score=Q(total)+identity-inequity
    chosen="ALTERNATIVE" if independent_delta(w)>0 else "BASE"
    if chosen=="ALTERNATIVE":
        realized_total=sum(MENUS[menu])
    else:realized_total=16
    max_total=max(16,sum(MENUS[menu]))
    gone=max_total-realized_total
    fields={"option":option,"recipient_A_points":a,"recipient_B_points":b,
      "total_points":total,"ingroup_recipient":"A" if ingroupA else "B",
      "outgroup_recipient":"B" if ingroupA else "A",
      "ingroup_points":a if ingroupA else b,"outgroup_points":b if ingroupA else a,
      "ingroup_minus_outgroup":group_effect,"absolute_inequality":dispersion,
      "identity_utility_term":identity,"inequality_penalty_term":inequity,
      "overall_utility":score,"actor_personal_reward":0,
      "chosen_option":chosen,"tie_select_BASE":independent_delta(w)==0,
      "choice_total_points":realized_total,"aggregate_points_forgone":gone,
      "chosen_alt_lower_aggregate":chosen=="ALTERNATIVE" and gone>0}
    return {key:str(fields[key]) for key in ALLFIELDS}

def verify(rows,results):
    if len(rows)!=432 or len(results["worlds"])!=216:raise AssertionError("incomplete world universe")
    if results["synthetic_worlds"]!=216 or results["complete_option_source_rows"]!=432:raise AssertionError("wrong metadata")
    universe={(w,option) for w in WORLDS for option in OPTIONS}
    seen={}
    for row in rows:
        try:
            w=(Q(row["identity_salience"]),Q(row["group_differentiation_weight"]),
               Q(row["inequality_aversion"]),row["ingroup_label"],row["menu"])
            option=row["option"]
        except (ValueError,KeyError,ZeroDivisionError) as err:raise AssertionError("bad dimensions") from err
        k=(w,option)
        if k not in universe or k in seen:raise AssertionError("wrong/missing/duplicate source")
        if row["world"]!=label(w):raise AssertionError("source ID wrong")
        expected=recompute(w,option)
        for field in ALLFIELDS:
            if row[field]!=expected[field]:raise AssertionError("source field tampered "+field)
        seen[k]=row
    if set(seen)!=universe:raise AssertionError("missing option source")
    chosen_alt=equal_alt=lower_alt=0
    for i,w in enumerate(WORLDS):
        x=results["worlds"][i]
        s,d,e,ingroup,menu=w
        if x["world"]!=label(w):raise AssertionError("result identity false")
        for field,expected in (("identity_salience",str(s)),("group_differentiation_weight",str(d)),
             ("inequality_aversion",str(e)),("ingroup_label",ingroup),("menu",menu)):
            if x[field]!=expected:raise AssertionError("world field mismatch "+field)
        base=recompute(w,"BASE")
        alternative=recompute(w,"ALTERNATIVE")
        if x["option_values"]!=[base,alternative]:raise AssertionError("world source values don't match")
        if x["chosen_option"]!=base["chosen_option"]:raise AssertionError("selected option mismatch")
        if x["tie_select_BASE"]!=(base["tie_select_BASE"]=="True"):raise AssertionError("wrong tie")
        if x["choice_total_points"]!=int(base["choice_total_points"]):raise AssertionError("realized total wrong")
        if x["aggregate_points_forgone"]!=int(base["aggregate_points_forgone"]):raise AssertionError("total sacrifice wrong")
        if x["chosen_alt_lower_aggregate"]!=(base["chosen_alt_lower_aggregate"]=="True"):raise AssertionError("false sacrificed total")
        if x["original_source_rows"]!=2:raise AssertionError("count per world wrong")
        if base["chosen_option"]=="ALTERNATIVE":
            chosen_alt+=1
            if menu.startswith("EQUAL_TOTAL"):equal_alt+=1
            else:lower_alt+=1
    if (chosen_alt,equal_alt,lower_alt)!=(12,10,2):raise AssertionError("toy synthetic choice counts")
    report=results["summary"]
    if report!={"artificial_alternative_chosen_worlds":12,
         "equal_total_alternatives_chosen":10,
         "lower_total_alternatives_chosen":2,
         "identity_salience_zero_alternate_worlds":0,
         "no_difference_weight_alternate_worlds":0,
         "A_ingroup_s1_d1_e0_equal_total_A_alt_utility":"20",
         "A_ingroup_s1_d1_e0_lower_total_A_alt_utility":"18",
         "A_ingroup_s1_d1_e0_lower_total_A_total_forgone":4}:
        raise AssertionError("summary frozen expected results wrong")
    for d,e,ingroup,menu in itertools.product(LEVELS,LEVELS,LABELS,MENUS):
        w=(Q(0),d,e,ingroup,menu)
        if independent_delta(w)>0:raise AssertionError("invariant negative-salience control")
    return {"independent_direct_score_delta_source_audit":"PASS",
       "full_option_sources":432,"synthetic_worlds":216,
       "alternative_choices":12,"lower_total_favored_choices":2,
       "new_real_human_animal_E2":0,"historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    freeze="60f6406cede7eb5bb7cea9dc622835d8fe3f4c41"
    if r["freeze_commit"]!=freeze or j["freeze_commit"]!=freeze:raise AssertionError("wrong freeze")
    if j["original_catalogue_id"]!="03-003" or j["research_id"]!="R304":raise AssertionError("wrong ID")
    if j["social_identity_model_utility_invented_by_project"] is not True:
        raise AssertionError("claiming author original fitted model")
    if j["original_1971_human_allocation_data_reanalyzed"] is not False:
        raise AssertionError("claiming real original observations")
    if any(j[k]!=0 for k in ("distinct_real_human_E2_added","new_real_animal_E2","historical_E3_added")):
        raise AssertionError("synthetic source promoted to empirical evidence")
    if r["source_rows"]!=432 or r["new_E2"]!=0 or r["new_E3"]!=0:raise AssertionError("wrong receipt")
    if r["source_sha256"]!=hashlib.sha256(SOURCE.read_bytes()).hexdigest():raise AssertionError("source SHA")
    if r["results_sha256"]!=hashlib.sha256(RESULT.read_bytes()).hexdigest():raise AssertionError("result SHA")
    return {**verify(load(),j),"source_sha256":r["source_sha256"],"results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["full_option_sources"],432)
    def test_worlds(self):self.assertEqual(len(WORLDS),216)
    def test_favor_ingroup(self):self.assertEqual(independent_delta((Q(1),Q(1),Q(0),"A_INGROUP","EQUAL_TOTAL_A_FAVORED")),4)
    def test_favor_outgroup(self):self.assertEqual(independent_delta((Q(1),Q(1),Q(0),"B_INGROUP","EQUAL_TOTAL_A_FAVORED")),-4)
    def test_total_sacrifice(self):self.assertEqual(independent_delta((Q(1),Q(1),Q(0),"A_INGROUP","LOWER_TOTAL_A_FAVORED")),2)
    def test_inequity_tie(self):self.assertEqual(independent_delta((Q(1),Q(1),Q(1),"A_INGROUP","EQUAL_TOTAL_A_FAVORED")),0)
    def test_no_salience(self):self.assertEqual(independent_delta((Q(0),Q(1),Q(0),"A_INGROUP","EQUAL_TOTAL_A_FAVORED")),0)
    def test_deletion(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        rows=load();rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_bad_allocation(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["recipient_A_points"]="77"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_bad_label(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["ingroup_label"]="C_INGROUP"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_bad_utility(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["overall_utility"]="100"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_bad_choice(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["chosen_option"]="NOT_DEFINED"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_bad_sacrifice(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["aggregate_points_forgone"]="15"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_result_tamper(self):
        j=obj(RESULT);j["worlds"][0]["option_values"][0]["overall_utility"]="100"
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_summary_tamper(self):
        j=obj(RESULT);j["summary"]["lower_total_alternatives_chosen"]=40
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_digest_tamper(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"fake").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R304 source audit"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
