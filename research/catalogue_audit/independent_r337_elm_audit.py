"""R337 independent no-import finite model audit and negative tamper controls."""
import csv
import io
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"R337"
HEADER=["involvement","ability","argument_quality","source_cue","cue_visible","policy","central_gate","score"]
EXPECTED={"worlds":32,"rows":64,"central_worlds":8,"other_worlds":24,"low_no_cue_zero":12,"quality_pairs_central":4,"quality_pairs_low":12,"cue_pairs_central":2,"cue_pairs_low":6,"agreement":2,"disagreement":30}
def reconstruct():
    rows,worlds=[],[]
    stats={k:0 for k in EXPECTED}
    for n in range(32):
        c=n%2
        e=2*(n//2%2)-1
        q=2*(n//4%2)-1
        b=n//8%2
        i=n//16
        g=int(i==1 and b==1)
        route=2*q if g else e*c
        fixed=q+e*c
        worlds.append({"involvement":i,"ability":b,"argument_quality":q,"source_cue":e,"cue_visible":c,"central_gate":g,"route_score":route,"fixed_score":fixed})
        rows.extend([[i,b,q,e,c,"ROUTE_GATE",g,route],[i,b,q,e,c,"FIXED_ADDITIVE",g,fixed]])
        stats["worlds"]+=1
        stats["rows"]+=2
        stats["central_worlds"]+=g
        stats["other_worlds"]+=1-g
        stats["low_no_cue_zero"]+=int(g==0 and c==0 and route==0)
        stats["quality_pairs_central"]+=int(q==1 and g==1)
        stats["quality_pairs_low"]+=int(q==1 and g==0)
        stats["cue_pairs_central"]+=int(e==1 and c==1 and g==1)
        stats["cue_pairs_low"]+=int(e==1 and c==1 and g==0)
        stats["agreement"]+=int(route==fixed)
        stats["disagreement"]+=int(route!=fixed)
    assert stats==EXPECTED
    stream=io.StringIO(newline="")
    writer=csv.writer(stream,lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return stream.getvalue().encode(),(json.dumps({"schema":"R337_frozen_binary_route_gate_v1","conditions":worlds,"checks":stats},indent=2,ensure_ascii=True)+"\n").encode()
def check(source,result):
    s,r=reconstruct()
    assert source==s,"CSV mismatch"
    assert result==r,"JSON mismatch"
if __name__=="__main__":
    s=(ROOT/"R337_ALL_64_ARTIFICIAL_ARGUMENT_CUE_ATOMS.csv").read_bytes()
    r=(ROOT/"R337_EXACT_32_CONDITIONS.json").read_bytes()
    check(s,r)
    rejected=0
    for a,b in ((s.replace(b"ROUTE_GATE",b"ROUTE_FAKE",1),r),(s,r.replace(b'"route_score": -2',b'"route_score": 99',1))):
        try:check(a,b)
        except AssertionError:rejected+=1
    assert rejected==2
    print("R337 INDEPENDENT_AUDIT_PASS 32 worlds 64 artificial atoms two tamper rejections")
