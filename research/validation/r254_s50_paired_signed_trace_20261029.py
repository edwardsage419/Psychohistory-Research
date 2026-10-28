#!/usr/bin/env python3
"""R254 S50 E1: frozen half-ER positive vs signed triangle, exact paired source audit.
No external packages or data required. Reconstructs frozen six-edge-bit and three-seed-bit universe.
This does not constitute a byte-level audit of the original GitHub CSV.
"""
import itertools, json, collections, hashlib
from fractions import Fraction
from pathlib import Path

BIT6=itertools.product((0,1),repeat=6)
SEEDS=list(itertools.product((0,1),repeat=3))

def edge(bits,signed):
    e=tuple(int(2*bits[i]+bits[i+1]<2) for i in (0,2,4))
    return e[:2]+((-e[2] if signed else e[2]),)

def matrix(e):
    a,b,c=e
    return ((0,a,b),(a,0,c),(b,c,0))

def matmul(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))

def mv(A,v):
    return tuple(sum(A[i][j]*v[j] for j in range(3)) for i in range(3))

def trace(M):
    return sum(M[i][i] for i in range(3))

def states(A,seed):
    out=[seed]
    for _ in range(3):out.append(mv(A,out[-1]))
    return out

def calculate():
    total=0; same_rho2=0; same_even2=0; same_even4=0; odd_nonzero=0
    mismatches=[0]*4; edge_masks=collections.Counter(); moment_sum={k:[0,0] for k in (2,3,4)}
    first_step_condition_ok=0; first_step_condition_mismatches=0
    for bits in BIT6:
        ep=edge(bits,False); en=edge(bits,True)
        Ap=matrix(ep); An=matrix(en)
        powp={1:Ap};pown={1:An}
        for k in (2,3,4):
            powp[k]=matmul(powp[k-1],Ap)
            pown[k]=matmul(pown[k-1],An)
        tp={k:trace(powp[k]) for k in (2,3,4)}
        tn={k:trace(pown[k]) for k in (2,3,4)}
        rho2p=sum(x*x for x in ep)+(1 if all(ep) else 0)
        rho2n=sum(x*x for x in en)+(1 if all(en) else 0)
        for seed in SEEDS:
            total+=1
            edge_masks[''.join(map(str,map(abs,ep)))]+=1
            same_rho2+=rho2p==rho2n
            same_even2+=tp[2]==tn[2]
            same_even4+=tp[4]==tn[4]
            odd_nonzero+=tp[3]!=tn[3]
            for k in (2,3,4):
                moment_sum[k][0]+=tp[k]
                moment_sum[k][1]+=tn[k]
            sp=states(Ap,seed);sn=states(An,seed)
            for t in range(4):mismatches[t]+=sp[t]!=sn[t]
            cond=(ep[2]!=0 and (seed[1]!=0 or seed[2]!=0))
            first_step_condition_ok+=(sp[1]!=sn[1])==cond
            first_step_condition_mismatches+=bool(cond)
    assert total==512
    assert same_rho2==same_even2==same_even4==512
    assert odd_nonzero==64
    assert mismatches[0]==0 and mismatches[1]==first_step_condition_mismatches==192
    assert first_step_condition_ok==512
    means={str(k):{'positive':str(Fraction(v[0],total)),'signed':str(Fraction(v[1],total)),'positive_minus_signed':str(Fraction(v[0]-v[1],total))} for k,v in moment_sum.items()}
    assert means['3']=={'positive':'3/4','signed':'-3/4','positive_minus_signed':'3/2'}
    assert means['2']['positive']==means['2']['signed']
    assert means['4']['positive']==means['4']['signed']
    assert sum(edge_masks.values())==512
    return dict(research_id='R254_S50',evidence='E1_FINITE_ARTIFICIAL',
      independent_edge_seed_pairs=total, time_points=4, original_source_full_byte_audit='NOT_PERFORMED',
      same_rho_squared_pairs=same_rho2,same_trace_A2_pairs=same_even2,same_trace_A4_pairs=same_even4,
      different_trace_A3_pairs=odd_nonzero,
      trace_moments=means, paired_vector_mismatch_count_by_n=mismatches,
      paired_vector_equal_count_by_n=[total-x for x in mismatches],
      paired_vector_mismatch_probability_by_n=[str(Fraction(x,total)) for x in mismatches],
      n1_analytic_condition_matches=first_step_condition_ok,
      edge_mask_counts=dict(sorted(edge_masks.items())),
      new_real_human_E2=0,new_real_historical_E3=0,external_independent_replication=0,
      R073='FROZEN',PESEN_v0_1='FROZEN')

if __name__=='__main__':
    result=calculate()
    out=Path(__file__).with_name('R254_S50_PAIRED_SIGNED_TRACE_RECEIPT_2026-10-29.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    print('receipt_sha256',hashlib.sha256(out.read_bytes()).hexdigest())
