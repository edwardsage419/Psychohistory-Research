"""R170 exact artificial two-token communication-inventory Markov process.

Project-authored bounded naming-game inspired by Baronchelli et al., 2006.
No real human utterance data, speaker learning, grammar, actual language
extinction or original author large-scale game simulated here.
"""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction as F
import json

N=4
CONTACTS=(
 ("path",((0,1),(1,2),(2,3))),
 ("star",((0,1),(0,2),(0,3))),
 ("cycle",((0,1),(0,3),(1,2),(2,3))),
 ("complete",((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))),
)
INVENTORIES=(
 ("split",(1,1,2,2)),
 ("alternate",(1,2,1,2)),
 ("bilingual",(1,3,2,3)),
)
NOISE=(F(0),F(1,4),F(1,2))
FEEDBACK=("both_confirm","listener_only")
HORIZON=3


def checked_inventory(inv):
    if not isinstance(inv,(list,tuple)) or len(inv)!=N or any(
        type(x) is not int or x not in (1,2,3) for x in inv):
        raise ValueError("exactly four nonempty A/B/AB vocabulary masks")
    return tuple(inv)


def checked_contacts(edges):
    if not isinstance(edges,(list,tuple)) or not edges:
        raise ValueError("must supply a nonempty undirected contact set")
    found=set()
    for edge in edges:
        if not isinstance(edge,(list,tuple)) or len(edge)!=2:
            raise ValueError("malformed contact edge")
        i,j=edge
        if type(i) is not int or type(j) is not int or not (
             0<=i<N and 0<=j<N) or i==j:
            raise ValueError("invalid contact endpoints")
        e=(min(i,j),max(i,j))
        if e in found:raise ValueError("duplicate contact edge")
        found.add(e)
    return tuple(sorted(found))


def checked_controls(nu,feedback):
    if isinstance(nu,bool) or not isinstance(nu,(int,F)) or F(nu) not in NOISE:
        raise ValueError("message flip probability outside frozen grid")
    if type(feedback) is not str or feedback not in FEEDBACK:
        raise ValueError("unknown feedback mode")
    return F(nu),feedback


def words(mask):
    if type(mask) is not int or mask not in (1,2,3):
        raise ValueError("empty or invalid linguistic inventory")
    return tuple(w for w in (1,2) if (mask&w)!=0)


def transform_direct(current,speaker,hearer,heard,feedback):
    inv=list(checked_inventory(current))
    if type(speaker) is not int or type(hearer) is not int or not (
        0<=speaker<N and 0<=hearer<N and speaker!=hearer):
        raise ValueError("invalid directed conversational participants")
    if heard not in (1,2) or type(heard) is not int:
        raise ValueError("heard word is not A/B")
    checked_controls(0,feedback)
    if inv[hearer]&heard:
        inv[hearer]=heard
        if feedback=="both_confirm":
            inv[speaker]=heard
    else:
        inv[hearer]|=heard
    return tuple(inv)


@lru_cache(None)
def direct_kernel(edges,current,nu,feedback):
    graph=checked_contacts(edges)
    inv=checked_inventory(current)
    nu,feedback=checked_controls(nu,feedback)
    out=defaultdict(F)
    for a,b in graph:
        for speaker,hearer in ((a,b),(b,a)):
            chance_edge=F(1,2*len(graph))
            candidates=words(inv[speaker])
            for spoken in candidates:
                chance_word=F(1,len(candidates))
                for flipped,channel_probability in ((False,1-nu),(True,nu)):
                    if channel_probability==0:continue
                    delivered=(3-spoken) if flipped else spoken
                    target=transform_direct(inv,speaker,hearer,delivered,feedback)
                    out[target]+=chance_edge*chance_word*channel_probability
    result=tuple(sorted(out.items()))
    if sum((p for _,p in result),F(0))!=1:
        raise AssertionError("direct naming transition not normalized")
    return result


def conditional_heard_probability_A(speaker_mask,nu):
    possible=words(speaker_mask)
    nu, _=checked_controls(nu,"both_confirm")
    return sum((F(1,len(possible))*(1-nu if word==1 else nu)
                for word in possible),F(0))


@lru_cache(None)
def independently_enumerated_kernel(edges,current,nu,feedback):
    """Independent delivered-token mixture, not direct_kernel or transform_direct."""
    graph=checked_contacts(edges)
    inv=checked_inventory(current)
    nu,feedback=checked_controls(nu,feedback)
    pairs=[(x,y) for x,y in graph]+[(y,x) for x,y in graph]
    out=defaultdict(F)
    for speaker,hearer in pairs:
        source=inv[speaker]
        source_words=tuple(x for x in (1,2) if source&x)
        pA=F(0)
        for x in source_words:
            if x==1:
                pA+=F(1,len(source_words))*(F(1)-nu)
            else:
                pA+=F(1,len(source_words))*nu
        for token,p_message in ((1,pA),(2,F(1)-pA)):
            if not p_message:continue
            updated=list(inv)
            if (inv[hearer]&token)!=0:
                updated[hearer]=token
                if feedback=="both_confirm":
                    updated[speaker]=token
            else:
                updated[hearer]=inv[hearer]|token
            out[tuple(updated)]+=F(1,len(pairs))*p_message
    result=tuple(sorted(out.items()))
    if sum((p for _,p in result),F(0))!=1:
        raise AssertionError("independent naming transition not normalized")
    return result


