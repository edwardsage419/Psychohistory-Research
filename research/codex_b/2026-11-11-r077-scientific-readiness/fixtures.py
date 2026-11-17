"""Entirely artificial timelines, not qualified frozen-byte human datasets."""
from functools import lru_cache
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/codex_b/2026-11-10-r077-exact-score-candidate'))
import candidate
original=candidate.original
sys.path.insert(0,str(ROOT/'research/R073'))
from r073_human_ipd_memory_loso import validate_experiment


@lru_cache(maxsize=None)
def donor_fixture(kind):
    if kind not in ('identity','varied'):raise ValueError('UNKNOWN_SYNTHETIC_KIND')
    sessions={}
    for tr in ('fix','rand'):
        for session in range(6):
            size=12 if tr=='fix' and session==5 else 16
            def own(person,t):
                if kind=='identity':return int(t==100 and session==0 and person<(2 if tr=='fix' else 3))
                return int((person*5+t*3+t//7+session+(tr=='rand'))%11<4)
            players={}
            for person in range(size):
                history={}
                for t in range(1,101):
                    shift=t%size if tr=='rand' else 0
                    partner=(((person+shift)%size)^1)-shift
                    partner%=size
                    history[t]=(own(person,t),own(partner,t))
                players[f'ARTIFICIAL_PERSON_{person}']=history
            sessions[(tr,f'ARTIFICIAL_SESSION_{session}')]=players
    shape=validate_experiment(sessions)
    fit=original.build_source_donors(sessions)[original.SOURCE_DONOR]
    # Independent history construction: do not call original records/event helper.
    events=tuple((h[t-1][0],h[t-1][1],h[t-2][0],h[t-2][1],h[t][0])
                 for players in sessions.values() for h in players.values() for t in range(3,101))
    return fit,events,shape


def one_event_targets():
    return {f'ARTIFICIAL_TARGET_{tr}':{'treatment':tr,'events':[(0,0,0,0,0)]} for tr in (0,1)}


def count_shaped_targets():
    out={}
    for i in range(15):
        events=[]
        for j in range(74 if i==14 else 69):
            k=(j//2+i)%16
            events.append(((k>>3)&1,(k>>2)&1,(k>>1)&1,k&1,(j+i)%2))
        out[f'ARTIFICIAL_TARGET_{i:02}']={'treatment':int(i>=7),'events':events}
    return out


def small_identity_fixture():
    source=((0,0,0,0,1),)+((0,0,0,0,0),)*8
    fit={'train_only_prevalence':1/9,'train_target_count':9,'source_sessions':1,
         'state_counts':{name:{(0,)*width:(1,9)} for name,width in zip(original.MODEL_NAMES[1:5],(1,1,2,4))}}
    return fit,source
