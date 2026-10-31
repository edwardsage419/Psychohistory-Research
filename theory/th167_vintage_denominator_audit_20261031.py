"""TH167: deterministic public-text arithmetic and synthetic sensitivity audit.

No network access, no private data, no empirical causal estimation.
"""
from fractions import Fraction


def check():
    old = {'district_mandals':405, 'excluded_started':51, 'excluded_other':1,
           'treatment':113, 'buffer':195, 'control':45,
           'gps':886, 'endline_sampled':8826, 'endline_untraced':268,
           'endline_ghost':386, 'endline_usable':8172,
           'baseline_sampled':8579, 'baseline_untraced':899,
           'baseline_ghost':298, 'baseline_usable':7382}
    new = {'district_mandals':405, 'excluded_urban':2, 'excluded_started':106,
           'excluded_no_strata':1, 'treatment':112, 'buffer':139, 'control':45,
           'gps':880, 'endline_sampled':8774, 'endline_untraced':287,
           'endline_missing_survey':8, 'endline_ghost':365,
           'endline_usable':8114, 'baseline_sampled':8527,
           'baseline_untraced':1000, 'baseline_ghost':102,
           'baseline_usable':7425}
    assert old['district_mandals']-old['excluded_started']-old['excluded_other']==353
    assert old['treatment']+old['buffer']+old['control']==353
    assert new['district_mandals']-new['excluded_urban']-new['excluded_started']-new['excluded_no_strata']==296
    assert new['treatment']+new['buffer']+new['control']==296
    assert (old['treatment']-new['treatment'],old['buffer']-new['buffer'],old['control']-new['control'])==(1,56,0)
    assert 353-296==57 and 109-52==57
    assert (15*5+16+10+12, 15*6+10+12)==(113,112)
    assert (6*127+4*31,6*126+4*31)==(886,880)
    assert old['endline_sampled']-old['endline_untraced']-old['endline_ghost']==old['endline_usable']
    assert new['endline_sampled']-new['endline_untraced']-new['endline_missing_survey']-new['endline_ghost']==new['endline_usable']
    assert old['baseline_sampled']-old['baseline_untraced']-old['baseline_ghost']==old['baseline_usable']
    assert new['baseline_sampled']-new['baseline_untraced']-new['baseline_ghost']==new['baseline_usable']
    assert 8572-1000-102==7470 and 7470-7425==45
    assert 8527-1000-102==7425
    assert 287+8==295
    bound=Fraction(1,113)
    for old_removed in (Fraction(0),Fraction(1)):
        for retained_mean in (Fraction(0),Fraction(1),Fraction(1,3)):
            mean113=(112*retained_mean+old_removed)/113
            assert abs(retained_mean-mean113)<=bound
    assert abs(Fraction(1)-(112*Fraction(1)+Fraction(0))/113)==bound
    return {'old_randomized':353,'new_randomized':296,'delta':57,
            'old_treated':113,'new_treated':112,
            'nalgonda_treated_old':16,'nalgonda_treated_new':15,
            'old_gps':886,'new_gps':880,
            '2016_main_text_baseline_error':45,
            '2016_appendix_baseline_identity':7425,
            '2016_endline_split':295,
            'synthetic_nested_equal_cluster_bound':str(bound)}


if __name__=='__main__':
    print('TH167 PASS',check())
