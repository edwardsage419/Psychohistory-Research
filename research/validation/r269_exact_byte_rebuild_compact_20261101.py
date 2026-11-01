#!/usr/bin/env python3
"""R269 independent, deterministic finite-E1 full-byte source and result oracle."""
import csv
import hashlib
import io
import itertools
import json
from fractions import Fraction as F

SOURCE = '20b33f85a9408655cfbd7bdbfc1de15ec534571e'
RESULT = '4947ccb7a53de1343216e1b69773d0a5c4ea1f29'
SOURCE256 = '6bc98c0c07c2a6d48184e6a8643dbd515dfa470ba626a10928d90614ce75155d'
RESULT256 = 'd7dda54fdd07148713cd8acbaaafb06bc1282a005b48b09f570211e1a7d4193e'
FREEZE = '1ba86be0a35b77c0d5e5f6a72bb102ba08c48795'
PS = (F(1, 4), F(1, 2), F(3, 4))
MODELS = ('GROUP_ID_MEMORIZER', 'GLOBAL_LAPLACE', 'CONSTANT_HALF')
FIELDS = ('world predictor true_p original_six_independent_group_latents '
          'original_complete_source_probability original_twelve_row_groups '
          'original_twelve_row_outcomes loor_row_predictions loor_row_squared_losses '
          'loor_average_brier logo_row_predictions logo_row_squared_losses '
          'logo_average_brier').split()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def rebuild():
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, FIELDS, lineterminator='\n')
    writer.writeheader()
    worlds = []
    for p, model in itertools.product(PS, MODELS):
        label = 'P' + str(p).replace('/', 'OF') + '_' + model
        sums = {'loor': F(0), 'logo': F(0)}
        mass_total = F(0)
        for bits in itertools.product((0, 1), repeat=6):
            k = sum(bits)
            mass = p**k * (1-p)**(6-k)
            mass_total += mass
            row = dict(world=label, predictor=model, true_p=p,
                       original_six_independent_group_latents=''.join(map(str, bits)),
                       original_complete_source_probability=mass,
                       original_twelve_row_groups=';'.join(str(i//2) for i in range(12)),
                       original_twelve_row_outcomes=';'.join(str(bits[i//2]) for i in range(12)))
            for mode in ('loor', 'logo'):
                pred, losses = [], []
                for g, y in enumerate(bits):
                    other = sum(bits[j] for j in range(6) if j != g)
                    if model == 'GROUP_ID_MEMORIZER':
                        q = F(y) if mode == 'loor' else F(1, 2)
                    elif model == 'CONSTANT_HALF':
                        q = F(1, 2)
                    else:
                        q = (F(2*other+y+1, 13) if mode == 'loor'
                             else F(2*other+1, 12))
                    pred.extend((q, q))
                    losses.extend(((F(y)-q)**2,)*2)
                mean = sum(losses, F(0))/12
                row[mode+'_row_predictions'] = ';'.join(map(str, pred))
                row[mode+'_row_squared_losses'] = ';'.join(map(str, losses))
                row[mode+'_average_brier'] = mean
                sums[mode] += mass*mean
            writer.writerow({key: str(row[key]) for key in FIELDS})
        if mass_total != 1:
            raise ValueError('source probability mass')
        expected = ((F(0), F(1,4)) if model == 'GROUP_ID_MEMORIZER' else
                    (F(1,4), F(1,4)) if model == 'CONSTANT_HALF' else
                    ((1+160*p*(1-p))/169, (1+160*p*(1-p))/144))
        if (sums['loor'], sums['logo']) != expected:
            raise ValueError('analytic expectation')
        worlds.append(dict(world=label, true_p=str(p), predictor=model,
                           complete_original_source_types=64,
                           expected_LOOR_Brier=str(sums['loor']),
                           expected_LOGO_Brier=str(sums['logo']),
                           source_enumeration_equals_independent_analytic=True))
    result = dict(research_id='R269', original_catalogue_id='11-029',
                  prescore_freeze_commit=FREEZE,
                  scope='ARTIFICIAL_E1_EXACT_SIX_INDEPENDENT_GROUPS_TWELVE_CORRELATED_ROWS',
                  world_count=9, source_types=576,
                  distinct_group_latent_sequences_per_true_p=64,
                  independent_latent_groups_per_source=6,
                  observed_repeated_rows_per_source=12,
                  row_leave_one_out_folds_per_source=12,
                  leave_one_group_out_folds_per_source=6,
                  each_observation_scored_once_each_protocol=True,
                  all_nine_independent_Binomial5_Bernoulli1_expected_scores_verified=True,
                  no_genuine_human_out_of_sample_evidence=True,
                  new_real_human_E2=0, new_real_historical_E3=0,
                  R073='FROZEN', PESEN_v0_1='FROZEN', world_results=worlds)
    src = out.getvalue().encode()
    res = (json.dumps(result, indent=2, ensure_ascii=False)+'\n').encode()
    return src, res


def main():
    src, res = rebuild()
    checks = {'source_git_blob': blob(src)==SOURCE,
              'result_git_blob': blob(res)==RESULT,
              'source_sha256': hashlib.sha256(src).hexdigest()==SOURCE256,
              'result_sha256': hashlib.sha256(res).hexdigest()==RESULT256}
    print(json.dumps({'status': 'COMPLETE' if all(checks.values()) else 'FAIL',
                      'source_rows': 576, 'worlds': 9,
                      'prediction_cells': 13824, 'loss_cells': 13824,
                      'source_bytes': len(src), 'result_bytes': len(res),
                      'checks': checks}, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
