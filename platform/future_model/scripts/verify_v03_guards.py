"""Run scientific and compatibility checks in the current (possibly optimized) stdlib interpreter."""
import json
import sys

from psychohistory.degroot import DeGroot
from psychohistory.prediction import protocol_spec, run_comparison
from psychohistory.replicator import normalize_parameters, run_trajectory, verify_archived_cases


def reject(label, call):
    try:
        call()
    except (ValueError, ArithmeticError) as error:
        return {'check': label, 'failure': str(error)}
    raise RuntimeError(f'Unsafe acceptance of {label}')


params = {'initial': ['1/2', '1/2'], 'payoff': [['-2', '2'], ['0', '1']],
          'method': 'euler', 'steps': 1, 'step_size': '4'}
result = {
    'optimization': sys.flags.optimize,
    'degroot': DeGroot().verify_reference(),
    'replicator': verify_archived_cases(),
    'refusals': [
        reject('non-simplex', lambda: normalize_parameters({**params, 'initial': ['0', '0']})),
        reject('Eq3 with ODE step size', lambda: normalize_parameters({**params, 'method': 'eq3'})),
        reject('Euler step outside allowed states', lambda: run_trajectory({
            **params, 'initial': ['3/4', '1/4']})),
        reject('empirical v2 comparison', lambda: run_comparison({**protocol_spec(7), 'scope': 'EMPIRICAL'})),
    ],
}
print(json.dumps(result, sort_keys=True, allow_nan=False))
