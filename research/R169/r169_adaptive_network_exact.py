"""R169 exact finite four-node cultural-opinion / contact-graph coevolution.

Project-authored active-discordant-edge Markov process, not a reproduction of
the Holme-Newman original event clock or Vazquez infinite-network transition.
No empirical human network, attitude or historical event observations.
"""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction as F
import json

N=4
GRAPHS=(
 ("path",((0,1),(1,2),(2,3))),
 ("star",((0,1),(0,2),(0,3))),
 ("cycle",((0,1),(0,3),(1,2),(2,3))),
 ("chord",((0,1),(0,2),(1,2),(2,3))),
)
OPINIONS=(
 ("block",(0,0,1,1)),
 ("alternate",(0,1,0,1)),
 ("singleton",(0,0,0,1)),
)
ALPHAS=(F(0),F(1,2),F(1))
MODES=("same","any")
HORIZON=3


def normalized_state(edges,opinions):
    if not isinstance(opinions,(tuple,list)) or len(opinions)!=N or any(
        type(x) is not int or x not in (0,1) for x in opinions):
        raise ValueError("exactly four binary cultural states required")
    if not isinstance(edges,(tuple,list)):
        raise ValueError("undirected edge collection must be tuple/list")
    seen=set()
    for edge in edges:
        if not isinstance(edge,(tuple,list)) or len(edge)!=2:
            raise ValueError("invalid undirected edge")
        i,j=edge
        if type(i) is not int or type(j) is not int or not (0<=i<N and 0<=j<N) or i==j:
            raise ValueError("bad endpoint or self-link")
        pair=(min(i,j),max(i,j))
        if pair in seen:raise ValueError("duplicate edge")
        seen.add(pair)
    return tuple(sorted(seen)),tuple(opinions)


def checked_controls(alpha,mode):
    if isinstance(alpha,bool) or not isinstance(alpha,(int,F)) or F(alpha) not in ALPHAS:
        raise ValueError("alpha must be one of exact 0, 1/2, 1")
    if type(mode) is not str or mode not in MODES:
        raise ValueError("unknown eligible-target policy")
    return F(alpha),mode


def active_edges(state):
    edges,op=normalized_state(*state)
    return tuple((i,j) for i,j in edges if op[i]!=op[j])


def eligible_targets(state,anchor,removed_neighbor,mode):
    edges,op=normalized_state(*state)
    if type(anchor) is not int or type(removed_neighbor) is not int or (
       not 0<=anchor<N or not 0<=removed_neighbor<N or anchor==removed_neighbor):
        raise ValueError("invalid anchor/neighbor")
    checked_controls(0,mode)
    neighbors={b if a==anchor else a for a,b in edges if anchor in (a,b)}
    return tuple(k for k in range(N) if k!=anchor and k!=removed_neighbor and
                 k not in neighbors and (mode=="any" or op[k]==op[anchor]))


def new_graph(edges,old_edge,new_edge):
    graph=set(edges)
    if old_edge not in graph:
        raise ValueError("attempt to remove absent edge")
    graph.remove(old_edge)
    graph.add((min(new_edge),max(new_edge)))
    return tuple(sorted(graph))


@lru_cache(None)
def direct_transition(state,alpha,mode):
    edges,op=normalized_state(*state)
    alpha,mode=checked_controls(alpha,mode)
    live=active_edges((edges,op))
    if not live:
        return (((edges,op),F(1)),)
    out=defaultdict(F)
    for old in live:
        for anchor,other in (old,(old[1],old[0])):
            base=F(1,2*len(live))
            if alpha<F(1):
                changed=list(op)
                changed[anchor]=op[other]
                out[(edges,tuple(changed))]+=base*(1-alpha)
            if alpha>0:
                candidate=eligible_targets((edges,op),anchor,other,mode)
                if not candidate:
                    out[(edges,op)]+=base*alpha
                else:
                    for new_other in candidate:
                        newer=new_graph(edges,old,(anchor,new_other))
                        out[(newer,op)]+=base*alpha/len(candidate)
    ordered=tuple(sorted((state,p) for state,p in out.items() if p))
    if sum((v for _,v in ordered),F(0))!=1:
        raise AssertionError("direct transition not normalized")
    return ordered


@lru_cache(None)
def enumerated_transition(state,alpha,mode):
    """Independent oriented active-edge categorical event space.

    Does not use direct_transition, active_edges, eligible_targets or new_graph.
    """
    edge_input,opin_input=state
    edges,op=normalized_state(edge_input,opin_input)
    alpha,mode=checked_controls(alpha,mode)
    directed=[(i,j) for i,j in edges if op[i]!=op[j]]+[
              (j,i) for i,j in edges if op[i]!=op[j]]
    if not directed:return (((edges,op),F(1)),)
    tally=defaultdict(F)
    for anchor,neighbor in directed:
        weight=F(1,len(directed))
        if alpha!=1:
            copied=list(op)
            copied[anchor]=op[neighbor]
            tally[(edges,tuple(copied))]+=weight*(1-alpha)
        if alpha!=0:
            adjacent=set()
            for i,j in edges:
                if i==anchor:adjacent.add(j)
                if j==anchor:adjacent.add(i)
            possible=[]
            for candidate in range(N):
                if candidate==anchor or candidate==neighbor or candidate in adjacent:
                    continue
                if mode=="same" and op[candidate]!=op[anchor]:continue
                possible.append(candidate)
            if not possible:
                tally[(edges,op)]+=weight*alpha
            else:
                for candidate in possible:
                    discarded=(min(anchor,neighbor),max(anchor,neighbor))
                    included=(min(anchor,candidate),max(anchor,candidate))
                    new_edges=tuple(sorted((set(edges)-{discarded})|{included}))
                    tally[(new_edges,op)]+=weight*alpha/F(len(possible))
    result=tuple(sorted((k,v) for k,v in tally.items() if v))
    if sum((v for _,v in result),F(0))!=1:
        raise AssertionError("enumerated transition not normalized")
    return result


