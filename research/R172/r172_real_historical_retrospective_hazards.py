"""R172 source-authenticated retrospective regime-breakdown risk prediction.

Original CC0 dataset doi:10.7910/DVN/WFO1N1, Dataverse v1.1.
This is a frozen retrospectively scored model comparison, not a causal claim,
a Cox proportional-hazards fit or a genuine prospective historical forecast.
"""
from __future__ import annotations

from collections import defaultdict,Counter
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path
import csv,hashlib,io,json,math,random,statistics,sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE/"source"
DATA=SOURCE/"Original_Replication_dataset.tab"
OUTPUT=HERE/"R172_EXACT_RESULTS.json"
PREDICTIONS=HERE/"R172_REAL_HELDOUT_PREDICTIONS.csv"
DATA_SHA256="ed8e29368d06d0fa6d597df567eb21e7ac27fa849e1cdfd90b76167c8b5778ba"
AUTHOR_CODE_SHA256="664cf425684b97b8a7bf835ed748955e2e34426e8a14c0db8abbf98a4fb2e3ad"
ORIGINAL_UPLOAD_SHA256="ddca691b25a664ce13ef2471184e3d5ae3ed62cb72521e0593bff770efb0e4e6"
PRECODE_PROTOCOL_COMMIT="099b7a50924c86fdaecb6254eca2748836ae0c64"
CUTOFF_TRAIN_CALENDAR=1999
CUTOFF_TRAIN_TRANSITION=1998
CUTOFF_TEST_TRANSITION=1999
CUTOFF_TEST_CALENDAR=2000
WEIGHT=F(20)
BINS=((0,2),(3,7),(8,15),(16,None))
BOOTSTRAPS=512
SEED=20261021


def assert_original_sources():
    paths={DATA.name:DATA_SHA256,
       "Original_Replication_code_Stata.do":AUTHOR_CODE_SHA256,
       "Original_Replication_dataset_as_uploaded.bin":ORIGINAL_UPLOAD_SHA256}
    seen={}
    for name,digest in paths.items():
        raw=(SOURCE/name).read_bytes()
        h=hashlib.sha256(raw).hexdigest()
        if h!=digest:raise ValueError("Source integrity gate failed: "+name)
        seen[name]={"sha256":h,"bytes":len(raw)}
    return seen


def parse_int(value):
    d=Decimal(str(value))
    if not d.is_finite() or d!=d.to_integral_value():raise ValueError("not an exact integer")
    return int(d)


def parse_optional_decimal(value):
    if value is None or str(value).strip() in ("",".","NA"):return None
    x=Decimal(str(value))
    if not x.is_finite():raise ValueError("nonfinite baseline liberal democracy")
    return x


def parse_rows(raw):
    rd=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")),delimiter="\t")
    if not {"id","country_text_id","country_name","year","t","transition","t0","breakdown","libdem0"}.issubset(rd.fieldnames or []):
        raise ValueError("original expected fields missing")
    result=[]
    for r in rd:
        if r["breakdown"] not in ("0","1",""):
            raise ValueError("unexpected outcome code")
        r0={
         "episode_id":r["id"],"country_id":r["country_text_id"],
         "country_name":r["country_name"],
         "year":parse_int(r["year"]),
         "transition":parse_int(r["transition"]),
         "age":parse_int(r["t"]),
         "t0":parse_int(r["t0"]),
         "event":None if r["breakdown"]=="" else int(r["breakdown"]),
         "baseline_libdem0":parse_optional_decimal(r["libdem0"])
        }
        if not r0["episode_id"] or not r0["country_id"]:raise ValueError("missing episode identity")
        if r0["year"]-r0["t0"]!=r0["age"] or r0["year"]<r0["t0"]:
            raise ValueError("invalid observed event-history time")
        if r0["year"]<r0["transition"]+1:
            raise ValueError("regime event observation precedes recorded transition")
        result.append(r0)
    return result


