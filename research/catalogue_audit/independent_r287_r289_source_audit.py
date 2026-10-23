#!/usr/bin/env python3
"""Independent source CSV and theory auditor, without importing research models."""
import argparse,csv,hashlib,itertools,json
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1]
Z,O=F(0),F(1)
def load(tag,csvname,resultname):
    base=R/tag;src=base/csvname;output=base/resultname
    rows=list(csv.DictReader(src.open(encoding="utf-8",newline="")))
    result=json.loads(output.read_text(encoding="utf-8"))
    receipt=json.loads((base/(tag+"_MACHINE_RECEIPT.json")).read_text())
    for name,key in ((src,"source_sha256"),(output,"result_sha256" if tag=="R287" else "results_sha256")):
        assert hashlib.sha256(name.read_bytes()).hexdigest()==receipt[key],(tag,key)
    return rows,result,receipt
def r287():
    rows,result,receipt=load("R287","R287_ALL_2304_ORIGINAL_COMMON_CONSEQUENCE_SOURCES.csv","R287_EXACT_EU_RESULTS.json")
    util={"LINEAR":{0:F(0),1:F(1),4:F(4),9:F(9)},
          "SQRT_ON_SQUARES":{0:F(0),1:F(1),4:F(2),9:F(3)},
          "SATURATING":{0:F(0),1:F(1),4:F(3,2),9:F(2)}}
    bits={''.join(q) for q in itertools.product("01",repeat=8)}
    groups=defaultdict(list)
    for row in rows:groups[(row["utility_profile"],row["lambda_common"])].append(row)
    assert len(rows)==2304 and len(groups)==len(result["results"])==9
    assert receipt["prescore_freeze_commit"]=="524211361d5180624d4350559d53112de31139ab"
    for (n,lstr),items in groups.items():
        l=F(lstr);u=util[n]
        assert len(items)==256 and {x["full_ordered_M1X1_M2X2_M3X3_M4X4"] for x in items}==bits
        mass_sum=a=b=F(0)
        for row in items:
            s=row["full_ordered_M1X1_M2X2_M3X3_M4X4"]
            m=sum(int(s[2*k]) for k in range(4))
            w=l**m*(1-l)**(4-m)*F(1,16)
            ap=[1 if s[2*k]=="1" else 4 for k in range(4)]
            bp=[1 if s[2*k]=="1" else (9 if s[2*k+1]=="1" else 0) for k in range(4)]
            ea=sum((u[x] for x in ap),F(0))/4
            eb=sum((u[x] for x in bp),F(0))/4
            assert F(row["source_probability"])==w
            assert row["actual_payoffs_A"]==";".join(map(str,ap))
            assert row["actual_payoffs_B"]==";".join(map(str,bp))
            assert (F(row["realized_mean_utility_A"]),F(row["realized_mean_utility_B"]),
                    F(row["realized_mean_difference_A_minus_B"]))==(ea,eb,ea-eb)
            mass_sum+=w;a+=w*ea;b+=w*eb
        assert mass_sum==1
        theory_a=(1-l)*u[4]+l*u[1]
        theory_b=(1-l)*(u[0]+u[9])/2+l*u[1]
        assert (a,b)==(theory_a,theory_b)
        v=next(x for x in result["results"] if x["profile"]==n and x["lambda_common"]==lstr)
        assert (v["expected_utility_A"],v["expected_utility_B"],v["EU_difference_A_minus_B"],
           v["affine_transformed_difference"])==tuple(map(str,(a,b,a-b,3*(a-b))))
    assert result["no_real_human_E2"]==result["no_real_historical_E3"]==0
    return "R287_COMPLETE_2304_EU_COMMON_CONSEQUENCE_INDEPENDENT_PASS"
