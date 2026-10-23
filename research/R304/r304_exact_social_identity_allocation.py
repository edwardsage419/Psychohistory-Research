#!/usr/bin/env python3
"""R304 exact project-specific minimal-group allocation preference toy; NOT Tajfel author-fitted model."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="60f6406cede7eb5bb7cea9dc622835d8fe3f4c41"
Z,O=F(0),F(1)
LEVELS=(Z,F(1,2),O)
LABELS=("A_INGROUP","B_INGROUP")
MENUS={"EQUAL_TOTAL_A_FAVORED":(10,6),"EQUAL_TOTAL_B_FAVORED":(6,10),
       "LOWER_TOTAL_A_FAVORED":(9,3),"LOWER_TOTAL_B_FAVORED":(3,9)}
OPTIONS=("BASE","ALTERNATIVE")
BASE=(8,8)
WORLDS=tuple(itertools.product(LEVELS,LEVELS,LEVELS,LABELS,tuple(MENUS)))
SOURCE_NAME="R304_ALL_432_ORIGINAL_MINIMAL_GROUP_ALLOCATION_OPTIONS.csv"
RESULT_NAME="R304_EXACT_SOCIAL_IDENTITY_ALLOCATION_RESULTS.json"
RECEIPT_NAME="R304_MACHINE_RECEIPT.json"

def world_id(s,d,e,label,menu):
    return f"salience={s}|differentiation={d}|inequity={e}|label={label}|menu={menu}"

def allocation_score(s,d,e,label,allocation):
    if s not in LEVELS or d not in LEVELS or e not in LEVELS or label not in LABELS:raise ValueError("frozen parameters only")
    a,b=allocation
    group_delta=(a-b) if label=="A_INGROUP" else (b-a)
    inequality=abs(a-b)
    total=a+b
    bonus=s*d*group_delta
    penalty=e*inequality
    return {"recipient_A_points":a,"recipient_B_points":b,"total_points":total,
            "ingroup_recipient":"A" if label=="A_INGROUP" else "B",
            "outgroup_recipient":"B" if label=="A_INGROUP" else "A",
            "ingroup_points":a if label=="A_INGROUP" else b,
            "outgroup_points":b if label=="A_INGROUP" else a,
            "ingroup_minus_outgroup":group_delta,"absolute_inequality":inequality,
            "identity_utility_term":bonus,"inequality_penalty_term":penalty,
            "overall_utility":F(total)+bonus-penalty,"actor_personal_reward":0}

def evaluate(s,d,e,label,menu):
    if (s,d,e,label,menu) not in WORLDS:raise ValueError("world not frozen")
    eq=allocation_score(s,d,e,label,BASE)
    other=allocation_score(s,d,e,label,MENUS[menu])
    chosen="ALTERNATIVE" if other["overall_utility"]>eq["overall_utility"] else "BASE"
    chosen_total=other["total_points"] if chosen=="ALTERNATIVE" else eq["total_points"]
    total_max=max(eq["total_points"],other["total_points"])
    return {"BASE":eq,"ALTERNATIVE":other,"chosen_option":chosen,
       "tie_select_BASE":eq["overall_utility"]==other["overall_utility"],
       "choice_total_points":chosen_total,"max_total_points":total_max,
       "aggregate_points_forgone":total_max-chosen_total,
       "chosen_alt_lower_aggregate":chosen=="ALTERNATIVE" and chosen_total<total_max}

def row(s,d,e,label,menu,option):
    if option not in OPTIONS:raise ValueError("not frozen option")
    z=evaluate(s,d,e,label,menu)
    return {"world":world_id(s,d,e,label,menu),
       "identity_salience":s,"group_differentiation_weight":d,
       "inequality_aversion":e,"ingroup_label":label,"menu":menu,"option":option,
       **z[option],"chosen_option":z["chosen_option"],
       "tie_select_BASE":z["tie_select_BASE"],
       "choice_total_points":z["choice_total_points"],
       "aggregate_points_forgone":z["aggregate_points_forgone"],
       "chosen_alt_lower_aggregate":z["chosen_alt_lower_aggregate"]}

def sources():
    return tuple(row(*world,option) for world in WORLDS for option in OPTIONS)

def verify():
    assert len(WORLDS)==216 and len(sources())==432
    assert len({(x["world"],x["option"]) for x in sources()})==432
    alternate_worlds=[w for w in WORLDS if evaluate(*w)["chosen_option"]=="ALTERNATIVE"]
    assert len(alternate_worlds)==12
    assert sum(w[4].startswith("EQUAL_TOTAL") for w in alternate_worlds)==10
    assert sum(w[4].startswith("LOWER_TOTAL") for w in alternate_worlds)==2
    for s,d,e,label,menu in WORLDS:
        z=evaluate(s,d,e,label,menu)
        assert z["BASE"]["overall_utility"]==16
        assert z["actor_personal_reward"]==0 if "actor_personal_reward" in z else True
        alt=z["ALTERNATIVE"]
        target_delta=(alt["recipient_A_points"]-alt["recipient_B_points"]) if label=="A_INGROUP" else (alt["recipient_B_points"]-alt["recipient_A_points"])
        assert alt["overall_utility"]==alt["total_points"]+s*d*target_delta-e*abs(target_delta)
        assert z["aggregate_points_forgone"]>=0
        if s==Z or d==Z:
            assert z["chosen_option"]=="BASE"
            other_label="B_INGROUP" if label=="A_INGROUP" else "A_INGROUP"
            assert evaluate(s,d,e,other_label,menu)["chosen_option"]==z["chosen_option"]
            assert evaluate(s,d,e,other_label,menu)["ALTERNATIVE"]["overall_utility"]==z["ALTERNATIVE"]["overall_utility"]
        if z["chosen_alt_lower_aggregate"]:
            assert (s,d,e)==(O,O,Z) and menu.startswith("LOWER_TOTAL")
    assert evaluate(O,O,Z,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["ALTERNATIVE"]["overall_utility"]==20
    assert evaluate(O,O,Z,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"]=="ALTERNATIVE"
    assert evaluate(O,O,Z,"B_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"]=="BASE"
    assert evaluate(O,O,O,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["tie_select_BASE"]
    assert evaluate(O,O,O,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"]=="BASE"
    assert evaluate(O,O,Z,"A_INGROUP","LOWER_TOTAL_A_FAVORED")["ALTERNATIVE"]["overall_utility"]==18
    assert evaluate(O,O,Z,"A_INGROUP","LOWER_TOTAL_A_FAVORED")["aggregate_points_forgone"]==4
    return True

def emit():
    verify()
    cols=("world","identity_salience","group_differentiation_weight",
       "inequality_aversion","ingroup_label","menu","option",
       "recipient_A_points","recipient_B_points","total_points",
       "ingroup_recipient","outgroup_recipient","ingroup_points","outgroup_points",
       "ingroup_minus_outgroup","absolute_inequality","identity_utility_term",
       "inequality_penalty_term","overall_utility","actor_personal_reward",
       "chosen_option","tie_select_BASE","choice_total_points",
       "aggregate_points_forgone","chosen_alt_lower_aggregate")
    csv_path=ROOT/SOURCE_NAME
    with csv_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for source in sources():w.writerow({k:str(source[k]) for k in cols})
    data={"research_id":"R304","original_catalogue_id":"03-003","freeze_commit":FREEZE,
       "scope":"E1_PROJECT_CUSTOM_ARTIFICIAL_MINIMAL_GROUP_ALLOCATION_TOY_NOT_TAJFEL_FITTED_HUMAN_MODEL",
       "synthetic_worlds":216,"complete_option_source_rows":432,
       "social_identity_model_utility_invented_by_project":True,
       "original_1971_human_allocation_data_reanalyzed":False,
       "distinct_real_human_E2_added":0,"new_real_animal_E2":0,"historical_E3_added":0,
       "worlds":[],"R073":"FROZEN","PESEN_v0_1":"FROZEN"}
    for s,d,e,label,menu in WORLDS:
        x=evaluate(s,d,e,label,menu)
        data["worlds"].append({"world":world_id(s,d,e,label,menu),
          "identity_salience":str(s),"group_differentiation_weight":str(d),
          "inequality_aversion":str(e),"ingroup_label":label,"menu":menu,
          "chosen_option":x["chosen_option"],"tie_select_BASE":x["tie_select_BASE"],
          "choice_total_points":x["choice_total_points"],
          "aggregate_points_forgone":x["aggregate_points_forgone"],
          "chosen_alt_lower_aggregate":x["chosen_alt_lower_aggregate"],
          "original_source_rows":2,
          "option_values":[{key:str(row(s,d,e,label,menu,opt)[key]) for key in cols if key not in
                 ("world","identity_salience","group_differentiation_weight","inequality_aversion","ingroup_label","menu")} for opt in OPTIONS]})
    alts=[z for z in data["worlds"] if z["chosen_option"]=="ALTERNATIVE"]
    data["summary"]={"artificial_alternative_chosen_worlds":len(alts),
       "equal_total_alternatives_chosen":sum(x["menu"].startswith("EQUAL_TOTAL") for x in alts),
       "lower_total_alternatives_chosen":sum(x["menu"].startswith("LOWER_TOTAL") for x in alts),
       "identity_salience_zero_alternate_worlds":0,
       "no_difference_weight_alternate_worlds":0,
       "A_ingroup_s1_d1_e0_equal_total_A_alt_utility":"20",
       "A_ingroup_s1_d1_e0_lower_total_A_alt_utility":"18",
       "A_ingroup_s1_d1_e0_lower_total_A_total_forgone":4}
    result_path=ROOT/RESULT_NAME
    result_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt={"research_id":"R304","freeze_commit":FREEZE,"source_rows":432,
      "source_sha256":hashlib.sha256(csv_path.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest(),
      "new_E2":0,"new_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_full(self):self.assertTrue(verify())
    def test_world_count(self):self.assertEqual(len(WORLDS),216)
    def test_source_count(self):self.assertEqual(len(sources()),432)
    def test_label_favor(self):self.assertEqual(evaluate(O,O,Z,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"],"ALTERNATIVE")
    def test_label_reverse(self):self.assertEqual(evaluate(O,O,Z,"B_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"],"BASE")
    def test_lower_total(self):self.assertEqual(evaluate(O,O,Z,"A_INGROUP","LOWER_TOTAL_A_FAVORED")["aggregate_points_forgone"],4)
    def test_no_salience(self):self.assertEqual(evaluate(Z,O,Z,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"],"BASE")
    def test_no_bias_weight(self):self.assertEqual(evaluate(O,Z,Z,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"],"BASE")
    def test_equity_tie(self):self.assertEqual(evaluate(O,O,O,"A_INGROUP","EQUAL_TOTAL_A_FAVORED")["chosen_option"],"BASE")
    def test_no_direct_personal_reward(self):self.assertEqual(row(O,O,Z,"A_INGROUP","LOWER_TOTAL_A_FAVORED","ALTERNATIVE")["actor_personal_reward"],0)
    def test_bad_weight(self):
        with self.assertRaises(ValueError):evaluate(F(1,3),O,Z,"A_INGROUP","LOWER_TOTAL_A_FAVORED")
    def test_bad_label(self):
        with self.assertRaises(ValueError):evaluate(O,O,Z,"NO_GROUP","LOWER_TOTAL_A_FAVORED")
    def test_bad_menu(self):
        with self.assertRaises(ValueError):evaluate(O,O,Z,"A_INGROUP","WRONG")
    def test_bad_option(self):
        with self.assertRaises(ValueError):row(O,O,Z,"A_INGROUP","LOWER_TOTAL_A_FAVORED","D")

def add_case(world,option,kind):
    def f(self):
        src=row(*world,option)
        v=evaluate(*world)
        if kind=="score":self.assertEqual(src["overall_utility"],v[option]["overall_utility"])
        elif kind=="choice":self.assertEqual(src["chosen_option"],v["chosen_option"])
        elif kind=="regret":self.assertEqual(src["aggregate_points_forgone"],v["aggregate_points_forgone"])
        else:raise AssertionError(kind)
    return f
for i,w in enumerate(WORLDS):
    for option in OPTIONS:
        for kind in ("score","choice","regret"):
            setattr(Tests,f"test_world{i}_{option}_{kind}",add_case(w,option,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R304"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
