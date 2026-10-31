#!/usr/bin/env python3
"""F009 phase39 synthetic TSA compromise and second-witness review gate."""
from collections import Counter
from itertools import product
FIELDS=('signer_valid','tsa_compromised','second_tsa_valid',
        'second_root_independent','audit_available','revocation_fresh',
        'human_recovery_approved','token_precedes_compromise')
def decide(state):
 s=dict(zip(FIELDS,state))
 if not s['signer_valid']:
  return 'REJECT'
 if not s['revocation_fresh'] or not s['human_recovery_approved']:
  return 'UNKNOWN'
 if s['tsa_compromised']:
  if not (s['second_tsa_valid'] and s['second_root_independent'] and s['audit_available']):
   return 'UNKNOWN'
  return 'REVIEW_SECOND_WITNESS_ONLY'
 if not s['audit_available']:
  return 'UNKNOWN'
 return 'REVIEW_PRIMARY'
def require(cond,msg):
 if not cond: raise ValueError(msg)
def main():
 counts=Counter()
 states=list(product((False,True),repeat=len(FIELDS)))
 for state in states:
  s=dict(zip(FIELDS,state))
  v=decide(state)
  counts[v]+=1
  require(v!='AUTO_EXECUTE','unexpected execution')
  if not s['signer_valid']: require(v=='REJECT','invalid signer accepted')
  if s['tsa_compromised'] and v.startswith('REVIEW'):
   require(v=='REVIEW_SECOND_WITNESS_ONLY','compromised TSA trusted')
   require(s['second_tsa_valid'] and s['second_root_independent'] and s['audit_available'],'second witness missing')
  if not s['revocation_fresh'] or not s['human_recovery_approved']:
   require(not v.startswith('REVIEW'),'stale or unapproved review')
  flipped=dict(s)
  flipped['token_precedes_compromise']=not s['token_precedes_compromise']
  require(decide(tuple(flipped[k] for k in FIELDS))==v,'token time restored trust')
 require(len(states)==256 and counts==Counter({'REJECT':128,'UNKNOWN':118,'REVIEW_PRIMARY':8,'REVIEW_SECOND_WITNESS_ONLY':2}),'unexpected counts')
 print('PASS F009 phase39 256 states:',dict(counts))
if __name__=='__main__':
 main()
