"""R273 S69 ↔ original source matching, not a new estimator or acceptance gate."""
import csv
from fractions import Fraction as F
import io
import re


def require(ok,reason):
    if not ok:raise ValueError(reason)


def identical_bytes(actual,expected):
    require(type(actual) is bytes and type(expected) is bytes and actual==expected,'NATIVE_BYTE_MISMATCH')
    return len(actual)


def read_rows(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8'),newline=''))
    require(reader.fieldnames is not None and len(set(reader.fieldnames))==len(reader.fieldnames),'CSV_HEADER')
    rows=list(reader);require(all(None not in r and None not in r.values() for r in rows),'CSV_WIDTH')
    return rows


def compare_sources(paired_csv,original_csv):
    """Identity join all576paired states to1728original predictor records.

    Fractions normalize original1/2 versus S69's2/4 metadata. Integer score
    numerators bind the same target pair; no statistical re-estimation.
    """
    original=read_rows(original_csv);paired=read_rows(paired_csv)
    require(len(original)==1728 and len(paired)==576,'SOURCE_CARDINALITY')
    models=('SOURCE_ORACLE','SOURCE_LAPLACE','TARGET_ORACLE');lookup={}
    ps={F(1,4),F(1,2),F(3,4)}
    for r in original:
        a,b=F(r['source_group_true_p']),F(r['target_group_true_p'])
        bits=r['original_full_source_target_sixbits'];model=r['fixed_predictor']
        require(a in ps and b in ps and model in models and re.fullmatch('[01]{6}',bits) is not None,'ORIGINAL_IDENTITY')
        key=a,b,model,bits;require(key not in lookup,'ORIGINAL_DUPLICATE');lookup[key]=r
        require(r['original_source_group_fourbits']==bits[:4] and r['original_target_group_twobits']==bits[4:],'ORIGINAL_SPLIT')
    seen=set();masses={};joins=0
    for r in paired:
        m=re.fullmatch(r'A([123])OF4_B([123])OF4',r['world'])
        require(m is not None,'PAIRED_WORLD');a,b=(F(int(v),4) for v in m.groups())
        bits=r['sixbits'];require(re.fullmatch('[01]{6}',bits) is not None,'PAIRED_BITS')
        key=a,b,bits;require(key not in seen,'PAIRED_DUPLICATE');seen.add(key)
        weight=int(r['weight_num_4096']);require(weight>0,'PAIRED_WEIGHT')
        masses[a,b]=masses.get((a,b),0)+weight
        ls,ll=int(r['source_score_num_288']),int(r['laplace_score_num_288'])
        require(r['paired_outcome']==('L_BETTER' if ll<ls else 'S_BETTER' if ll>ls else 'TIE'),'PAIRED_RANK')
        for model in models:
            base=lookup[a,b,model,bits];joins+=1
            require(F(base['exact_two_population_source_probability'])==F(weight,4096),'SOURCE_WEIGHT')
            q=F(base['frozen_before_target_observation_forecast'])
            want=F(int(r['source_forecast_num_12']),12) if model=='SOURCE_ORACLE' else F(int(r['laplace_forecast_num_12']),12) if model=='SOURCE_LAPLACE' else b
            require(q==want,'SOURCE_FORECAST')
            if model!='TARGET_ORACLE':
                require(F(base['target_independent_mean_Brier'])==F(ls if model=='SOURCE_ORACLE' else ll,288),'PAIRED_TEST_SCORE')
    require(len(masses)==9 and all(x==4096 for x in masses.values()),'WORLD_MASS')
    require(joins==1728,'SOURCE_COVERAGE')
    return {'paired_rows':576,'original_rows':1728,'model_source_joins':joins,'worlds':9,'probability_masses_each':4096}


def compare_risks(extension,original):
    lookup={(F(r['source_p']),F(r['target_p']),r['predictor']):F(r['complete_source_expected_target_test_Brier'])
            for r in original['world_results']}
    require(len(lookup)==27,'ORIGINAL_RISK_COVERAGE');seen=set();count=0
    for r in extension['world_results']:
        a,b=F(r['source_p']),F(r['target_p']);require((a,b) not in seen,'DUPLICATE_RISK_WORLD');seen.add((a,b))
        for model,field in (('SOURCE_ORACLE','source_oracle_risk'),('SOURCE_LAPLACE','source_laplace_risk'),('TARGET_ORACLE','target_oracle_risk')):
            require(lookup[a,b,model]==F(r[field]),'POPULATION_RISK_PARITY');count+=1
    require(len(seen)==9 and count==27,'RISK_COVERAGE')
    return count
