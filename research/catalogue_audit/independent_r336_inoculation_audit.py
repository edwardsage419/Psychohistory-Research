"""R336 independent arithmetic replay, without production import."""
import csv
import io
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"R336"
HEADER=["mode","weak","refutation","same_topic","attack_intensity","policy","defense","baseline_post","post_belief","retained_gain"]
EXPECTED={"worlds":48,"rows":96,"same_topic_agreement":24,"novel_transfer_advantage":4,"no_weak_equal_baseline":24,"no_refutation_equal_baseline":24}
def independent_expected():
    rows,worlds=[],[]
    tally={k:0 for k in EXPECTED}
    for i in range(48):
        a=1+i%2
        s=i//2%2
        r=i//4%2
        w=i//8%2
        m=i//16
        valid=(m>0 and w==1 and r==1)
        ds={0:0,1:2,2:3}[m] if valid else 0
        dn={0:0,1:1,2:2}[m] if valid else 0
        d=ds if s else dn
        c=d if s else 0
        b=6-2*a
        t=6-max(0,2*a-d)
        u=6-max(0,2*a-c)
        worlds.append({"mode":m,"weak":w,"refutation":r,"same_topic":s,"attack_intensity":a,"baseline_post":b,"transfer_post":t,"support_post":u,"transfer_defense":d,"support_defense":c})
        rows.extend([[m,w,r,s,a,"INOCULATION_TRANSFER",d,b,t,t-b],[m,w,r,s,a,"TOPIC_SPECIFIC_SUPPORT",c,b,u,u-b]])
        tally["worlds"]+=1
        tally["rows"]+=2
        tally["same_topic_agreement"]+=int(bool(s) and t==u)
        tally["novel_transfer_advantage"]+=int(not s and t>u)
        tally["no_weak_equal_baseline"]+=int(not w and t==b and u==b)
        tally["no_refutation_equal_baseline"]+=int(not r and t==b and u==b)
    assert tally==EXPECTED
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return out.getvalue().encode(),(json.dumps({"schema":"R336_frozen_inoculation_transfer_v1","conditions":worlds,"checks":tally},indent=2,ensure_ascii=True)+"\n").encode()
def validate(source,result):
    expected_source,expected_result=independent_expected()
    assert source==expected_source,"independent CSV mismatch"
    assert result==expected_result,"independent JSON mismatch"
if __name__=="__main__":
    source=(BASE/"R336_ALL_96_ARTIFICIAL_ATTACK_ATOMS.csv").read_bytes()
    result=(BASE/"R336_EXACT_48_CONDITIONS.json").read_bytes()
    validate(source,result)
    tamper=0
    for sc,jc in ((source.replace(b"INOCULATION_TRANSFER",b"INOCULATION_FAKE",1),result),
                  (source,result.replace(b'"transfer_post": 4',b'"transfer_post": 99',1))):
        try:validate(sc,jc)
        except AssertionError:tamper+=1
    assert tamper==2
    print("R336 INDEPENDENT_AUDIT_PASS 48 worlds 96 rows 2 tamper rejections")
