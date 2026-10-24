"""R334 independent no-import exact source auditor and negative controls."""
import csv
import io
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R334"
SOURCE=ROOT/"R334_ALL_48_ARTIFICIAL_CONTRAST_ATOMS.csv"
RESULT=ROOT/"R334_EXACT_16_CONDITIONS.json"

def expected():
    entries,summary=[],[]
    for a in [-1,1]:
        for b in [-1,1]:
            for reward in [1,3]:
                for agency in [0,1]:
                    inconsistent=int(a*b==-1)
                    adjustment=Q(agency*inconsistent,reward+1)
                    final_d=Q(a)*(1-adjustment)+Q(b)*adjustment
                    final_i=Q(a)*(1-adjustment*reward)+Q(b)*adjustment*reward
                    entries.extend([
                        ["DISSONANCE",a,b,reward,agency,inconsistent,str(adjustment),str(final_d)],
                        ["RESPONSE_DEMAND",a,b,reward,agency,inconsistent,"0",str(final_d)],
                        ["INCENTIVE",a,b,reward,agency,inconsistent,"0",str(final_i)]
                    ])
                    summary.append(dict(a=a,b=b,j=reward,c=agency,post_dissonance=str(final_d),
                        post_response_demand=str(final_d),post_incentive=str(final_i),
                        strain_dissonance=str(adjustment),strain_response_demand="0",strain_incentive="0"))
    assert len(entries)==48 and len(summary)==16
    def cond(a,b,j):
        return next(s for s in summary if (s["a"],s["b"],s["j"],s["c"])==(a,b,j,1))
    low=sum(abs(Q(cond(a,-a,1)["post_dissonance"])-a)>abs(Q(cond(a,-a,3)["post_dissonance"])-a) for a in [-1,1])
    high=sum(abs(Q(cond(a,-a,1)["post_incentive"])-a)<abs(Q(cond(a,-a,3)["post_incentive"])-a) for a in [-1,1])
    checks=dict(rows=48,conditions=16,
        unchanged_conditions=sum((s["c"]==0 or s["a"]==s["b"]) and s["post_dissonance"]==str(s["a"]) and s["post_incentive"]==str(s["a"]) for s in summary),
        identical_reports=sum(s["post_dissonance"]==s["post_response_demand"] for s in summary),
        latent_strain_disagreements=sum(s["strain_dissonance"]!="0" for s in summary),
        low_justification_larger_dissonance_shifts=low,
        high_justification_larger_incentive_shifts=high)
    buff=io.StringIO(newline="")
    writer=csv.writer(buff,lineterminator="\\r\\n")
    writer.writerow(["model","a","b","j","c","m","latent_strain","post_attitude"])
    writer.writerows(entries)
    obj=dict(schema="R334_frozen_induced_compliance_v1",conditions=summary,checks=checks)
    return buff.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=False)+"\\n").encode(),checks

def validate(cb,jb):
    a,b,checks=expected()
    assert cb==a,"R334 CSV tampering detected"
    assert jb==b,"R334 JSON tampering detected"
    assert checks==dict(rows=48,conditions=16,unchanged_conditions=12,identical_reports=16,
        latent_strain_disagreements=4,low_justification_larger_dissonance_shifts=2,
        high_justification_larger_incentive_shifts=2)

if __name__=="__main__":
    cb,jb=SOURCE.read_bytes(),RESULT.read_bytes()
    validate(cb,jb)
    changed=cb.replace(b"DISSONANCE,-1,-1,1,0,0,0,-1",b"DISSONANCE,-1,-1,1,0,0,0,1",1)
    assert changed!=cb
    try:
        validate(changed,jb)
        raise RuntimeError("CSV negative control passed")
    except AssertionError as e:
        assert "CSV tampering" in str(e)
    obj=json.loads(jb)
    obj["conditions"][0]["post_dissonance"]="0"
    bad=(json.dumps(obj,indent=2,ensure_ascii=False)+"\\n").encode()
    assert bad!=jb
    try:
        validate(cb,bad)
        raise RuntimeError("JSON negative control passed")
    except AssertionError as e:
        assert "JSON tampering" in str(e)
    print("R334 INDEPENDENT_PASS 48 atoms 16 conditions six falsifiers two tamper rejections")
