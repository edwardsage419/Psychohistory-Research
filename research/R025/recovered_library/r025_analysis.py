#!/usr/bin/env python3
"""R025: local re-analysis of *derived genuine* R024 numeric survey records.

Source: StanfordHCI/spiral-of-silence/data.csv
Author Git blob: 11c4ccb53944a79b1f1def49d358e04c944e42f1

Important: this is NOT raw-author-byte-to-local provenance. The numeric
records are a validated pseudonymized derivative; no actual posting behavior.
R025 also audits a second experiment, Oswald et al. 2025, whose Zenodo CSV
bytes are NOT in this package. No empirical treatment estimate is claimed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t as student_t
import statsmodels.formula.api as smf
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups,cov_cluster

ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
SOURCE_BLOB='11c4ccb53944a79b1f1def49d358e04c944e42f1'
DERIVED_FNV1A32='d6606b70'
EXPECTED={"records":439,"participants":58,"items":130,"communities":12}


def fnv1a32(data: str):
    acc=2166136261
    for value in data.encode('ascii'):
        acc=((acc ^ value)*16777619)&0xffffffff
    return f'{acc:08x}'


def decode(text: str, verify=True):
    raw=''.join(text.split())
    if len(raw)%10:raise ValueError('Each encoded record must be 10 characters')
    if any(x not in ALPHABET for x in raw):raise ValueError('Invalid alphabet')
    if verify and fnv1a32(raw)!=DERIVED_FNV1A32:
        raise ValueError('Cross-platform checksum mismatch')
    out=[]
    for k in range(0,len(raw),10):
        parts=[ALPHABET.index(x) for x in raw[k:k+10]]
        vals=[parts[0],parts[1]*64+parts[2],*parts[3:]]
        p,item,community,topic,a,perception,inc,comment,upvote=vals
        if not (0<=p<64 and 0<=item<4096 and 1<=a<=7 and 1<=perception<=7
                and inc in (0,1) and 1<=comment<=7 and 1<=upvote<=7):
            raise ValueError('Unexpected value/scale')
        if inc!=int(perception<=4):raise ValueError('Incongruency classification mismatch')
        out.append((p,item,community,topic,a,perception,inc,comment,upvote))
    df=pd.DataFrame(out,columns=['participant','item','community','topic','agreement',
                                   'perceived_community_agreement','incongruency',
                                   'comment_likelihood','upvote_likelihood'])
    if verify:
        s={'records':len(df),'participants':df.participant.nunique(),
           'items':df.item.nunique(),'communities':df.community.nunique()}
        if s!=EXPECTED:raise ValueError(f'Unexpected real-data shape: {s}')
        if df.duplicated(['participant','item']).any():
            raise ValueError('Repeated person-item key')
        if (df.groupby('item').community.nunique()>1).any():
            raise ValueError('Item assigned to multiple communities')
    return df


def cluster_diagnostics(df,y='comment_likelihood'):
    model=smf.ols(y+' ~ incongruency + agreement + C(participant) + C(item)',data=df).fit()
    idx=list(model.params.index).index('incongruency')
    # CGM inclusion-exclusion: V(person) + V(item) - V(person x item).
    # This is a two-way cluster-robust sandwich; NOT randomization inference.
    both,person,item=cov_cluster_2groups(model,df.participant.to_numpy(dtype='int64'),
                                              df.item.to_numpy(dtype='int64'),use_correction=True)
    community_only=cov_cluster(model,df.community.to_numpy(dtype="int64"),use_correction=True)
    participant_community,_,_=cov_cluster_2groups(model,df.participant.to_numpy(dtype="int64"),
                                                 df.community.to_numpy(dtype="int64"),use_correction=True)
    beta=float(model.params.iloc[idx]);v=float(both[idx,idx])
    if not v>0:raise ValueError('Nonpositive two-way sandwich variance')
    se=float(np.sqrt(v))
    # Conservative exploratory reference df based on 58 persons vs 130 items.
    p=float(2*student_t.sf(abs(beta/se),df=min(df.participant.nunique(),df.item.nunique())-1))
    q=float(student_t.ppf(.975,df=min(df.participant.nunique(),df.item.nunique())-1))
    return dict(outcome=y,records=len(df),beta=beta,se_two_way=se,
                se_by_person=float(np.sqrt(person[idx,idx])),
                se_by_item=float(np.sqrt(item[idx,idx])),
                sensitivity_se_community_only=float(np.sqrt(community_only[idx,idx])),
                sensitivity_se_person_community=float(np.sqrt(participant_community[idx,idx])),
                t_reference_df=57,approx_p_two_sided=p,approx_95_interval=[beta-q*se,beta+q*se],
                component_variance=dict(person=float(person[idx,idx]),item=float(item[idx,idx]),
                                        joint=float(person[idx,idx]+item[idx,idx]-both[idx,idx])),
                model_rank=int(model.model.rank),residual_df=int(model.df_resid))


def leave_one_group_out(df,group):
    vals=[]
    for key in sorted(df[group].unique()):
        keep=df[df[group]!=key]
        fit=smf.ols('comment_likelihood ~ incongruency + agreement + C(participant) + C(item)',data=keep).fit()
        vals.append(dict(omitted=int(key),remaining_rows=len(keep),
                         beta=float(fit.params['incongruency'])))
    return {'n_omitted_groups':len(vals),'min_beta':min(z['beta'] for z in vals),
            'max_beta':max(z['beta'] for z in vals),
            'nonnegative_count':sum(z['beta']>=0 for z in vals),
            'all':vals}


def hypothetical_six_community_assignments():
    """Number of unordered allocations with exactly 2 communities per arm.

    Does NOT assert these were the authors' actual randomization permutations.
    """
    from math import factorial
    k=factorial(6)//(factorial(2)**3)
    assert k==90
    return {'communities':6,'communities_per_arm':2,
      'balanced_labelings_if_fully_exchangeable':k,
      'min_raw_permutation_resolution_if_all_90_admissible':1/k,
      'scope':'Mathematical design diagnostic ONLY; actual assignment mechanism unverified'}


def analyze(df,do_leave_one_out=True):
    res={'round':'R025','scope':'real derived-data sensitivity and new-source intake gate',
         'data_provenance':{'repository':'https://github.com/StanfordHCI/spiral-of-silence',
                            'git_blob_sha1':SOURCE_BLOB,'derived_fnv1a32':DERIVED_FNV1A32,
                            'local_origin':'pseudonymized numeric derivative from R024, not original CSV'},
         'survey_source_shape':{'n':len(df),'participants':df.participant.nunique(),
                               'items':df.item.nunique(),'communities':df.community.nunique()},
         'comment':cluster_diagnostics(df,'comment_likelihood'),
         'upvote':cluster_diagnostics(df,'upvote_likelihood'),
         'new_field_experiment':hypothetical_six_community_assignments(),
         'warnings':['Both comment and upvote outcomes are self-reported likelihood, not actual posts.',
                     'Incongruency not randomized; clustering does not solve selection/confounding.',
                     'Two-way sandwich small-cluster degrees-of-freedom approximation is exploratory.',
                     '2025 Reddit field experiment primary dataset was NOT downloaded/analyzed.']}
    if do_leave_one_out:
        res['persons_cross_community_counts']={int(k):int(v) for k,v in df.groupby('participant').community.nunique().value_counts().items()}
        res['omit_community']=leave_one_group_out(df,'community')
        res['omit_person']=leave_one_group_out(df,'participant')
        res['omit_item']=leave_one_group_out(df,'item')
    return res


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=Path(__file__).with_name('DERIVED_NUMERIC_ROWS.txt'))
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULTS.json'))
    parser.add_argument('--skip-leave-one-out',action='store_true')
    args=parser.parse_args()
    raw=args.input.read_text(encoding='ascii')
    df=decode(raw)
    res=analyze(df,do_leave_one_out=not args.skip_leave_one_out)
    res['derived_input_sha256']=hashlib.sha256(raw.encode('ascii')).hexdigest()
    args.output.write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'comment':res['comment'],'upvote':res['upvote'],
                       'out':str(args.output)},indent=2))
if __name__=='__main__':main()