"""R333 independent replay; never imports the production module."""
import csv, io, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R333"
C=ROOT/"R333_ALL_160_ARTIFICIAL_TRIADIC_STATES.csv"
J=ROOT/"R333_EXACT_32_TRIADIC_WORLDS.json"
HEADER=["mechanism","initial_p","initial_b","initial_e","do_b1","time","p","b","e"]

def expected():
    rows,worlds,seqs=[],[],{}
    for model in ("cyclic","feedforward"):
        for state in range(8):
            p0=(state>>2)&1
            b0=(state>>1)&1
            e0=state&1
            for d in range(2):
                p,b,e=p0,b0,e0
                seq=[(p,b,e)]
                for t in range(1,5):
                    pp=int(p!=e)
                    bb=int(p!=b)
                    ee=int(b!=e) if model=="cyclic" else e
                    p,b,e=pp,(d if t==1 else bb),ee
                    seq.append((p,b,e))
                seqs[(model,state,d)]=seq
                for t,(pp,bb,ee) in enumerate(seq):
                    rows.append([model,p0,b0,e0,d,t,pp,bb,ee])
                worlds.append(dict(mechanism=model,initial_p=p0,initial_b=b0,initial_e=e0,do_b1=d,final_p=p,final_b=b,final_e=e))
    checks=dict(equal_b1=0,different_p2=0,different_b3=0,cyclic_e2_do=0,feedforward_e2_do=0)
    for state in range(8):
        c0=seqs[("cyclic",state,0)]
        c1=seqs[("cyclic",state,1)]
        f0=seqs[("feedforward",state,0)]
        f1=seqs[("feedforward",state,1)]
        checks["cyclic_e2_do"]+=c0[2][2]!=c1[2][2]
        checks["feedforward_e2_do"]+=f0[2][2]!=f1[2][2]
        for c,f in ((c0,f0),(c1,f1)):
            checks["equal_b1"]+=c[1][1]==f[1][1]
            checks["different_p2"]+=c[2][0]!=f[2][0]
            checks["different_b3"]+=c[3][1]!=f[3][1]
    stream=io.StringIO(newline="")
    writer=csv.writer(stream,lineterminator="\r\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    obj=dict(schema="R333_frozen_triads_v1",worlds=worlds,checks=checks)
    return stream.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=False)+"\n").encode(),checks

def validate(csv_bytes,json_bytes):
    ec,ej,checks=expected()
    assert csv_bytes==ec,"source tampering detected"
    assert json_bytes==ej,"world tampering detected"
    assert checks==dict(equal_b1=16,different_p2=8,different_b3=8,cyclic_e2_do=8,feedforward_e2_do=0)

if __name__=="__main__":
    cb,jb=C.read_bytes(),J.read_bytes()
    validate(cb,jb)
    changed=cb.replace(b"cyclic,0,0,0,0,0,0,0,0",b"cyclic,0,0,0,0,0,1,0,0",1)
    assert changed!=cb
    try:
        validate(changed,jb)
        raise RuntimeError("CSV tampering accepted")
    except AssertionError as ex:
        assert "source tampering detected" in str(ex)
    obj=json.loads(jb)
    obj["worlds"][0]["final_p"]=1-obj["worlds"][0]["final_p"]
    changed_j=(json.dumps(obj,indent=2,ensure_ascii=False)+"\n").encode()
    try:
        validate(cb,changed_j)
        raise RuntimeError("world tampering accepted")
    except AssertionError as ex:
        assert "world tampering detected" in str(ex)
    print("R333 INDEPENDENT_AUDIT_PASS 160 rows 32 worlds 5 falsifiers two tamper rejections")