@lru_cache(None)
def exact_path(edges,initial,nu,feedback):
    graph=checked_contacts(edges)
    initial=checked_inventory(initial)
    nu,feedback=checked_controls(nu,feedback)
    dist={initial:F(1)}
    result=[tuple(sorted(dist.items()))]
    for _ in range(HORIZON):
        later=defaultdict(F)
        for inv,mass in dist.items():
            for updated,prob in direct_kernel(graph,inv,nu,feedback):
                later[updated]+=mass*prob
        dist=dict(later)
        if sum(dist.values(),F(0))!=1:
            raise AssertionError("improper probability mass")
        result.append(tuple(sorted(dist.items())))
    return tuple(result)


@lru_cache(None)
def oracle_path(edges,initial,nu,feedback):
    graph=checked_contacts(edges)
    initial=checked_inventory(initial)
    nu,feedback=checked_controls(nu,feedback)
    dist={initial:F(1)}
    result=[tuple(sorted(dist.items()))]
    for _ in range(HORIZON):
        later=defaultdict(F)
        for inv,mass in dist.items():
            for updated,prob in independently_enumerated_kernel(graph,inv,nu,feedback):
                later[updated]+=mass*prob
        dist=dict(later)
        result.append(tuple(sorted(dist.items())))
    return tuple(result)


def metrics(distribution):
    if sum((mass for _,mass in distribution),F(0))!=1:
        raise AssertionError("snapshot not normalized")
    return {
      "expected_inventory_items":str(sum((F(sum(len(words(x)) for x in s))*p
                                         for s,p in distribution),F(0))),
      "expected_bilingual_speakers":str(sum((F(sum(x==3 for x in s))*p
                                             for s,p in distribution),F(0))),
      "probability_unanimous_single_word":str(sum((p for s,p in distribution
                                                 if s==(1,1,1,1) or s==(2,2,2,2)),F(0))),
      "supported_inventory_vectors":len(distribution)
    }


@lru_cache(None)
def document():
    worlds=[]
    for gi,(graphname,edges) in enumerate(CONTACTS):
        for ii,(inventoryname,initial) in enumerate(INVENTORIES):
            for ni,nu in enumerate(NOISE):
                for mi,feedback in enumerate(FEEDBACK):
                    a=exact_path(edges,initial,nu,feedback)
                    b=oracle_path(edges,initial,nu,feedback)
                    if a!=b:raise AssertionError("R170 independent exact paths differ")
                    stages=[]
                    for t,dist in enumerate(a):
                        stages.append({"t":t,**metrics(dist),
                            "distribution":[{"inventories":list(inv),"probability":str(p)}
                                            for inv,p in dist]})
                    worlds.append({
                       "id":f"g{gi}_i{ii}_n{ni}_m{mi}",
                       "graph":graphname,"initial_vocabulary":inventoryname,
                       "message_flip_probability":str(nu),
                       "feedback":feedback,
                       "independent_exact_oracles_equal":True,
                       "snapshots":stages
                    })
    if len(worlds)!=72 or len({w["id"] for w in worlds})!=72:
        raise AssertionError("frozen 72 worlds missing")
    bilingual=INVENTORIES[2][1]
    initial_difference=exact_path(CONTACTS[0][1],bilingual,F(0),"both_confirm")[1]!=(
                       exact_path(CONTACTS[0][1],bilingual,F(0),"listener_only")[1])
    if not initial_difference:
        raise AssertionError("bilingual model update-policy discriminator failed")
    return {
      "research_id":"R170",
      "evidence":"E1_BOUNDED_TWO_WORD_INVENTORY_NAMING_GAME_ONLY",
      "original_Baronchelli_unbounded_vocabulary_model_reproduced":False,
      "original_human_utterance_data_used":False,
      "real_language_decline_estimated":False,
      "frozen_world_count":72,
      "timepoints_per_world":4,
      "worlds":worlds,
      "prespecified_controls":{
        "bilingual_split_feedback_first_step_different_without_noise":initial_difference,
        "nu_half_delivered_A_equals_half_all_inventory_masks":all(
            conditional_heard_probability_A(mask,F(1,2))==F(1,2) for mask in (1,2,3)),
        "nu_zero_consensus_A_absorbing":all(
            direct_kernel(edges,(1,1,1,1),0,mode)==(((1,1,1,1),F(1)),)
            for _,edges in CONTACTS for mode in FEEDBACK),
        "nu_quarter_consensus_A_nonabsorbing":all(
            direct_kernel(edges,(1,1,1,1),F(1,4),mode)!=(((1,1,1,1),F(1)),)
            for _,edges in CONTACTS for mode in FEEDBACK),
      }
    }


if __name__=="__main__":
    print(json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False))
