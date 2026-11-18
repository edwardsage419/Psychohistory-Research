# v0.2 DeGroot model and synthetic comparison

## Exact two-agent model

The built-in model `r123-degroot@1.0.0` uses the scalar, fixed-weight specialization of DeGroot’s update. At each integer round it replaces both opinions simultaneously by `x(t+1) = W x(t)`. The two opinions lie in `[0,1]`, and the nonnegative weights in each row sum exactly to 1. The plugin uses Python’s standard library `Fraction` and exchanges canonical rational strings. It supports rounds 0 through 32 and denominator limits that bound the size of exact arithmetic. [DeGroot (1974), *Reaching a Consensus*, p. 120](https://doi.org/10.1080/01621459.1974.10480137)

For the published matrix `[[1/2, 1/2], [1/4, 3/4]]`, R123 records stationary weights `(1/3, 2/3)`. The archived example starts with the project’s chosen `(0,1)` and has a theoretical common limit of `2/3`. The comparison report checks these values and verifies the entire 32-round reference trajectory against an independent recurrence. The receipt hash recorded in the report refers to the file at repository commit `7ea6eab94433e3669b6f492d802bb35316dc90d6`. [Pinned R123 acceptance receipt](../../../research/R123/R123_PHASE_A_ORIGINAL_DEGROOT_BERGER_58_TEST_226_MATRIX_CI_ACCEPTANCE.json)

Write `b = W[0,1]` and `c = W[1,0]`. If `b+c > 0`, the mean `(c*x₀ + b*x₁)/(b+c)` is invariant and the opinion gap is multiplied by `1-b-c` each round. For `0 < b+c < 2`, all initial opinion pairs converge to this mean. When `b+c = 0`, the identity matrix preserves both opinions. When `b+c = 2`, the swap oscillates unless the opinions start equal. The distinction between consensus for a particular input and a guarantee for all inputs follows Berger’s correction discussed in R123. [Pinned R123 report](../../../research/R123/R123_DEGROOT_1974_BERGER_1981_ORIGINAL_CONSENSUS_AND_INFLUENCE_SCIENTIFIC_REPORT_2026-10-19.md)

The report contains a content-addressed base snapshot and two branch snapshots. The branches start from the same opinions and use either the published weights or equal weights. Each branch stores its starting state and every subsequent round. The `parent_hash` points to the shared base, and the payload hash covers the state, branch identity, parent, and events.

## Frozen synthetic comparison

`protocol_spec(seed)` returns the registered JSON profile for the given seed. `run_comparison(spec)` checks the entire profile against the registered version, generates its fixture and validates all rows before fitting any baseline or selecting a model. The two studies each contribute eight training, four validation and eight test sessions with six trials per session. Study, session, and trial identities key separate SHA-256 draws. The seed determines the fixture.

| Partition | Label round | Rows per study | Use |
| --- | ---: | ---: | --- |
| Training | 4 | 48 | Fit a separate event prevalence for each study |
| Validation | 12 | 24 | Select one candidate setting by equal-study mean Brier score |
| Test | 20 | 48 | Score the selected setting and the training-only baselines |

Each trial’s features occur three rounds before the target event and become available one round before it. Cutoff 19 precedes all test labels. The aligned study draws an event with probability `(left + 3*right)/40`, where each integer signal lies in 1 through 9 and the model receives it divided by 10. The weak reversed study uses `(19 - right)/24`. Both observe the same synthetic binary event construct and report the same units and target window.

The candidate uses the first agent’s opinion as a Bernoulli forecast after one, two, or three DeGroot updates. The number of model updates is a candidate setting. The event window stays fixed for all settings. The validation selection breaks ties in favor of fewer updates. Brier score is mean squared error for the event probability. Log loss is the mean negative natural logarithm of the probability assigned to the observed outcome, with that probability floored at `10^-12` to keep contradictory certain forecasts finite.

The report presents each test study and three combined summaries with raw weights `1:1`, `4:1`, and `1:4`. With seed 7, equal weights favor the training-prevalence baseline on both scores. The summary emphasizing the aligned study favors DeGroot on both scores. These are conditional results for two synthetic mechanisms. The report gives empirical predictive validity as `UNKNOWN`.

## Pure interfaces

```python
from psychohistory.degroot import DeGroot
from psychohistory.prediction import protocol_spec, run_comparison

model = DeGroot()
path = model.simulate(model.initial_state(), steps=4)
restored = model.restore_state(model.serialize_state(path[-1]))
report = run_comparison(protocol_spec(7))
```

`synthetic_rows(spec)` materializes the fixture. `validate_split(rows, spec)` verifies the complete dataset shape, group and row uniqueness, measure semantics, and timing, then returns a dictionary keyed by split. `evaluate(rows, forecasts, spec, partition='test')` expects one forecast per row in the selected partition, keyed by `row_id`. Each forecast is a `BERNOULLI` object with a numeric `probability` or a declaration of `UNKNOWN` or `UNIDENTIFIABLE`. A partition with any unknown or unidentifiable forecasts returns a null score and the affected counts. `aggregate(study_results, weights)` combines the two registered model scores for compatible synthetic studies using normalized declared weights. Missing scores in a positive-weight study propagate to the aggregate.
