#!/usr/bin/env python3
"""Independent finite R127/05-003 audit. Python standard library only.

The constants are transcribed from the PRE-EXISTING 2026-10-20 frozen
protocol. This does not read the 1990 article or import the R127 implementation.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import unittest

SESSIONS = (
    (16,(8,3,2,1,1,1,0),(1,0,0,0,1,1,13)),
    (16,(4,1,3,4,1,3,0),(1,0,1,0,0,1,13)),
    (14,(4,2,5,3,0,0,0),(2,0,0,1,0,2,9)),
    (15,(6,0,8,1,0,0,0),(0,0,0,0,0,2,13)),
    (16,(2,1,9,3,1,0,0),(0,0,0,1,1,3,11)),
    (16,(5,2,5,2,1,0,1),(3,0,0,0,0,5,8)),
    (14,(4,1,2,4,1,1,1),(1,0,0,0,0,3,10)),
)


def check(condition, message):
    if not condition:
        raise ValueError(message)


def cash(efforts, i):
    return Q(3,5) + Q(min(efforts),5) - Q(efforts[i],10)


def alternative(own, others):
    # Independent formula, deliberately does not call cash().
    m = min(own, min(others))
    return Q(6 + 2*m - own,10)


def count_sessions(sessions):
    check(len(sessions)==7, 'missing session')
    totals = [0,0,0,0]
    for n, first, last in sessions:
        check(n in (14,15,16), 'unexpected group size')
        check(len(first)==len(last)==7, 'wrong category count')
        check(all(type(x) is int and x>=0 for x in (*first,*last)), 'invalid category')
        check(sum(first)==sum(last)==n, 'incorrect group margin')
        totals[0] += n
        totals[1] += first[0]
        totals[2] += first[-1]
        totals[3] += last[-1]
    return tuple(totals)


def finite_games():
    profiles=deviations=0
    nash={}
    for n in (2,3,4):
        equilibria=[]
        for e in itertools.product(range(1,8),repeat=n):
            profiles+=1
            is_nash=True
            for i, own in enumerate(e):
                others=e[:i]+e[i+1:]
                observed=cash(e,i)
                candidate_scores=[]
                for k in range(1,8):
                    alternate=e[:i]+(k,)+e[i+1:]
                    s1=cash(alternate,i)
                    s2=alternative(k,others)
                    check(s1==s2, 'independent payoff mismatch')
                    candidate_scores.append(s1)
                    deviations+=1
                max_score=max(candidate_scores)
                check(candidate_scores.count(max_score)==1, 'nonunique best response')
                check(candidate_scores.index(max_score)+1==min(others), 'best reply mismatch')
                if observed!=max_score:
                    is_nash=False
            if is_nash:
                equilibria.append(e)
        check(equilibria==[(x,)*n for x in range(1,8)],'Nash universe mismatch')
        nash[str(n)]=len(equilibria)
    return {'profiles':profiles,'individual_deviation_payoffs':deviations,'strict_nash_by_n':nash}


def risk_2x2():
    scanned=double=conflicts=ties=0
    for a,b,c,d in itertools.product(range(6),repeat=4):
        scanned+=1
        # Two strict pure diagonal Nash in the symmetric two-player game.
        if not (a>c and d>b):
            continue
        double+=1
        aa_loss=a-c
        bb_loss=d-b
        if aa_loss==bb_loss:
            ties+=1
        if (a>d and aa_loss<bb_loss) or (d>a and bb_loss<aa_loss):
            conflicts+=1
        # Independent best-response threshold from payoffs, with exact fractions.
        threshold=Q(d-b,(a-c)+(d-b))
        check(Q(a)*threshold+Q(b)*(1-threshold) ==
              Q(c)*threshold+Q(d)*(1-threshold), 'belief indifference wrong')
    return {'all_integer_symmetric_games':scanned,'two_strict_diagonal_nash':double,
            'pareto_risk_strict_conflict':conflicts,'risk_product_ties':ties}


def audit():
    counts=count_sessions(SESSIONS)
    check(counts==(107,33,2,77),'published aggregate transcription mismatch')
    check(Q(33,107)>Q(30,100) and Q(33,107)<Q(32,100), 'first percentage')
    check(Q(77,107)>Q(71,100) and Q(77,107)<Q(73,100), 'last percentage')
    check(cash((1,1),0)==Q(7,10) and cash((7,7),0)==Q(13,10), 'cash payoffs')
    check([alternative(k,(1,)) for k in range(1,8)]==
          [Q(x,10) for x in (7,6,5,4,3,2,1)],'security ranking')
    games=finite_games()
    check(games['profiles']==2793 and games['individual_deviation_payoffs']==75117,
          'finite enumeration mismatch')
    two=risk_2x2()
    check(two=={'all_integer_symmetric_games':1296,'two_strict_diagonal_nash':225,
                'pareto_risk_strict_conflict':30,'risk_product_ties':55},
          'two-player enumeration mismatch')
    return {'status':'PASS','scope':'INTERNAL_NONBLIND_ARTIFICIAL_E1_AND_PUBLISHED_AGGREGATE_TRANSCRIPTION',
            'source':'2026-10-20 frozen protocol, NOT freshly reread 1990 scan',
            'original_R127_code_imported':False,'participant_rows_loaded':0,
            'session_aggregates':{'participants':counts[0],'period1_choose7':counts[1],
                                  'period1_choose1':counts[2],'period10_choose1':counts[3]},
            'minimum_effort':games,'symmetric_2x2':two,
            'historical_E3':0,'new_real_E2':0,'R073':'FROZEN','PESEN_v0_1':'FROZEN'}


class NegativeControls(unittest.TestCase):
    def test_wrong_session_margin(self):
        x=list(SESSIONS); n,a,b=x[0]; a=list(a); a[0]+=1; x[0]=(n,tuple(a),b)
        with self.assertRaisesRegex(ValueError,'incorrect group margin'):
            count_sessions(x)
    def test_negative_count(self):
        x=list(SESSIONS); n,a,b=x[0]; a=list(a); a[-1]=-1; x[0]=(n,tuple(a),b)
        with self.assertRaisesRegex(ValueError,'invalid category'):
            count_sessions(x)
    def test_missing_session(self):
        with self.assertRaisesRegex(ValueError,'missing session'):
            count_sessions(SESSIONS[:-1])
    def test_payoff_offset(self):
        self.assertNotEqual(cash((1,1),0),Q(1,10))
    def test_risk_tie(self):
        a,b,c,d=4,0,2,2
        self.assertEqual((a-c)**2,(d-b)**2)
    def test_conflict(self):
        a,b,c,d=5,0,4,4
        self.assertTrue(a>d and (a-c)**2<(d-b)**2)
    def test_positive_receipt(self):
        self.assertEqual(audit()['status'],'PASS')


def main():
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(NegativeControls)
    test_result=unittest.TextTestRunner(verbosity=1).run(suite)
    check(test_result.wasSuccessful(),'negative controls failed')
    result=audit()
    result['tests_run']=test_result.testsRun
    result['negative_controls']=6
    result['python_optimization_safe']=True
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
