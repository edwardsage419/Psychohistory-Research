#!/usr/bin/env python3
"""Independent nonblind Fraction audit for R331 S127. No JS imports."""
import hashlib
import json
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path

PAIRS=((F(1,4),F(1,2)),(F(1,4),F(3,4)),(F(1,2),F(3,4)))
WEIGHTS=(F(1,4),F(1,2),F(3,4))

def generate():
    rows=[];groups=[]
    for k,((a,b),w) in enumerate(product(PAIRS,WEIGHTS),1):
        name=f'W{k:02d}'
        s=lambda t:w*a**t+(1-w)*b**t
        h0=1-(w*a+(1-w)*b)
        hazards=[];shares=[]
        for t in range(8):
            x=s(t);y=s(t+1)
            hazard=1-y/x;share=w*a**t/x
            hazards.append(hazard);shares.append(share)
            rows.append(dict(world_id=name,a=str(a),b=str(b),w=str(w),t=t,s_t=str(x),s_t1=str(y),
                             retention=str(y/x),hazard=str(hazard),fast_share=str(share),
                             homogeneous_hazard=str(h0)))
        groups.append(dict(world_id=name,a=str(a),b=str(b),w=str(w),h0=str(h0),h7=str(hazards[-1]),
                           hazard_strictly_decreasing=all(x>y for x,y in zip(hazards,hazards[1:])),
                           fast_share_strictly_decreasing=all(x>y for x,y in zip(shares,shares[1:]))))
    return dict(model='R331_S127_CONSTRUCTED_CONDITIONAL_HAZARD_E1',evidence='E1_CONSTRUCTED_ONLY',
                world_count=9,row_count=72,groups=groups,rows=rows)

def validate(x):
    if x!=generate():raise ValueError('full receipt mismatch')
    return True

class Checks(unittest.TestCase):
    def test_all_worlds(self):
        x=generate();self.assertTrue(validate(x));self.assertEqual(len(x['rows']),72)
        self.assertTrue(all(g['hazard_strictly_decreasing'] and g['fast_share_strictly_decreasing'] for g in x['groups']))
    def test_frozen_example(self):
        x=[r for r in generate()['rows'] if r['world_id']=='W05']
        self.assertEqual([r['hazard'] for r in x[:3]],['1/2','3/8','3/10'])
        self.assertEqual([r['fast_share'] for r in x[:3]],['1/2','1/4','1/10'])
    def test_mutations(self):
        original=generate()
        for i in range(6):
            v=json.loads(json.dumps(original))
            if i==0:v['rows'].pop()
            if i==1:v['rows'][1]=v['rows'][0]
            if i==2:v['rows'][3]['hazard']='99'
            if i==3:v['rows'][3]['fast_share']='99'
            if i==4:v['groups'][0]['hazard_strictly_decreasing']=False
            if i==5:v['evidence']='E2'
            with self.subTest(i=i),self.assertRaises(ValueError):validate(v)

if __name__=='__main__':
    import sys
    if not unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks)).wasSuccessful():raise SystemExit(1)
    b=(json.dumps(generate(),sort_keys=True,separators=(',',':'))+'\n').encode()
    print('bytes',len(b),'sha256',hashlib.sha256(b).hexdigest(),'gitblob',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())
