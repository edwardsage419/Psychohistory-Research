"""R166 exact one-step comparison, corrected arithmetic-count runner.
The original first-attempt script is preserved unchanged for failure provenance.
Requires Python standard library and frozen R166_EXACT_RESULTS.json.
"""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE / "r166_one_step_identifiability_20261026.py"
spec = importlib.util.spec_from_file_location("r166_first_attempt", OLD)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

original = json.loads(mod.ORIGINAL.read_text(encoding="utf-8"))
frozen = {(x["N"], x["regime"], x["mechanism"]): x["rows"] for x in original["kernels"]}
assert len(frozen) == 12
rows_verified = 0
for n in mod.N_GRID:
    for regime in mod.REGIMES:
        for mechanism in mod.MECHANISMS:
            for k in range(n + 1):
                generated = mod.binomial_count_distribution(
                    n, mod.success_probability(n, k, regime, mechanism))
                assert [str(x) for x in generated] == frozen[n, regime, mechanism][k]
                rows_verified += 1
assert rows_verified == 84

cases = []
neutral = 0
for n in mod.N_GRID:
    for regime in mod.REGIMES:
        for k in range(n + 1):
            a = mod.binomial_count_distribution(n, mod.success_probability(n, k, regime, "selection"))
            b = mod.binomial_count_distribution(n, mod.success_probability(n, k, regime, "transformation"))
            tv = mod.tv_distance(a, b)
            if regime == "neutral":
                assert tv == 0
                neutral += 1
            else:
                cases.append({
                    "N": n, "k": k, "regime": regime, "p": str(F(k, n)),
                    "TV": str(tv), "equal_prior_Bayes_error": str((1 - tv) / 2),
                    "equal": tv == 0
                })
assert len(cases) == 28 and neutral == 14
assert sum(x["equal"] for x in cases) == 8
assert sum(not x["equal"] for x in cases) == 20
mutant = mod.binomial_count_distribution(4, F(5, 8))
reference = mod.binomial_count_distribution(4, F(2, 3))
mutant_tv = mod.tv_distance(mutant, reference)
assert mutant_tv > 0

out = {
    "id": "R166", "evidence": "E1_SYNTHETIC_ONLY",
    "frozen_kernels": len(frozen), "frozen_rows_verified": rows_verified,
    "nonneutral_conditions": len(cases), "neutral_controls": neutral,
    "identical_nonneutral": 8, "different_nonneutral": 20,
    "mutant_q": "5/8", "mutant_TV": str(mutant_tv),
    "postexecution_arithmetic_correction": True,
    "cases": cases, "E2_new": 0, "E3_new": 0,
}
print(json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True))