def load_validated_episodes():
    identities=assert_original_sources()
    raw=DATA.read_bytes()
    rows=parse_rows(raw)
    episode=defaultdict(list)
    for r in rows:episode[r["episode_id"]].append(r)
    if len(rows)!=1731 or len(episode)!=103:
        raise ValueError("original expected source dimensions drifted")
    missing=[r for r in rows if r["event"] is None]
    if len(missing)!=6 or {r["episode_id"] for r in missing}!={"NGA2011"}:
        raise ValueError("missing event labels do not match frozen audit")
    valid={}
    for key,arr in episode.items():
        arr=sorted(arr,key=lambda r:r["year"])
        if len({r["year"] for r in arr})!=len(arr):
            raise ValueError("duplicate episode calendar year")
        if [r["year"] for r in arr]!=list(range(arr[0]["year"],arr[-1]["year"]+1)):
            raise ValueError("source episode has missing observed years")
        if len({r["transition"] for r in arr})!=1 or len({r["country_id"] for r in arr})!=1:
            raise ValueError("multiple source episode identities")
        ones=[i for i,r in enumerate(arr) if r["event"]==1]
        if len(ones)>1 or (ones and ones[0]!=len(arr)-1):
            raise ValueError("duplicate/early event followed by future risk years")
        if key!="NGA2011":
            if any(r["event"] not in (0,1) for r in arr):
                raise ValueError("unexpected nonbinary event")
            baseline=[r["baseline_libdem0"] for r in arr if r["baseline_libdem0"] is not None]
            if len(set(baseline))>1:raise ValueError("in-episode baseline changes")
            valid[key]=arr
    assert sum(len(v) for v in valid.values())==1725 and len(valid)==102
    assert sum(sum(r["event"] for r in v) for v in valid.values())==45
    return valid,identities


def cohorts(episodes):
    train=[];test=[];excluded=[]
    for ident,rows in sorted(episodes.items()):
        start=rows[0]["transition"]
        if start<=CUTOFF_TRAIN_TRANSITION:
            for r in rows:
                if r["year"]<=CUTOFF_TRAIN_CALENDAR:
                    train.append(r)
                else:
                    excluded.append(r)
        elif start>=CUTOFF_TEST_TRANSITION:
            for r in rows:
                if r["year"]<CUTOFF_TEST_CALENDAR:
                    raise ValueError("held-out episode has ineligible year")
                test.append(r)
        else:raise AssertionError("unexpected transition-year gap")
    train.sort(key=lambda r:(r["episode_id"],r["year"]))
    test.sort(key=lambda r:(r["episode_id"],r["year"]))
    excluded.sort(key=lambda r:(r["episode_id"],r["year"]))
    if not train or not test or not any(r["event"]==1 for r in train) or not any(r["event"]==1 for r in test):
        raise ValueError("real-world train/test cohort cannot support event scoring")
    if {r["episode_id"] for r in train}&{r["episode_id"] for r in test}:
        raise AssertionError("leaked episode across train/test split")
    if max(r["year"] for r in train)>1999 or min(r["year"] for r in test)<2000:
        raise AssertionError("calendar future leakage")
    if any(r["transition"]>1998 for r in train) or any(r["transition"]<1999 for r in test):
        raise AssertionError("transition-cohort leakage")
    for r in train:
        if r["year"]>r["transition"] and r["age"]>0 and r["baseline_libdem0"] is None:
            pass
    return train,test,excluded


def bucket(age):
    if type(age) is not int or age<0:raise ValueError("duration age must be a nonnegative integer")
    for i,(lo,hi) in enumerate(BINS):
        if age>=lo and (hi is None or age<=hi):return i
    raise AssertionError("no risk-duration bucket")


def fit_models(train):
    if not train:raise ValueError("empty training risk set")
    if any(r["event"] not in (0,1) for r in train):
        raise ValueError("unlabeled source event in training")
    E=sum(r["event"] for r in train);N=len(train)
    if E==0 or E==N:raise ValueError("insufficient event and non-event training cases")
    p0=F(E+1,N+2)
    base={}
    for b in range(len(BINS)):
        samples=[r for r in train if bucket(r["age"])==b]
        nb=len(samples);eb=sum(r["event"] for r in samples)
        p=(F(eb)+WEIGHT*p0)/(F(nb)+WEIGHT)
        base[b]={"N":nb,"E":eb,"p":p}
    strat={}
    for b in range(len(BINS)):
        for s in ("low","high"):
            samples=[r for r in train
              if r["age"]>=1 and bucket(r["age"])==b
              and r["baseline_libdem0"] is not None
              and ("high" if r["baseline_libdem0"]>=Decimal(50) else "low")==s]
            nbs=len(samples); ebs=sum(r["event"] for r in samples)
            p=(F(ebs)+WEIGHT*base[b]["p"])/(F(nbs)+WEIGHT)
            strat[(b,s)]={"N":nbs,"E":ebs,"p":p}
    return {"N":N,"E":E,"p0":p0,"duration":base,"duration_baseline":strat}


def predict(train_fit,row):
    b=bucket(row["age"])
    p0=train_fit["p0"]
    p1=train_fit["duration"][b]["p"]
    baseline=row["baseline_libdem0"]
    # Non-negotiable: no use of a baseline observation before the episode's
    # first observed year; t=0 M2 always falls back to duration-only M1.
    if row["age"]==0 or baseline is None:
        p2=p1
    else:
        s="high" if baseline>=Decimal(50) else "low"
        p2=train_fit["duration_baseline"][(b,s)]["p"]
    if any(not (0<p<1) for p in (p0,p1,p2)):
        raise AssertionError("conditional hazard outside open probability interval")
    return (p0,p1,p2)