def r288():
    rows,result,receipt=load("R288","R288_ALL_576_ORIGINAL_REFERENCE_LOSS_SOURCES.csv","R288_EXACT_REFERENCE_RESULTS.json")
    assert len(rows)==576 and len(result["result"])==9
    assert receipt["freeze_commit"]=="d94d9d7f275082a6672fbea0e191ac76a54bed87"
    groups=defaultdict(list);bits={''.join(q) for q in itertools.product("01",repeat=6)}
    for row in rows:groups[(int(row["reference"]),int(row["loss_multiplier"]))].append(row)
    assert len(groups)==9
    def v(x,ref,L):
        diff=F(x-ref)
        return diff if diff>=0 else L*diff
    for (ref,L),items in groups.items():
        assert len(items)==64 and {x["ordered_all_six_independent_fair_gamble_bits"] for x in items}==bits
        mass=G=S=F(0)
        for row in items:
            src=row["ordered_all_six_independent_fair_gamble_bits"]
            pay=[3 if x=="1" else -2 for x in src]
            val=[v(x,ref,L) for x in pay]
            g=sum(val,F(0))/6;s=v(0,ref,L)
            assert F(row["source_probability"])==F(1,64)
            assert row["realized_gamble_payoffs"]==";".join(map(str,pay))
            assert row["realized_gamble_reference_values"]==";".join(map(str,val))
            assert (F(row["realized_mean_gamble_reference_value"]),F(row["sure_zero_reference_value"]),
             F(row["realized_mean_gamble_minus_sure"]))==(g,s,g-s)
            mass+=F(1,64);G+=g/64;S+=s/64
        assert mass==1
        assert (G,S)==((v(3,ref,L)+v(-2,ref,L))/2,v(0,ref,L))
        entry=next(x for x in result["result"] if x["reference"]==ref and x["loss_multiplier"]==L)
        assert (entry["exact_expected_gamble_value"],entry["exact_sure_reference_value"],
                entry["exact_gamble_minus_sure"])==tuple(map(str,(G,S,G-S)))
    assert result["human_E2"]==result["historical_E3"]==0
    return "R288_COMPLETE_576_REFERENCE_LOSS_ORIGINAL_SOURCES_INDEPENDENT_PASS"
def r289():
    rows,result,receipt=load("R289","R289_ALL_486_ORIGINAL_SEQUENTIAL_OFFER_SOURCES.csv","R289_EXACT_SATISFICING_RESULTS.json")
    assert len(rows)==486 and len(result["worlds"])==6
    assert receipt["freeze_commit"]=="27fa695d5e0c612fd77fb3a3fc5af26a543c0a27"
    dgp={"UNIFORM":(F(1,3),F(1,3),F(1,3)),
         "LOW_HEAVY":(F(1,2),F(1,4),F(1,4)),
         "HIGH_HEAVY":(F(1,4),F(1,4),F(1,2))}
    space={''.join(map(str,v)) for v in itertools.product((1,3,5),repeat=4)}
    groups=defaultdict(list)
    for row in rows:groups[(row["distribution"],int(row["aspiration"]))].append(row)
    assert len(groups)==6
    for (name,asp),items in groups.items():
        assert len(items)==81 and {x["complete_ordered_four_offer_source"] for x in items}==space
        p=dict(zip((1,3,5),dgp[name]))
        total=F(0);moments=[F(0)]*5
        for row in items:
            vals=tuple(map(int,row["complete_ordered_four_offer_source"]))
            prob=F(1)
            for x in vals:prob*=p[x]
            index=next((i for i,x in enumerate(vals,1) if x>=asp),4)
            selected=vals[index-1]
            net=F(selected)-F(index-1,2)
            values=(net,index,vals[0],max(vals),int(selected<asp))
            assert row["world"]==name+"_"+str(asp)
            assert F(row["complete_source_probability"])==prob
            assert (int(row["stopped_at_offer_index"]),int(row["observed_offer_count"]))==(index,index)
            assert (int(row["chosen_payoff"]),int(row["aspiration_met"]))==(selected,int(selected>=asp))
            assert (F(row["search_cost"]),F(row["net_payoff"]))==(F(index-1,2),net)
            assert (int(row["first_offer_only_payoff"]),
              int(row["infeasible_full_future_information_maximum_payoff"]))==(vals[0],max(vals))
            total+=prob
            for i,x in enumerate(values):moments[i]+=prob*x
        assert total==1
        q=sum((prob for x,prob in p.items() if x<asp),F(0))
        hitpay=sum((prob*x for x,prob in p.items() if x>=asp),F(0))
        mu=sum((prob*x for x,prob in p.items()),F(0))
        count=1+q+q*q+q**3
        expected=(hitpay*(1+q+q*q)+q**3*mu)-F(1,2)*(count-1)
        oracle=1+2*(1-p[1]**4)+2*(1-(p[1]+p[3])**4)
        assert moments==[expected,count,mu,oracle,q**4]
        entry=next(x for x in result["worlds"] if x["distribution"]==name and x["aspiration"]==asp)
        keys=("expected_net_payoff","expected_observed_offers","first_offer_baseline_mean",
              "nondeployable_perfect_foresight_max_mean","probability_aspiration_never_met")
        assert [entry[k] for k in keys]==list(map(str,moments))
    assert result["E2_human"]==result["E3_historical"]==0
    return "R289_COMPLETE_486_SATISFICING_SEQUENTIAL_SOURCES_INDEPENDENT_PASS"
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--research",choices=["R287","R288","R289"],required=True)
    target=parser.parse_args().research
    print({"R287":r287,"R288":r288,"R289":r289}[target]())
