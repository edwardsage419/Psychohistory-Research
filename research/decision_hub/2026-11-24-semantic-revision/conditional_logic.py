"""Finite Boolean semantics with shared unknown atoms; synthetic cases only."""
from itertools import product
import json

FORMULAS = {
    'and': ('and','A','B'),
    'or': ('or','A','B'),
    'not': ('not','A'),
    'tautology': ('or','A',('not','A')),
    'contradiction': ('and','A',('not','A')),
    'shared_branch': ('or',('and','A','B'),('and','A',('not','B'))),
}

def eval3(f, env):
    if isinstance(f,str): return env[f]
    op,*children=f
    xs=[eval3(c,env) for c in children]
    if op=='not': return None if xs[0] is None else not xs[0]
    if op=='and': return False if False in xs else True if all(x is True for x in xs) else None
    if op=='or': return True if True in xs else False if all(x is False for x in xs) else None
    raise ValueError(op)

def exact(f,env):
    keys=tuple(env)
    worlds=product(*[(False,True) if env[k] is None else (env[k],) for k in keys])
    outcomes={eval3(f,dict(zip(keys,world))) for world in worlds}
    return next(iter(outcomes)) if len(outcomes)==1 else None

def oracle(name,a,b):
    # Independent simplification for these specific finite formulas.
    if name=='tautology': return True
    if name=='contradiction': return False
    if name=='shared_branch': return a
    if name=='not': return None if a is None else not a
    if name=='and': return False if a is False or b is False else True if a is True and b is True else None
    if name=='or': return True if a is True or b is True else False if a is False and b is False else None
    raise ValueError(name)

def run():
    rows=[]
    for (name,f),a,b in product(FORMULAS.items(),(False,True,None),(False,True,None)):
        env={'A':a,'B':b}; v=exact(f,env); k=eval3(f,env); expected=oracle(name,a,b)
        if v!=expected: raise RuntimeError((name,a,b,v,expected))
        if k is not None and k!=expected: raise RuntimeError('unsound baseline')
        rows.append(dict(formula=name,a=a,b=b,kleene=k,exact=v,expected=expected))
    result=dict(cases=len(rows),kleene_correct=sum(r['kleene']==r['expected'] for r in rows),exact_correct=len(rows),extra_resolved=sum(r['kleene'] is None and r['exact'] is not None for r in rows),rows=rows)
    print(json.dumps(result,indent=2))
if __name__=='__main__': run()