@lru_cache(None)
def direct_path(state,alpha,mode):
    normalized=normalized_state(*state)
    checked_controls(alpha,mode)
    current={normalized:F(1)}
    out=[tuple(sorted(current.items()))]
    for _ in range(HORIZON):
        next_states=defaultdict(F)
        for key,mass in current.items():
            for dest,prob in direct_transition(key,alpha,mode):
                next_states[dest]+=mass*prob
        current=dict(next_states)
        if sum(current.values(),F(0))!=1:raise AssertionError("path not normalized")
        out.append(tuple(sorted(current.items())))
    return tuple(out)


@lru_cache(None)
def enumerated_path(state,alpha,mode):
    normalized=normalized_state(*state)
    checked_controls(alpha,mode)
    current={normalized:F(1)}
    out=[tuple(sorted(current.items()))]
    for _ in range(HORIZON):
        next_states=defaultdict(F)
        for key,mass in current.items():
            for dest,prob in enumerated_transition(key,alpha,mode):
                next_states[dest]+=mass*prob
        current=dict(next_states)
        out.append(tuple(sorted(current.items())))
    return tuple(out)


def component_count(edges):
    nodes=list(range(N))
    for a,b in edges:
        pa=nodes[a]
        pb=nodes[b]
        for i in range(N):
            if nodes[i]==pb:nodes[i]=pa
    return len(set(nodes))


def summary(distribution):
    if sum((mass for _,mass in distribution),F(0))!=1:
        raise AssertionError("snapshot not normalized")
    return {
      "expected_discordant_edges":str(sum((F(len(active_edges(s)))*v for s,v in distribution),F(0))),
      "expected_A_count":str(sum((F(sum(s[1]))*v for s,v in distribution),F(0))),
      "expected_components":str(sum((F(component_count(s[0]))*v for s,v in distribution),F(0))),
      "distinct_labeled_states":len(distribution)
    }


@lru_cache(None)
def document():
    worlds=[]
    for gi,(graph_name,edges) in enumerate(GRAPHS):
        for oi,(op_name,opinions) in enumerate(OPINIONS):
            state=normalized_state(edges,opinions)
            for ai,alpha in enumerate(ALPHAS):
                for mi,mode in enumerate(MODES):
                    path=direct_path(state,alpha,mode)
                    check=enumerated_path(state,alpha,mode)
                    if path!=check:raise AssertionError("two oracles disagree")
                    states=[]
                    for time,dist in enumerate(path):
                        expected=summary(dist)
                        states.append({"t":time,**expected,
                            "distribution":[{
                                 "edges":[list(x) for x in key[0]],
                                 "opinions":list(key[1]),
                                 "probability":str(prob)
                            } for key,prob in dist]})
                    worlds.append({"id":f"g{gi}_o{oi}_a{ai}_m{mi}",
                        "graph":graph_name,"opinion_template":op_name,
                        "alpha":str(alpha),"rewiring_mode":mode,
                        "exact_complete_oracles_equal":True,
                        "snapshots":states})
    if len(worlds)!=72 or len({w["id"] for w in worlds})!=72:
        raise AssertionError("frozen 72-case set not fulfilled")
    mode_distinguishes=[]
    for gi,(g,edges) in enumerate(GRAPHS):
        for oi,(o,opinions) in enumerate(OPINIONS):
            s=normalized_state(edges,opinions)
            if direct_path(s,F(1),"same")!=direct_path(s,F(1),"any"):
                mode_distinguishes.append(f"{g}_{o}")
    if not mode_distinguishes:
        raise AssertionError("frozen policies cannot be distinguished")
    return {
      "research_id":"R169",
      "evidence":"E1_FOUR_NODE_LABELED_ADAPTIVE_NETWORK_EXACT_ONLY",
      "author_phase_transition_recreated":False,
      "original_author_event_clock_claimed":False,
      "real_network_or_opinion_data_used":False,
      "world_count":72,"steps_per_world":3,
      "worlds":worlds,
      "frozen_controls":{
        "edge_count_templates":[len(x[1]) for x in GRAPHS],
        "target_mode_different_at_alpha1_worlds":mode_distinguishes,
        "alpha0_graph_fixed":all(
          len({tuple(tuple(edge) for edge in item["edges"])
               for snap in w["snapshots"] for item in snap["distribution"]})==1
          for w in worlds if w["alpha"]=="0"),
        "alpha1_A_count_fixed":all(len({sum(item["opinions"])
                                      for snap in w["snapshots"] for item in snap["distribution"]})==1
                                   for w in worlds if w["alpha"]=="1"),
      }
    }


if __name__=="__main__":
    print(json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False))
