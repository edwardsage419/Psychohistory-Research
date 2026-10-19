#!/usr/bin/env python3
"""R117 public first-party ROUNDED aggregates and an explicitly invented focus toy.

Cialdini, Reno, Kallgren (1990) JPSP, Figure 1, Study 1:
doi:10.1037/0022-3514.58.6.1015
Schultz, Nolan, Cialdini, Goldstein, Griskevicius (2007), Psychol Sci:
doi:10.1111/j.1467-9280.2007.01917.x

No original subject/household rows, no source raw data reconstruction, no
estimated population uncertainty, no own human E2 test. The source-group
numbers below are directly TRANSCRIBED from published original papers.
"""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json


class NormFocusAuditError(ValueError):
    pass


PAPER_1990_DOI = "10.1037/0022-3514.58.6.1015"
PAPER_2007_DOI = "10.1111/j.1467-9280.2007.01917.x"

# First-party FIGURE 1 printed rounded percentages and group denominators.
# Source ordering is fixed: clean × high, clean × low,
# littered × high, littered × low.
CELLS_1990 = (
    ("clean_high_focus", 31, 6),
    ("clean_low_focus", 50, 14),
    ("littered_high_focus", 24, 54),
    ("littered_low_focus", 34, 32),
)

# Author's printed short-term baseline/followup group means in daily kWh.
# These are PUBLIC AGGREGATES, not participant paired action data.
CELLS_2007 = (
    ("descriptive_only_above_average", 64, "21.47", "20.25"),
    ("descriptive_only_below_average", 79, "10.38", "11.27"),
    ("descriptive_plus_injunctive_above_average", 63, "20.63", "18.91"),
    ("descriptive_plus_injunctive_below_average", 81, "10.34", "10.58"),
)


def _whole(value, name):
    if type(value) is not int or value < 0:
        raise NormFocusAuditError("R117_NONNEGATIVE_INTEGER_REQUIRED_" + name)
    return value


def _published_percent(value):
    if type(value) is not int or not 0 <= value <= 100:
        raise NormFocusAuditError("R117_PRINTED_PERCENT_MUST_BE_INT_0_TO_100")
    return value


def nearest_whole_percent(successes, total):
    """Exact round-half-UP of 100 successes / total, no float rounding drift."""
    yes = _whole(successes, "SUCCESSES")
    n = _whole(total, "GROUP_SIZE")
    if n == 0 or yes > n:
        raise NormFocusAuditError("R117_INVALID_ROUNDED_PERCENT_DENOMINATOR")
    return (200 * yes + n) // (2 * n)


def infer_unique_count_from_rounded_percent(total, published_percent):
    """All integers consistent with the primary author's rounded Figure 1.

    Returns the sole consistent integer, or FAIL CLOSED on ambiguity/impossibility.
    This is NOT independent reading of individual original study records.
    """
    n = _whole(total, "GROUP_SIZE")
    printed = _published_percent(published_percent)
    if n == 0:
        raise NormFocusAuditError("R117_CANNOT_REVERSE_EMPTY_GROUP")
    candidates = [k for k in range(n + 1) if nearest_whole_percent(k, n) == printed]
    if len(candidates) != 1:
        raise NormFocusAuditError("R117_PUBLISHED_ROUNDING_COUNT_NOT_UNIQUE")
    return candidates[0]


def published_1990_figure1_arithmetic():
    rows=[]
    for name,n,pct in CELLS_1990:
        inferred=infer_unique_count_from_rounded_percent(n,pct)
        rows.append({
            "anonymous_source_figure_cell":name,
            "printed_subject_denominator":n,
            "printed_rounded_littering_percent":pct,
            "integer_litter_count_uniquely_inferred_from_printed_rounding":inferred,
            "inferred_fraction_as_text":str(Fraction(inferred,n)),
        })
    clean_high,clean_low,littered_high,littered_low=rows
    printed_clean=clean_high["printed_rounded_littering_percent"]-clean_low["printed_rounded_littering_percent"]
    printed_littered=littered_high["printed_rounded_littering_percent"]-littered_low["printed_rounded_littering_percent"]
    fractions=[Fraction(item["integer_litter_count_uniquely_inferred_from_printed_rounding"],
                        item["printed_subject_denominator"]) for item in rows]
    # [litter high - litter low] - [clean high - clean low]
    exact_did=(fractions[2]-fractions[3])-(fractions[0]-fractions[1])
    return {
        "source_DOI":PAPER_1990_DOI,
        "study_and_material":"Study 1 Figure 1, author's original rounded labels and printed group n",
        "published_groups":rows,
        "total_published_study1_people":sum(row["printed_subject_denominator"] for row in rows),
        "clean_high_minus_low_focus_published_percentage_points":printed_clean,
        "littered_high_minus_low_focus_published_percentage_points":printed_littered,
        "printed_rounded_interaction_difference_in_differences_percentage_points":printed_littered-printed_clean,
        "uniquely_inferred_integer_count_interaction_fraction_exact":str(exact_did),
        "original_article_reports_interaction_significant":True,
        "original_article_says_two_within_environment_simple_contrasts_not_significant":True,
        "original_person_level_experiment_CSV_accessed":False,
        "independent_SPSS_loglinear_significance_reproduced":False,
    }


def _fixed_published_decimal(value):
    if type(value) is not str:
        raise NormFocusAuditError("R117_PUBLISHED_MEANS_MUST_BE_ORIGINAL_DECIMAL_STRINGS")
    try:
        x=Decimal(value)
    except Exception:
        raise NormFocusAuditError("R117_INVALID_PUBLISHED_DECIMAL_MEAN") from None
    if not x.is_finite() or x < 0 or x.as_tuple().exponent != -2:
        raise NormFocusAuditError("R117_EXPECT_TWO_DECIMAL_POSITIVE_OR_ZERO_AUTHOR_MEAN")
    return x


