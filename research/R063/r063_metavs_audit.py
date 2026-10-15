#!/usr/bin/env python3
"""R063 Najar 2020 VS2 / metaVS state transition audit.

This is an independent, deliberately narrow Python translation of the
model UPDATE and private-choice log-likelihood branches from author MATLAB:
  models/VS/VS2.m   blob 66c8f9638e97179ad9ab625c7b0b475a5d34906b
  models/VS/metaVS.m blob cc6e92af0945a2afe4c4f84dcd310a75b5de5a31

It is NOT a replication of source fitting, participant preprocessing,
publication AIC, or local trial-by-trial participant findings.
No synthetic traces are represented as human data.

Choice codes below are 0/1, corresponding to author's MATLAB 1/2.
Call simulate separately per session or separately per desired input block;
MATLAB models themselves reset once per model function call. We do not claim
that R061's particular session segmentation duplicates author fit calls.
"""
from dataclasses import dataclass
from math import exp, log1p
from collections import defaultdict
import argparse
import json

SOURCE_COMMIT = '554ee8007ff6fd1c51cd68d7d254f22a34e6dab1'
SOURCE_BLOBS = {
    'VS2': '66c8f9638e97179ad9ab625c7b0b475a5d34906b',
    'metaVS': 'cc6e92af0945a2afe4c4f84dcd310a75b5de5a31',
}

@dataclass(frozen=True)
class Parameters:
    beta: float = 2.0
    alpha_private: float = 0.2
    alpha_social_or_meta: float = 0.03
    perseveration: float = 0.0


def softplus(z):
    return max(z, 0.0) + log1p(exp(-abs(z)))


def validate_event(e):
    if e['kind'] not in ('private', 'demo'):
        raise ValueError('kind must be private or demo')
    if not isinstance(e['state'], int) or e['state'] < 1:
        raise ValueError('state must be positive integer')
    if e['choice'] not in (0, 1):
        raise ValueError('choice must be normalized to 0 or 1')
    if e['kind'] == 'private' and e.get('reward') not in (-1, 1):
        raise ValueError('private reward must be +1/-1')
    if e['kind'] == 'demo' and e.get('reward') is not None:
        raise ValueError('demonstrator reward must be unobserved')


def simulate(events, params, family='metaVS'):
    """Return temporal state trace and pre-outcome private-choice mean logloss."""
    if family not in ('VS2', 'metaVS'):
        raise ValueError('family must be VS2 or metaVS')
    if not 0 <= params.alpha_private <= 1 or not 0 <= params.alpha_social_or_meta <= 1:
        raise ValueError('audit domain: learning rates 0..1')
    if params.beta < 0:
        raise ValueError('beta must be nonnegative')
    q = defaultdict(lambda: [0.0, 0.0])
    last = {}
    dynamic = defaultdict(float)
    trace = []
    total_logloss, n = 0.0, 0
    for t, event in enumerate(events):
        e = dict(event)
        validate_event(e)
        s, choice = e['state'], e['choice']
        other = 1 - choice
        oldq = q[s][:]
        old_rate = dynamic[s]
        target = None
        loss = None
        if e['kind'] == 'private':
            biased_q = q[s][:]
            if s in last:
                biased_q[last[s]] += params.perseveration
            logit = params.beta * (biased_q[1] - biased_q[0])
            loss = softplus(-logit if choice == 1 else logit)
            total_logloss += loss
            n += 1
            r = e['reward']
            # Source updates both chosen and unchosen options using +/- own reward.
            q[s][choice] += params.alpha_private * (r - q[s][choice])
            q[s][other] += params.alpha_private * (-r - q[s][other])
            last[s] = choice
        else:
            if family == 'metaVS':
                # MATLAB max(Q) breaks ties by returning first of two options.
                if s in last:
                    best = 0 if q[s][0] >= q[s][1] else 1
                    target = int(choice == best)
                    dynamic[s] += params.alpha_social_or_meta * (target - dynamic[s])
                rate = dynamic[s]
            else:
                rate = params.alpha_social_or_meta
            q[s][choice] += rate * (1.0 - q[s][choice])
            q[s][other] += rate * (-1.0 - q[s][other])
        trace.append({
            't': t, 'kind': e['kind'], 'state': s, 'choice': choice,
            'old_q': oldq, 'new_q': q[s][:],
            'prior_dynamic_rate': old_rate,
            'effective_social_rate': dynamic[s] if family == 'metaVS' else params.alpha_social_or_meta,
            'target': target, 'private_loss_before_reward': loss,
        })
    return {'family': family, 'private_rows': n,
            'mean_private_logloss': total_logloss / n if n else None,
            'trace': trace}


def illustrative_trace():
    p = Parameters(alpha_private=0.2, alpha_social_or_meta=0.03)
    events = [{'kind': 'private', 'state': 1, 'choice': 0, 'reward': 1}]
    events += [{'kind': 'demo', 'state': 1, 'choice': 0} for _ in range(20)]
    events += [{'kind': 'private', 'state': 1, 'choice': 0, 'reward': 1}]
    meta = simulate(events, p, 'metaVS')
    fixed = simulate(events, p, 'VS2')
    return {'kind': 'SYNTHETIC_MECHANISM_CHECK', 'params': vars(p),
            'expected_meta_rate_after_20_concordant_demos': 1 - .97**20,
            'meta_final_rate': meta['trace'][20]['effective_social_rate'],
            'fixed_rate': fixed['trace'][20]['effective_social_rate'],
            'meta_Q_after_20_demos': meta['trace'][20]['new_q'],
            'fixed_Q_after_20_demos': fixed['trace'][20]['new_q'],
            'final_private_loss_meta': meta['trace'][21]['private_loss_before_reward'],
            'final_private_loss_fixed': fixed['trace'][21]['private_loss_before_reward']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--example', action='store_true', help='Output synthetic mechanism example')
    args = parser.parse_args()
    if args.example:
        print(json.dumps(illustrative_trace(), indent=2, ensure_ascii=False))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
