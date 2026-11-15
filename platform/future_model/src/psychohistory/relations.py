"""Mechanism graph contracts; simulation never confers identified causal status."""
KINDS={'ASSOCIATION','CANDIDATE_CAUSAL','IDENTIFIED_CAUSAL','DYNAMIC_FEEDBACK','CROSS_SCALE','THEORY_CONFLICT','COMPLEMENT','COMPETING_EXPLANATION'}

def validate_relations(relations):
    for r in relations:
        if r.get('kind') not in KINDS:
            raise ValueError('Unknown relationship type')
        if not all(k in r for k in ['source','assumptions','time_semantics','verification','limitations']):
            raise ValueError('Relationship provenance required')
        if r['kind']=='IDENTIFIED_CAUSAL' and (r['verification']!='INDEPENDENTLY_IDENTIFIED' or not r.get('identification_protocol') or r['source']=='SYNTHETIC'):
            raise ValueError('Causal identification not established')
    return relations

def validate_schedule(edges):
    graph={}
    for a,b,delay in edges:
        if type(delay)!=int or delay<0: raise ValueError('Invalid synchronization delay')
        if delay==0:graph.setdefault(a,[]).append(b)
    seen,active=set(),set()
    def visit(a):
        if a in active:raise ValueError('Undefined simultaneous feedback cycle')
        if a in seen:return
        active.add(a)
        for b in graph.get(a,[]):visit(b)
        active.remove(a);seen.add(a)
    for a in graph:visit(a)

class ContinuousIntegrator:
    """Extension boundary; no continuous solver is falsely advertised."""
    def advance(self, state, dt):
        raise NotImplementedError('Provide a separately versioned, validated continuous integrator')

# Computational causal-analysis modules must be independently versioned and admitted.
# This is a Python structural contract, not an executable estimator or causal claim.
from typing import Protocol

class CausalAnalysisPlugin(Protocol):
    model_id: str
    version: str
    def describe(self) -> dict: ...
    def validate_input(self, record: dict, identification_protocol: dict) -> None: ...
    def estimate(self, record: dict, identification_protocol: dict) -> dict: ...