def published_2007_short_term_arithmetic():
    rows=[]
    for name,n,original_baseline,original_followup in CELLS_2007:
        size=_whole(n,"GROUP_SIZE")
        if size == 0:
            raise NormFocusAuditError("R117_SOURCE_GROUP_MUST_NOT_BE_EMPTY")
        baseline=_fixed_published_decimal(original_baseline)
        followup=_fixed_published_decimal(original_followup)
        change=followup-baseline
        rows.append({
            "anonymous_source_published_cell":name,
            "reported_households_n":size,
            "published_daily_kwh_baseline_mean":original_baseline,
            "published_daily_kwh_short_followup_mean":original_followup,
            "simple_difference_of_published_rounded_means_kwh_day":format(change,".2f"),
        })
    return {
        "source_DOI":PAPER_2007_DOI,
        "source_short_term_4_cells":rows,
        "initial_eligible_households_reported":290,
        "source_households_withdrew":3,
        "analyzed_households_reported":sum(row["reported_households_n"] for row in rows),
        "descriptive_only_below_group_boomerang_reported":True,
        "descriptive_plus_injunctive_below_group_change_reported_not_significant":True,
        "household_original_meter_readings_CSV_accessed":False,
        "independent_statistical_uncertainty_computed":False,
        "outcome_unit":"kilowatt_hours_per_day_differences_of_rounded_group_means",
    }


HALF=Fraction(1,2)
BASELINE=HALF
WEIGHT_D=HALF
WEIGHT_I=HALF


def _norm_probability(value, name):
    if type(value) is not Fraction or not 0 <= value <= 1:
        raise NormFocusAuditError("R117_EXACT_PROPORTION_0_TO_1_REQUIRED_"+name)
    return value


def _focus_flag(value, name):
    if type(value) is not bool:
        raise NormFocusAuditError("R117_FOCUS_BOOLEAN_FLAG_REQUIRED_"+name)
    return value


def toy_prosocial_action_probability(
    descriptive, injunctive, *,
    focus_descriptive=False, focus_injunctive=False,
    baseline=BASELINE, weight_descriptive=WEIGHT_D, weight_injunctive=WEIGHT_I,
):
    """Researcher's transparent, bounded toy, NOT authors' fitted equations.

    P(A=1) = baseline + wD*(D-1/2)*focusD + wI*(I-1/2)*focusI.
    An invalid P is rejected, never clipped. D and I denote unlike constructs.
    """
    d=_norm_probability(descriptive, "DESCRIPTIVE")
    i=_norm_probability(injunctive, "INJUNCTIVE")
    fd=_focus_flag(focus_descriptive,"DESCRIPTIVE")
    fi=_focus_flag(focus_injunctive,"INJUNCTIVE")
    b=_norm_probability(baseline,"BASELINE")
    wd=_norm_probability(weight_descriptive,"DESCRIPTIVE_WEIGHT")
    wi=_norm_probability(weight_injunctive,"INJUNCTIVE_WEIGHT")
    p=b + (wd*(d-HALF) if fd else Fraction(0)) + (wi*(i-HALF) if fi else Fraction(0))
    if not 0 <= p <= 1:
        raise NormFocusAuditError("R117_TOY_PROBABILITY_OUT_OF_RANGE_NO_CLIPPING")
    return p


def source_inspired_synthetic_competition():
    """Only invented proportions and channels; source-real aggregates elsewhere."""
    d=Fraction(1,5)
    i=Fraction(9,10)
    toy=lambda fd,fi:toy_prosocial_action_probability(
        d,i,focus_descriptive=fd,focus_injunctive=fi)
    concordant=Fraction(4,5)
    conflicting_descriptive=toy_prosocial_action_probability(
        Fraction(1,5),concordant,focus_descriptive=True)
    conflicting_injunctive=toy_prosocial_action_probability(
        Fraction(1,5),concordant,focus_injunctive=True)
    return {
        "status":"PURE_RESEARCHER_TOY_NOT_HUMAN_REPRODUCTION",
        "P0_no_focus":str(toy(False,False)),
        "P_descriptive_only_low_prosocial_frequency":str(toy(True,False)),
        "P_injunctive_only_high_approval":str(toy(False,True)),
        "P_both_foci_conflicting_cues":str(toy(True,True)),
        "same_descriptive_and_injunctive_signal_only_D":str(
            toy_prosocial_action_probability(concordant,concordant,focus_descriptive=True)),
        "same_descriptive_and_injunctive_signal_only_I":str(
            toy_prosocial_action_probability(concordant,concordant,focus_injunctive=True)),
        "conflict_D_low_I_high_only_D":str(conflicting_descriptive),
        "conflict_D_low_I_high_only_I":str(conflicting_injunctive),
        "public_source_1990_litter_behavior_not_fitted":True,
        "public_source_2007_energy_kwh_not_fitted":True,
        "PESEN_v0_1":"FROZEN",
        "R073":"FROZEN",
    }


def public_aggregate_and_toy_receipt():
    return {
        "research_id":"R117",
        "phase":"A",
        "source_1990_published_figure_arithmetic":published_1990_figure1_arithmetic(),
        "source_2007_published_shortterm_arithmetic":published_2007_short_term_arithmetic(),
        "researcher_invented_probability_counterexamples":source_inspired_synthetic_competition(),
        "no_original_human_individual_rows":True,
        "new_original_human_E2_scores":0,
        "causal_normative_mechanism_newly_estimated":False,
    }


if __name__ == "__main__":
    print(json.dumps(public_aggregate_and_toy_receipt(), sort_keys=True, indent=2))
