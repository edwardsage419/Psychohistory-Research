#!/usr/bin/env python3
"""R110 C0 frozen 2015 UCL 120 human PLOS source real lag Brier controls.

STRICT E2 BOUNDED ACTOR-EXCLUDED external reference with observed actor history.
No true original lab-session ID or actual partner person ID in source; author
provided prior partner cooperation signal not independently opponent verified.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,math,pathlib,random
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a
import r110_phase_b1_2015_PLOS_UCL_original_subject_game_round_NONBEHAVIOR_roster as b

MODELS=("M0","M1","M2","M3","M4")
PRIMARY={
  "M3_vs_M2_equal_shrink":"M2",
  "M3_vs_M4_same_marginal_shuffled_peer":"M4",
  "M3_vs_M1_own_lag":"M1",
  "M3_vs_M0_external_prior":"M0",
}
PSEED=110
BOOTSTRAP=2000
MIN_TARGETS=800
MIN_ACTORS=40
BINARY={"0":0,"1":1,"0.0":0,"1.0":1}
HEAD=("Round","Subject ID","Player type","Partner type","Gender","Age",
      "Country","Subject studied","Partner coop prev","Game type",
      "Player C after D","Player P in response to C","Partner P after D prev",
      "Player opt out after D","Player P in response to D","Player cooperated",
      "Partner opt out prev","Player C after D 2")

def binary(value):
    return BINARY.get(value.strip()) if isinstance(value,str) else None

def fixed_laplace(successes,n):
    return (1+successes)/(n+2)

def score_subset(records):
    n=len(records)
    if not n:return {"scored_actions":0,"brier":{m:None for m in MODELS},"gains":{name:None for name in PRIMARY}}
    mse={m:math.fsum(x["loss"][m] for x in records)/n for m in MODELS}
    return {"scored_actions":n,"brier":mse,
        "gains":{name:mse[alt]-mse["M3"] for name,alt in PRIMARY.items()}}

def evaluate_original_source(raw,enforce_real_source=True):
    roster=b.audited_source_actor_game_round_roster(raw)
    if enforce_real_source and (
        not roster["exact_paper_reported_120_people_two_games_50_each_source_structure"]
        or roster["source_distinct_pseudonymous_Subject_ID_codes"]!=120
        or roster["source_duplicate_subject_game_round_keys"]!=0):
        raise a.SourceError("R110_C0_SOURCE_NONBEHAVIOR_120_ACTOR_TWO_GAME_ROSTER_GATE")
    try:r=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
    except UnicodeError as e:raise a.SourceError("R110_C0_ORIGINAL_SOURCE_CSV_ENCODING_INVALID") from e
    header=next(r,None)
    if tuple(header or ())!=HEAD:
        raise a.SourceError("R110_C0_PRE_FROZEN_18_ORIGINAL_BEHAVIOR_COLUMN_IDENTITY_DIFFERENT")
    obs={}
    by_group_previous=collections.defaultdict(dict)
    actor_condition={}
    for row in r:
        if len(row)!=18:
            raise a.SourceError("R110_C0_SOURCE_ROW_WIDTH_UNEXPECTED")
        # Allowed ONLY the predeclared source behavior and nonbehavior fields:
        sid=row[1]
        game=row[9]
        t=int(row[0])
        condition=(game,row[2],row[3])
        k=(sid,game,t)
        if k in obs:
            raise a.SourceError("R110_C0_SOURCE_DUPLICATE_ACTOR_GAME_ROUND")
        # No demographic, payoff, punishment, derived own C after D values touched.
        y=binary(row[15])
        peer=binary(row[8])
        optprev=binary(row[16])
        obs[k]={"sid":sid,"game":game,"condition":condition,"t":t,
                "y":y,"peer_lag":peer,"peer_optout_previous":optprev}
        by_group_previous[(condition,t)][sid]=y
        actor_condition[(sid,game)]=condition
    if enforce_real_source and len(obs)!=12000:
        raise a.SourceError("R110_C0_ORIGINAL_12000_RAW_BEHAVIOR_ROUND_SOURCE_UNIVERSE")
    missing=collections.Counter()
    candidate=[]
    for sid,game,t in sorted(obs):
        record=obs[(sid,game,t)]
        if t==1:
            missing["first_round_each_actor_game"]+=1
            continue
        previous=obs.get((sid,game,t-1))
        if previous is None:
            missing["no_exact_previous_actor_game_period"]+=1
            continue
        if record["y"] is None:
            missing["invalid_or_missing_current_binary_action"]+=1
            continue
        if previous["y"] is None:
            missing["invalid_or_missing_previous_own_binary_action"]+=1
            continue
        if record["peer_lag"] is None:
            missing["invalid_or_missing_author_previous_peer_signal"]+=1
            continue
        if record["peer_optout_previous"]!=0:
            missing["prior_partner_optout_or_unknown"]+=1
            continue
        if record["condition"]!=previous["condition"]:
            missing["source_actor_game_condition_changed"]+=1
            continue
        condition=record["condition"]
        values=by_group_previous[(condition,t-1)]
        pool=[v for other,v in values.items() if other!=sid and v is not None]
        if len(pool)<2:
            missing["external_prior_same_condition_pool_below_two"]+=1
            continue
        q=fixed_laplace(sum(pool),len(pool))
        candidate.append({
            "sid":sid,"game":game,"condition":condition,"t":t,
            "target":record["y"],"own":previous["y"],"peer":record["peer_lag"],
            "external":q,
        })
    strata=collections.defaultdict(list)
    for rec in candidate:
        strata[(rec["condition"],rec["t"])].append(rec)
    eligible=[]
    for group in strata.values():
        group.sort(key=lambda x:x["sid"])
        if len(group)<2:
            missing["sham_donor_source_stratum_under_two"]+=len(group)
            continue
        for j,rec in enumerate(group):
            donor=group[(j+1)%len(group)]
            if rec["sid"]==donor["sid"]:
                raise a.SourceError("R110_C0_SOURCE_SHAM_DONOR_MUST_DIFFER_ACTOR")
            o=rec["own"];p=rec["peer"];q=rec["external"];sham=donor["peer"]
            forecasts={
              "M0":q,"M1":float(o),"M2":0.5*o+0.5*q,
              "M3":0.5*o+0.5*p,"M4":0.5*o+0.5*sham,
            }
            if any(not math.isfinite(pred) or not 0<=pred<=1 for pred in forecasts.values()):
                raise a.SourceError("R110_C0_MODEL_PREDICTION_PROBABILITY_OUT_OF_BOUNDS")
            eligible.append({
                "sid":rec["sid"],"game":rec["game"],"t":rec["t"],
                "loss":{m:(rec["target"]-forecast)**2 for m,forecast in forecasts.items()},
            })
    if sum(missing.values())+len(eligible)!=len(obs):
        raise a.SourceError("R110_C0_FIXED_SAMPLE_ELIGIBILITY_DENOMINATOR_NOT_CLOSED")
    actor_set={r["sid"] for r in eligible}
    game_set={r["game"] for r in eligible}
    if enforce_real_source and (len(eligible)<MIN_TARGETS or
        len(actor_set)<MIN_ACTORS or len(game_set)<2):
        raise a.SourceError("R110_C0_PRE_FROZEN_REAL_800_TARGET_40_ACTOR_2_GAME_GATE_FAIL")
    per_actor=collections.defaultdict(list)
    per_game=collections.defaultdict(list)
    for record in eligible:
        per_actor[record["sid"]].append(record)
        per_game[record["game"]].append(record)
    by_actor=[]
    for slot,sid in enumerate(sorted(per_actor),start=1):
        result=score_subset(per_actor[sid])
        by_actor.append({
            "anonymous_pseudonymous_actor_slot":slot,
            "source_scored_next_actions":result["scored_actions"],
            "real_source_Brier":result["brier"],
            "real_source_gains":result["gains"],
        })
    per_game_out=[]
    for slot,game in enumerate(sorted(per_game),start=1):
        result=score_subset(per_game[game])
        per_game_out.append({"anonymous_original_game_category_slot":slot,
                             "scored_next_actions":result["scored_actions"],
                             "brier":result["brier"],"gains":result["gains"]})
    dirs={}
    for contrast in PRIMARY:
        gains=[r["real_source_gains"][contrast] for r in by_actor]
        dirs[contrast]={
            "positive_source_actors":sum(z>0 for z in gains),
            "negative_source_actors":sum(z<0 for z in gains),
            "zero_source_actors":sum(z==0 for z in gains),
        }
    bootstrap={}
    actor_blocks=[per_actor[s] for s in sorted(per_actor)]
    gen=random.Random(PSEED)
    for contrast,alternative in PRIMARY.items():
        sample_gains=[]
        per_actor_gain_sums=[
            math.fsum(item["loss"][alternative]-item["loss"]["M3"] for item in block)
            for block in actor_blocks
        ]
        per_actor_denominators=[len(block) for block in actor_blocks]
        for _ in range(BOOTSTRAP):
            sampled_indices=[gen.randrange(len(actor_blocks)) for i in range(len(actor_blocks))]
            n=sum(per_actor_denominators[i] for i in sampled_indices)
            improvement=math.fsum(per_actor_gain_sums[i] for i in sampled_indices)/n
            sample_gains.append(improvement)
        sample_gains.sort()
        bootstrap[contrast]={
            "subject_cluster_bootstrap_n":BOOTSTRAP,
            "fixed_seed":PSEED,
            "descriptive_2_5_percentile":sample_gains[49],
            "descriptive_97_5_percentile":sample_gains[1949],
            "dyadic_session_dependence_not_identified":True,
        }
    return {
        "research_id":"R110","phase":"C0",
        "status":"R110_C0_TRUE_2015_UCL_120_SOURCE_PEER_LAG_BOUNDED_ACTOR_EXCLUDED_BRIER_E2",
        "published_original_source_DOI":"10.1371/journal.pone.0117183.s001",
        "original_full_source_SHA256":roster["original_whole_source_SHA256"],
        "original_120_actor_two_50_game_roster_exact":roster["exact_paper_reported_120_people_two_games_50_each_source_structure"],
        "total_true_original_person_game_round_records":len(obs),
        "source_eligible_next_binary_actions":len(eligible),
        "source_distinct_actors_with_eligible_targets":len(actor_set),
        "source_game_categories_with_eligible_targets":len(game_set),
        "source_legal_target_exclusion_reason_counts":dict(sorted(missing.items())),
        "model_definition":{
            "M0":"fixed Laplace pooled other pseudonymous actors same game and player/partner type preceding round (focal entirely excluded)",
            "M1":"same focal human last legal action in exactly same game",
            "M2":"0.5 own preceding action + 0.5 same-condition other-source actor prior-round Laplace mean",
            "M3":"0.5 own preceding action + 0.5 author-coded Partner coop prev at current row",
            "M4":"0.5 own preceding action + 0.5 cyclically permuted other actor's prior peer signal same game/types/round, exactly preserved marginal",
        },
        "original_source_has_true_lab_session_ID":False,
        "original_source_has_counterpart_person_ID":False,
        "original_author_prior_partner_signal_not_independently_partner_ID_verified":True,
        "same_marginal_sham_donor_might_be_actual_partner":True,
        "target_original_Player_cooperated_binary_0_1":"Author Player cooperated 1/1.0=cooperated; 0/0.0=defected; opt-out/missing excluded, not relabeled",
        "loss":"Brier lower better",
        "overall_identical_source_next_action_targets":score_subset(eligible),
        "early_t2_to_t10":score_subset([r for r in eligible if r["t"]<=10]),
        "late_t11_to_t50":score_subset([r for r in eligible if r["t"]>=11]),
        "original_game_2_conditions_anonymous_results":per_game_out,
        "anonymous_source_actor_level_results":by_actor,
        "source_actor_cluster_contrast_directions":dirs,
        "fixed_source_actor_bootstrap_descriptive_only":bootstrap,
        "original_source_actor_ID_or_choice_values_exported":False,
        "not_genuine_lab_session_LOSO":True,
        "not_exact_R073_model_reproduction":True,
        "not_causal_social_learning":True,
        "not_prospective_calendar_E3":True,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=pathlib.Path,required=True)
    args=ap.parse_args()
    try:result=evaluate_original_source(a.actual_official_source(),enforce_real_source=True)
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as e:
        result={"research_id":"R110","phase":"C0",
            "status":"R110_C0_TRUE_SOURCE_BEHAVIOR_OR_PRESCORE_GATE_FAIL_CLOSED",
            "safe_failure":str(e) if isinstance(e,a.SourceError) else "R110_C0_REAL_HUMAN_SOURCE_SCORE_NOT_VERIFIED",
            "real_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R110_C0_TRUE_2015_UCL_120_SOURCE_PEER_LAG_BOUNDED_ACTOR_EXCLUDED_BRIER_E2":
        raise SystemExit(1)
if __name__=="__main__":main()
