# R183 source identity: Python import-cache counterexample (bounded static audit)

Date: 2026-11-14 UTC. Starting main: `2fc96b296658082e088e624021142b6aaba50fff`. Scope: R183 native source import integrity only. No frozen research code changed.

## Observed source

`research/R183/r183_logistic_separation_exact.py` blob `d3aba985f8f7c7de21ca12f318f73abaa7fb3b0d`, lines 45–55: `source()` hashes the on-disk R177 Python file and R177 result JSON, then prepends the R177 directory to `sys.path` and executes `from r177_four_finite_count_families_exact import formula_pmf,event_dp`. Python resolves an existing `sys.modules` entry before filesystem import. Therefore the verified on-disk bytes need not be the code object actually used when that module name is already cached.

## Independently executed minimal negative example

Executed with the local Python interpreter, standard library only:

```python
import sys, tempfile, pathlib, hashlib, types
with tempfile.TemporaryDirectory() as d:
    p=pathlib.Path(d)/'pinned_source.py'
    p.write_text('def formula_pmf(): return "trusted"\n')
    expected=hashlib.sha1(b'blob '+str(len(p.read_bytes())).encode()+b'\0'+p.read_bytes()).hexdigest()
    fake=types.ModuleType('pinned_source')
    fake.formula_pmf=lambda: 'substituted'
    sys.modules['pinned_source']=fake
    assert hashlib.sha1(b'blob '+str(len(p.read_bytes())).encode()+b'\0'+p.read_bytes()).hexdigest()==expected
    sys.path.insert(0,d)
    from pinned_source import formula_pmf
    print('pinned_file_hash_match=True; imported_function=',formula_pmf())
```

Observed stdout: `pinned_file_hash_match=True; imported_function= substituted`. Exit code 0.

This establishes the Python import-cache failure mode under a preloaded module. It does **not** establish exploitation in historical R183 CI or native fresh-process execution, and does not show the actual R177 module was substituted. The prior R183 exact arithmetic and archived file hash evidence remains valid within its recorded scope.

## Scientific disposition and handoff

Potential P0 source identity assurance gap, conditional on a pre-populated `sys.modules` entry. Independent native R183 execution and complete output comparison remain outstanding. R mainline owns any core-code change. Candidate bounded remediation: load the exact verified file by explicit path with an isolated module object, or reject preexisting module-name cache entries and verify the loaded module `__file__` resolves to the hashed path; add a negative test injecting a same-name cached module and demonstrate fail-closed behavior. The latter path check alone is weaker if an adversary can spoof module metadata.

Research status unchanged: `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC`; catalogue 08-007 remains provisional. New E2/E3 0. No CI or paid resources invoked.