def logloss(label,p):
    if label not in (0,1) or not (0<p<1):raise ValueError("bad scored Bernoulli")
    return -math.log(float(p)) if label else -math.log1p(-float(p))


def brier(label,p):
    if label not in (0,1):raise ValueError("bad Brier label")
    return (float(p)-label)**2


def percentile(values,fraction):
    if not values:raise ValueError("empty bootstrap quantiles")
    v=sorted(values)
    at=(len(v)-1)*fraction
    lo=math.floor(at);hi=math.ceil(at)
    return v[lo]+(v[hi]-v[lo])*(at-lo)


def twelve(x):
    if not math.isfinite(float(x)):raise ValueError("nonfinite score")
    return f"{float(x):.12f}"


def serial_fit(model):
    return {
      "M0":{"N":model["N"],"E":model["E"],"p":str(model["p0"])},
      "M1":[{"age_bucket":b,"range":str(BINS[b]),"N":x["N"],"E":x["E"],"p":str(x["p"])}
            for b,x in sorted(model["duration"].items())],
      "M2":[{"age_bucket":b,"baseline_group":s,"N":x["N"],"E":x["E"],"p":str(x["p"])}
            for (b,s),x in sorted(model["duration_baseline"].items())]
    }


def score(test,model):
    outfile=io.StringIO()
    writer=csv.writer(outfile,lineterminator="\n")
    writer.writerow(["episode_id","country_id","year","transition_year","age_t",
                     "recorded_breakdown_event","baseline_libdem0",
                     "M0_constant_exact","M1_duration_exact","M2_duration_baseline_exact"])
    by_episode=defaultdict(list)
    scores=[]
    for row in test:
        ps=predict(model,row)
        writer.writerow([row["episode_id"],row["country_id"],row["year"],
           row["transition"],row["age"],row["event"],
           "" if row["baseline_libdem0"] is None else str(row["baseline_libdem0"]),
           *(str(p) for p in ps)])
        losses=[logloss(row["event"],p) for p in ps]
        briers=[brier(row["event"],p) for p in ps]
        scores.append({"episode":row["episode_id"],"y":row["event"],
                       "log_loss":losses,"brier":briers})
        by_episode[row["episode_id"]].append(scores[-1])
    matrix_bytes=outfile.getvalue().encode("utf-8")
    PREDICTIONS.write_bytes(matrix_bytes)
    samples={}
    for ep in sorted(by_episode):
        group=by_episode[ep]
        samples[ep]={
          "n":len(group),"events":sum(a["y"] for a in group),
          "log_loss_sum":[sum(a["log_loss"][i] for a in group) for i in range(3)],
          "brier_sum":[sum(a["brier"][i] for a in group) for i in range(3)]
        }
    def scored(indices):
        subset=[samples[ep] for ep in indices]
        n=sum(s["n"] for s in subset)
        episode_count=len(subset)
        return {
         "annual_logloss":[sum(s["log_loss_sum"][i] for s in subset)/n for i in range(3)],
         "annual_brier":[sum(s["brier_sum"][i] for s in subset)/n for i in range(3)],
         "mean_episode_total_logloss":[sum(s["log_loss_sum"][i] for s in subset)/episode_count for i in range(3)],
        }
    full=scored(sorted(samples))
    rng=random.Random(SEED)
    ids=sorted(samples)
    delta_samples={measure:{"M1_vs_M0":[],"M2_vs_M0":[]} for measure in ("annual_logloss","annual_brier")}
    for _ in range(BOOTSTRAPS):
        draw=[ids[rng.randrange(len(ids))] for __ in ids]
        result=scored(draw)
        for measure in delta_samples:
            for i,name in ((1,"M1_vs_M0"),(2,"M2_vs_M0")):
                delta_samples[measure][name].append(result[measure][i]-result[measure][0])
    summary={}
    for measure,vals in full.items():
        summary[measure]={name:twelve(vals[i]) for i,name in enumerate(("M0","M1","M2"))}
        for i,name in ((1,"M1_vs_M0"),(2,"M2_vs_M0")):
            summary[measure][name+"_difference"]=twelve(vals[i]-vals[0])
    ci={}
    for measure,comparisons in delta_samples.items():
        ci[measure]={}
        for name,distribution in comparisons.items():
            ci[measure][name]={
              "point":summary[measure][name+"_difference"],
              "lower_2p5":twelve(percentile(distribution,.025)),
              "upper_97p5":twelve(percentile(distribution,.975)),
            }
    return summary,ci,{"file":PREDICTIONS.name,"bytes":len(matrix_bytes),
                      "sha256":hashlib.sha256(matrix_bytes).hexdigest(),
                      "rows":len(test)},samples


