"""Independent oriented-event exact R169 audit, Python standard library only.
No reuse of main step() or trajectory(); import only for result comparison.
"""
from fractions import Fraction as Q
from collections import defaultdict
from itertools import product
import importlib.util, json, pathlib

ROOT=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('r169_main',ROOT.parent/'validation'/'r169_observation_ladder_20261026.py')
main=importlib.util.module_from_spec(spec);spec.loader.exec_module(main)

def alternate_kernel(state,alpha,mode):
    edge_list,values=state
    orientations=[(i,j) for i,j in edge_list if values[i]!=values[j]] + [(j,i) for i,j in edge_list if values[i]!=values[j]]
    if len(orientations)==0:return {state:Q(1)}
    masses=defaultdict(Q)
    for i,j in orientations:
        atom=Q(1,len(orientations))
        changed=tuple(values[k] if k!=i else values[j] for k in range(4))
        masses[(edge_list,changed)]+=atom*(1-alpha)
        current_neighbors=[]
        for a,b in edge_list:
            if a==i:current_neighbors.append(b)
            if b==i:current_neighbors.append(a)
        targets=[]
        for k in range(4):
            if k==i or k==j or k in current_neighbors:continue
            if mode=='same' and values[k]!=values[i]:continue
            targets.append(k)
        if targets:
            for k in targets:
                replacement=tuple(sorted([tuple(sorted(pair)) for pair in edge_list if set(pair)!={i,j}] + [tuple(sorted((i,k)))]))
                masses[(replacement,values)]+=atom*alpha/Q(len(targets))
        else:masses[state]+=atom*alpha
    return {key:v for key,v in masses.items() if v!=0}

def alternate_path(state,alpha,mode):
    current={state:Q(1)};result=[current]
    for time in range(3):
        next_=defaultdict(Q)
        for key,prob in current.items():
            for new_key,weight in alternate_kernel(key,alpha,mode).items():next_[new_key]+=prob*weight
        current={k:v for k,v in next_.items() if v!=0}
        result.append(current)
    return result

def main_audit():
    worlds=0;matched=0;matched_snapshots=0;kernel_states=0;negative_checks=0
    for edges in main.GRAPHS.values():
        for values in main.OPINIONS.values():
            initial=(edges,values)
            for alpha,mode in product(main.ALPHAS,main.MODES):
                worlds+=1
                a=main.trajectory(initial,alpha,mode)
                b=alternate_path(initial,alpha,mode)
                assert len(a)==len(b)==4
                for x,y in zip(a,b):
                    assert x==y,(initial,alpha,mode)
                    matched_snapshots+=1
                    for state in x:
                        assert main.step(state,alpha,mode)==alternate_kernel(state,alpha,mode)
                        kernel_states+=1
                matched+=1
    initial=(main.GRAPHS['path'],main.OPINIONS['block'])
    right=alternate_kernel(initial,Q(1),'any')
    wrong={initial:Q(1)}
    mutation_distance=sum((abs(right.get(s,Q(0))-wrong.get(s,Q(0))) for s in set(right)|set(wrong)),Q(0))/2
    assert mutation_distance>0
    negative_checks+=1
    same=alternate_path(initial,Q(1),'same')[2]; any_=alternate_path(initial,Q(1),'any')[2]
    tv=sum((abs(same.get(s,Q(0))-any_.get(s,Q(0))) for s in set(same)|set(any_)),Q(0))/2
    assert tv==Q(1,2)
    return {'audit':'R169 independent oriented-event algorithm','worlds':worlds,'full_snapshot_equalities':matched_snapshots,
      'individual_reachable_kernel_equalities':kernel_states,'all_worlds_matched':matched,
      'executed_mutant_noop_TV':str(mutation_distance),'negative_controls_passed':negative_checks,
      'original_R169_TV2_recomputed':str(tv),'method':'independent oriented-edge enumeration and propagation',
      'evidence':'INTERNAL_INDEPENDENT_METHOD_E1','external_research_team':False}

if __name__=='__main__':print(json.dumps(main_audit(),indent=2,sort_keys=True))
