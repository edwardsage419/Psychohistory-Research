#!/usr/bin/env python3
"""R024 actual derived-data analysis, offline reproducible.
Original author Git blob source obtained with GitHub read-only connector:
StanfordHCI/spiral-of-silence/data.csv SHA1 11c4ccb53944a79b1f1def49d358e04c944e42f1.
The DERIVED_NUMERIC_ROWS.txt strips original Participant identifiers and item text.
This is an independent analytical derivative, not the original author's CSV bytes.
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
SOURCE_SHA='11c4ccb53944a79b1f1def49d358e04c944e42f1'
FIELDS=('participant','item','subreddit','topic','agreement','community_agreement','incongruency','comment_likelihood','upvote_likelihood')

def decode(payload):
    raw=''.join(payload.split())
    if len(raw)%10:raise ValueError('invalid 10-character record framing')
    vals=[]
    for k in range(0,len(raw),10):
        c=raw[k:k+10]
        if any(t not in ALPHABET for t in c):raise ValueError('invalid numeric code')
        a=[ALPHABET.index(t) for t in c]
        v=[a[0],a[1]*64+a[2],*a[3:]]
        row=dict(zip(FIELDS,v))
        if not (5<=row['agreement']<=7 and 1<=row['community_agreement']<=7 and 1<=row['comment_likelihood']<=7 and 1<=row['upvote_likelihood']<=7 and row['incongruency'] in (0,1)):
            raise ValueError('invalid scale in record')
        vals.append(row)
    return pd.DataFrame(vals,columns=FIELDS)

def check(df):
    if not np.array_equal(df.incongruency.to_numpy(),(df.community_agreement<=4).astype(int).to_numpy()):
        raise ValueError('Incongruency mismatch with (Sub_Agree <= 4) coding')
    # Names are intentionally omitted; item is indexed per original (Subreddit, Topic, Viewpoint) triple.
    if df.groupby('item').subreddit.nunique().max()>1:raise ValueError('item spans multiple subreddits')
    if df.groupby('item').topic.nunique().max()>1:raise ValueError('item spans multiple topics')
    return dict(rows=len(df),persons=int(df.participant.nunique()),viewpoints=int(df.item.nunique()),subreddits=int(df.subreddit.nunique()),topics_in_community=int(df.groupby(['subreddit','topic']).ngroups),incongruency_coding_mismatch=0)

def item_contrasts(df):
    out=[]
    for item,g in df.groupby('item'):
        b=g[g.incongruency==0];a=g[g.incongruency==1]
        if len(a) and len(b):
            out.append(dict(item=int(item),n_congruent=len(b),n_incongruent=len(a),
                            difference=float(a.comment_likelihood.mean()-b.comment_likelihood.mean()),
                            avg_agreement_diff=float(a.agreement.mean()-b.agreement.mean())))
    return out

def participant_contrasts(df, split='participant'):
    out=[]
    for id,g in df.groupby(split):
        a=g[g.incongruency==1];b=g[g.incongruency==0]
        if len(a) and len(b):
            out.append(float(a.comment_likelihood.mean()-b.comment_likelihood.mean()))
    return out

def percent_ci(arr, seed=20261014, n=10000):
    if not arr:raise ValueError('need overlap')
    rng=np.random.default_rng(seed)
    vals=np.array(arr,dtype=float)
    # Data blocks are not assumed independent beyond explicitly chosen stratum; exploratory only.
    draws=np.mean(rng.choice(vals,size=(n,len(vals)),replace=True),axis=1)
    return [float(np.quantile(draws,.025)),float(np.quantile(draws,.975))]

def fe(df,formula):
    fit=smf.ols(formula,data=df).fit()
    # Participant cluster robust; no guarantee this accounts for item dependence.
    by_person=fit.get_robustcov_results(cov_type='cluster',groups=df.participant,use_t=True)
    by_item=fit.get_robustcov_results(cov_type='cluster',groups=df.item,use_t=True)
    name='incongruency';k=list(fit.params.index).index(name)
    return {'beta':float(fit.params.iloc[k]),'rank':int(fit.model.rank),
            'df_resid':float(fit.df_resid),'se_cluster_participant':float(by_person.bse[k]),
            'p_cluster_participant':float(by_person.pvalues[k]),
            'se_cluster_item':float(by_item.bse[k]),
            'p_cluster_item':float(by_item.pvalues[k]),
            'r2':float(fit.rsquared)}

def analyze(df,boot=10000):
    audit=check(df)
    cell=[]
    for inc,g in df.groupby('incongruency'):
        cell.append(dict(incongruency=int(inc),n=len(g),mean_comment=float(g.comment_likelihood.mean()),
                         mean_agreement=float(g.agreement.mean()),mean_sub_agreement=float(g.community_agreement.mean()),
                         mean_upvote=float(g.upvote_likelihood.mean())))
    ps=participant_contrasts(df)
    item=item_contrasts(df)
    itemdiff=[x['difference'] for x in item]
    # Compare nested controls; no model is guaranteed causal or preregistered.
    formulas={
      'naive':'comment_likelihood ~ incongruency',
      'agreement_only':'comment_likelihood ~ incongruency + agreement',
      'participant_FE_agreement':'comment_likelihood ~ incongruency + agreement + C(participant)',
      'item_FE_agreement':'comment_likelihood ~ incongruency + agreement + C(item)',
      'two_way_FE_agreement':'comment_likelihood ~ incongruency + agreement + C(participant) + C(item)'
    }
    x=df.copy()
    x['comment_minus_upvote']=x.comment_likelihood-x.upvote_likelihood
    x['person_agreement']=x.participant*10+x.agreement
    x['person_subreddit']=x.participant*20+x.subreddit
    same_agreement=participant_contrasts(x,'person_agreement')
    same_subreddit=participant_contrasts(x,'person_subreddit')
    communities=[]
    for sub,g in x.groupby('subreddit'):
        a=g[g.incongruency==1]; b=g[g.incongruency==0]
        communities.append({'subreddit_code':int(sub),'records':len(g),'incongruent_n':len(a),
          'contrast':None if not len(a) or not len(b) else float(a.comment_likelihood.mean()-b.comment_likelihood.mean())})
    return {'provenance':{'author_repository':'https://github.com/StanfordHCI/spiral-of-silence',
                          'source_blob_sha1':SOURCE_SHA,'local_data_kind':'encoded, pseudonymized derived columns (not raw author CSV)'},
      'audit':audit,'cells':cell,
      'same_person':{'n':len(ps),'mean_diff':float(np.mean(ps)),'bootstrap95':percent_ci(ps,n=boot)},
      'same_item':{'n':len(item),'mean_diff_unweighted':float(np.mean(itemdiff)),
                   'bootstrap95_item_level':percent_ci(itemdiff,seed=23008,n=boot),
                   'n_both_group_rows':int(sum(x['n_incongruent']+x['n_congruent'] for x in item)),
                   'signs':dict(negative=int(sum(x<0 for x in itemdiff)),zero=int(sum(x==0 for x in itemdiff)),positive=int(sum(x>0 for x in itemdiff)))},
      'fixed_effects':{k:fe(df,f) for k,f in formulas.items()},
      'secondary_outcomes':{'upvote_twfe':fe(x,'upvote_likelihood ~ incongruency + agreement + C(participant) + C(item)'),
       'comment_minus_upvote_twfe':fe(x,'comment_minus_upvote ~ incongruency + agreement + C(participant) + C(item)')},
      'same_person_same_agreement':{'n':len(same_agreement),'mean_diff':float(np.mean(same_agreement))},
      'same_person_same_subreddit':{'n':len(same_subreddit),'mean_diff':float(np.mean(same_subreddit))},
      'community_descriptives':communities,
      'noncausal_warning':'Incongruency is mechanically determined by perception of community agreement; observational survey and selected items; FE estimates cannot identify sanctions or real posts.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).with_name('DERIVED_NUMERIC_ROWS.txt'));p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULTS.json'));p.add_argument('--bootstrap',type=int,default=10000);a=p.parse_args()
    df=decode(a.input.read_text(encoding='ascii'))
    result=analyze(df,a.bootstrap)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with a.output.with_name('ITEM_COMPARISONS.csv').open('w',newline='',encoding='utf-8') as f:
        records=item_contrasts(df);w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
    print(json.dumps({'audit':result['audit'],'FE':result['fixed_effects'],'item':result['same_item']},indent=2))
if __name__=='__main__':main()