def run():
    episodes,identities=load_validated_episodes()
    train,test,withheld=cohorts(episodes)
    model=fit_models(train)
    scores,intervals,file_meta,ep_samples=score(test,model)
    country_train={r["country_id"] for r in train}
    country_test={r["country_id"] for r in test}
    event_train=sum(r["event"] for r in train)
    event_test=sum(r["event"] for r in test)
    trained=set(r["episode_id"] for r in train)
    heldout=set(r["episode_id"] for r in test)
    output={
     "research_id":"R172",
     "status":"REAL_HISTORICAL_RETROSPECTIVE_EPISODE_HELDOUT_EXPERIMENT",
     "scientific_level":"RETROSPECTIVE_HISTORICAL_DATA_BENCHMARK_NOT_INDEPENDENT_PROSPECTIVE_E3",
     "original_dataset_doi":"10.7910/DVN/WFO1N1",
     "original_dataset_version":"1.1",
     "CC0_license":True,
     "original_source_SHA256_and_bytes":identities,
     "preregistered_protocol_commit":PRECODE_PROTOCOL_COMMIT,
     "source_original_total_rows":1731,
     "source_original_episodes":103,
     "excluded_missing_outcome_episode":"NGA2011",
     "excluded_missing_outcome_rows":6,
     "eligible_source_rows":1725,
     "eligible_source_episodes":102,
     "split":{
       "train_transition_year_max":1998,"train_calendar_year_max":1999,
       "test_transition_year_min":1999,"test_calendar_year_min":2000,
       "train_rows":len(train),"test_rows":len(test),
       "old_episode_future_followup_withheld_rows":len(withheld),
       "train_episodes":len(trained),"test_episodes":len(heldout),
       "train_breakdown_events":event_train,"test_breakdown_events":event_test,
       "train_country_count":len(country_train),"test_country_count":len(country_test),
       "countries_present_in_both_cohorts":sorted(country_train&country_test),
       "train_episode_identities":sorted(trained),
       "test_episode_identities":sorted(heldout),
       "right_censored_training_episodes_under_cutoff":sum(
         train_group[-1]["event"]==0
         for ident in sorted(trained)
         for train_group in [[r for r in train if r["episode_id"]==ident]]),
       "test_right_censored_episodes":sum(v["events"]==0 for v in ep_samples.values()),
       "test_complete_event_episodes":sum(v["events"]==1 for v in ep_samples.values())
     },
     "models_train_only_counts_and_exact_Fraction_parameters":serial_fit(model),
     "score_summary":scores,
     "episode_cluster_resample_CI":{
       "seed":SEED,"iterations":BOOTSTRAPS,"cluster_key":"episode_id",
       "limit":"same countries may contribute multiple episodes; episode bootstrap is not country-clustered inference",
       "percentile_algorithm":"linear_interpolate_sorted_samples_at_(n-1)*q",
       "intervals":intervals
     },
     "full_heldout_predictions_original_rows":file_meta,
     "checks":{
        "no_heldout_episode_used_in_fit":not bool(trained&heldout),
        "no_after_1999_outcome_fitted":all(r["year"]<=1999 for r in train),
        "never_use_t0_baseline_in_M2":all(
          predict(model,r)[1]==predict(model,r)[2] for r in test if r["age"]==0),
        "all_episode_risk_sets_event_ended":True,
        "original_NGA2011_excluded":not bool({"NGA2011"}&(trained|heldout)),
        "all_3_predictions_strict_probabilities":True,
        "observed_test_contains_events":event_test>0,
        "observed_train_contains_events":event_train>0,
     },
     "author_original_Cox_model_reproduced":False,
     "author_original_regime_study_reproduced":False,
     "independent_real_time_historical_event_prediction":False,
     "new_E2_repeated_game_human_predictions":0,
     "new_E3_genuinely_external_historical_forecasts":0,
     "R073":"FROZEN","PESEN_v0_1":"FROZEN"
    }
    OUTPUT.write_text(json.dumps(output,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R172_FROZEN_REAL_SPLIT",json.dumps({k:v for k,v in output["split"].items()
           if k not in ("train_episode_identities","test_episode_identities",
                         "countries_present_in_both_cohorts")},sort_keys=True))
    print("R172_FROZEN_REAL_SCORES",json.dumps(scores,sort_keys=True))
    print("R172_FROZEN_REAL_CI",json.dumps(intervals,sort_keys=True))
    print("R172_FULL_PREDICTIONS_SHA256",file_meta["sha256"])
    print("R172_EXACT_RESULTS_SHA256",hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
    return output


if __name__=="__main__":
    run()
