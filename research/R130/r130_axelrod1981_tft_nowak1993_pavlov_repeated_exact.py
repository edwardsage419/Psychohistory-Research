#!/usr/bin/env python3
"""R130 exact original Axelrod/Hamilton 1981, Nowak/Sigmund 1993.

Primary original Science 211, 1390-1396, DOI 10.1126/science.7466396
Source Figure1: R=3 S=0 T=5 P=1, p1392; p1393 Eq(1) requires
both TFT defenses: w>=(T-R)/(T-P), w>=(T-R)/(R-S).
Primary original Nature 364, 56-58, DOI 10.1038/364056a0,
p56-57 Pavlov after own outcomes (R,S,T,P)=(1,0,0,1).
R128 used different Skyrms2004 game, no duplicated human E2.
Do NOT claim original 1980 Axelrod tournaments or original Nowak 1993
population mutational evolutionary simulations reexecuted.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json


class RepeatedGamesAuditError(ValueError):
    pass


REWARD=F(3)
SUCKER=F(0)
TEMPTATION=F(5)
PUNISHMENT=F(1)
STRATEGIES=("TFT","ALLD","ALLC","ALT_DC","WSLS")
DELTA_GRID=(F(0),F(1,4),F(1,2),F(3,5),F(2,3),F(4,5),F(9,10))
HORIZONS=(1,2,3,5,8,12)


def _delta(w):
    if type(w) is not F or not F(0)<=w<F(1):
        raise RepeatedGamesAuditError("R130_DISCOUNT_EXACT_FRACTION_0_TO_LESS_THAN_1")
    return w


def _horizon(n, maximum=100):
    if type(n) is not int or not 1<=n<=maximum:
        raise RepeatedGamesAuditError("R130_POSITIVE_INTEGER_HORIZON_BOUNDED")
    return n


def _strategy(s):
    if type(s) is not str or s not in STRATEGIES:
        raise RepeatedGamesAuditError("R130_UNKNOWN_REPEATED_GAME_STRATEGY")
    return s


def stage_payoffs(row,col):
    if type(row) is not str or type(col) is not str or row not in ("C","D") or col not in ("C","D"):
        raise RepeatedGamesAuditError("R130_STAGE_ACTION_C_OR_D_ONLY")
    if row=="C" and col=="C":
        return (REWARD,REWARD)
    if row=="C" and col=="D":
        return (SUCKER,TEMPTATION)
    if row=="D" and col=="C":
        return (TEMPTATION,SUCKER)
    return (PUNISHMENT,PUNISHMENT)


def policy_choice(strategy, own_previous, opponent_previous, turn):
    """Pure public previous realized actions, memory one; ALT has parity."""
    s=_strategy(strategy)
    if type(turn) is not int or turn<0 or turn>10000:
        raise RepeatedGamesAuditError("R130_TURN_NONNEGATIVE_INT")
    if turn==0:
        if own_previous is not None or opponent_previous is not None:
            raise RepeatedGamesAuditError("R130_FIRST_ROUND_HISTORY_MUST_BE_NONE")
    else:
        if own_previous not in ("C","D") or opponent_previous not in ("C","D"):
            raise RepeatedGamesAuditError("R130_LATER_ROUNDS_REQUIRE_BOTH_REALIZED_ACTIONS")
    if s=="ALLD":return "D"
    if s=="ALLC":return "C"
    if s=="ALT_DC":return "D" if turn%2==0 else "C"
    if turn==0:return "C"
    if s=="TFT":return opponent_previous
    # Original Nature 1993 Pavlov: repeat after R or T, switch after S or P.
    earned=stage_payoffs(own_previous,opponent_previous)[0]
    if earned in (REWARD,TEMPTATION):
        return own_previous
    return "D" if own_previous=="C" else "C"


def deterministic_action_pair(row_strategy,col_strategy,previous_pair,turn,
                              forced_row=None,forced_col=None):
    """External forced implementation errors affect executed action only."""
    r=_strategy(row_strategy);c=_strategy(col_strategy)
    if previous_pair is None:
        if turn!=0:
            raise RepeatedGamesAuditError("R130_ROUND0_MUST_HAVE_EMPTY_HISTORY")
        prevrow=prevcol=None
    elif type(previous_pair) in (tuple,list) and len(previous_pair)==2 and all(v in ("C","D") for v in previous_pair):
        if turn==0:
            raise RepeatedGamesAuditError("R130_FIRST_TURN_HISTORY_NONEMPTY")
        prevrow,prevcol=previous_pair
    else:
        raise RepeatedGamesAuditError("R130_MALFORMED_PREVIOUS_ACTIONS")
    a=policy_choice(r,prevrow,prevcol,turn)
    b=policy_choice(c,prevcol,prevrow,turn)
    if forced_row is not None:
        if forced_row not in ("C","D") or type(forced_row) is not str:
            raise RepeatedGamesAuditError("R130_FORCED_ACTION_INVALID")
        a=forced_row
    if forced_col is not None:
        if forced_col not in ("C","D") or type(forced_col) is not str:
            raise RepeatedGamesAuditError("R130_FORCED_ACTION_INVALID")
        b=forced_col
    return a,b


def simulate_explicit_rounds(row_strategy,col_strategy,rounds,
                             initial_forced_row=None, initial_forced_col=None):
    """History/action execution path; no period-detection code invoked."""
    row_strategy=_strategy(row_strategy);col_strategy=_strategy(col_strategy)
    n=_horizon(rounds)
    history=[]
    previous=None
    for t in range(n):
        a,b=deterministic_action_pair(row_strategy,col_strategy,previous,t,
                                      initial_forced_row if t==0 else None,
                                      initial_forced_col if t==0 else None)
        first,second=stage_payoffs(a,b)
        history.append({"round":t,"row":a,"col":b,
                        "row_payoff":first,"col_payoff":second})
        previous=(a,b)
    return tuple(history)


def discounted_explicit_prefix(row_strategy,col_strategy,w,n,
                               initial_forced_row=None,initial_forced_col=None):
    w=_delta(w);n=_horizon(n)
    history=simulate_explicit_rounds(row_strategy,col_strategy,n,initial_forced_row,initial_forced_col)
    first=sum((w**t*h["row_payoff"] for t,h in enumerate(history)),F(0))
    second=sum((w**t*h["col_payoff"] for t,h in enumerate(history)),F(0))
    return first,second


def detect_finite_state_prefix_cycle(row_strategy,col_strategy):
    """Separate path and state-cycle routine. Includes time parity for ALT.

    A state is (previous executed row action, previous executed column
    action, parity of next turn). There are at most 2*5=10 legal states.
    """
    r=_strategy(row_strategy);c=_strategy(col_strategy)
    seen={}
    previous=None
    payoffs=[]
    actions=[]
    for t in range(64):
        state=(previous,t%2)
        if state in seen:
            onset=seen[state]
            cycle=tuple(payoffs[onset:])
            if not cycle:
                raise RepeatedGamesAuditError("R130_EMPTY_DETECTED_ACTION_CYCLE")
            return {
                "prefix_payoffs":tuple(payoffs[:onset]),
                "cycle_payoffs":cycle,
                "prefix_actions":tuple(actions[:onset]),
                "cycle_actions":tuple(actions[onset:]),
                "cycle_start":onset,"cycle_length":len(cycle),
            }
        seen[state]=t
        a,b=deterministic_action_pair(r,c,previous,t)
        actions.append((a,b))
        payoffs.append(stage_payoffs(a,b))
        previous=(a,b)
    raise RepeatedGamesAuditError("R130_FINITE_STRATEGY_MACHINE_NEVER_CYCLED")


def _discount_vector(payoff_tuple,w):
    return tuple(sum((w**k*p[i] for k,p in enumerate(payoff_tuple)),F(0)) for i in range(2))


def independent_infinite_state_cycle_value(row_strategy,col_strategy,w):
    """Exact prefix + one whole cycle / (1-w^L), no numeric truncation."""
    w=_delta(w)
    seq=detect_finite_state_prefix_cycle(row_strategy,col_strategy)
    prefix=seq["prefix_payoffs"];loop=seq["cycle_payoffs"]
    f=_discount_vector(prefix,w);v=_discount_vector(loop,w)
    length=len(loop);start=len(prefix)
    return tuple(f[i]+w**start*v[i]/(1-w**length) for i in range(2))


def independent_state_cycle_tail(row_strategy,col_strategy,w,n):
    """Compute sum of payoff terms FROM N onward without infinite total.

    This is not infinite_total - finite_prefix; uses independent cycle
    decomposition and rotated loop discount mass.
    """
    w=_delta(w);n=_horizon(n)
    s=detect_finite_state_prefix_cycle(row_strategy,col_strategy)
    prefix=s["prefix_payoffs"];cycle=s["cycle_payoffs"]
    start=len(prefix);period=len(cycle)
    if n<start:
        early=tuple(sum((w**t*prefix[t][i] for t in range(n,start)),F(0))
                    for i in range(2))
        circle=_discount_vector(cycle,w)
        return tuple(early[i]+w**start*circle[i]/(1-w**period) for i in range(2))
    rotate=(n-start)%period
    rotated=cycle[rotate:]+cycle[:rotate]
    circle=_discount_vector(rotated,w)
    return tuple(w**n*circle[i]/(1-w**period) for i in range(2))


def original_1981_stability_formulas(w):
    """Exactly both printed Science 1981 p1393 Eq1 inequalities.

    These are pairwise non-invasion payoff conditions, NOT an exhaustive
    new proof of ESS for arbitrary strategies/populations.
    """
    w=_delta(w)
    tft=REWARD/(1-w)
    alld=TEMPTATION+w*PUNISHMENT/(1-w)
    alt=(TEMPTATION+w*SUCKER)/(1-w*w)
    threshold_alld=(TEMPTATION-REWARD)/(TEMPTATION-PUNISHMENT)
    threshold_alt=(TEMPTATION-REWARD)/(REWARD-SUCKER)
    return {
        "original_tft_self_payoff":tft,
        "original_alld_vs_tft_payoff":alld,
        "original_alternating_DC_vs_tft_payoff":alt,
        "original_alld_noninvading_boundary":threshold_alld,
        "original_alt_DC_noninvading_boundary":threshold_alt,
        "original_alld_not_better_than_TFT_self":tft>=alld,
        "original_alt_DC_not_better_than_TFT_self":tft>=alt,
        "both_printed_payoff_defenses_hold":tft>=alld and tft>=alt,
    }


def audit_original_1981_double_constraint():
    results={}
    for w in DELTA_GRID:
        original=original_1981_stability_formulas(w)
        simulated={
            "tft":independent_infinite_state_cycle_value("TFT","TFT",w)[0],
            "alld":independent_infinite_state_cycle_value("ALLD","TFT",w)[0],
            "alt_dc":independent_infinite_state_cycle_value("ALT_DC","TFT",w)[0],
        }
        if (original["original_tft_self_payoff"],
            original["original_alld_vs_tft_payoff"],
            original["original_alternating_DC_vs_tft_payoff"])!=tuple(simulated.values()):
            raise RepeatedGamesAuditError("R130_SOURCE_1981_CLOSED_FORM_VS_STATE_CYCLE_MISMATCH")
        if original["original_alld_not_better_than_TFT_self"]!=(w>=F(1,2)):
            raise RepeatedGamesAuditError("R130_1981_SOURCE_FIRST_BARRIER_DRIFT")
        if original["original_alt_DC_not_better_than_TFT_self"]!=(w>=F(2,3)):
            raise RepeatedGamesAuditError("R130_1981_SOURCE_SECOND_BARRIER_DRIFT")
        results[str(w)]={
            "TFT_self":str(simulated["tft"]),
            "ALLD_vs_TFT":str(simulated["alld"]),
            "ALT_DC_vs_TFT":str(simulated["alt_dc"]),
            "only_ALLD_defense_satisfied":w>=F(1,2) and w<F(2,3),
            "both_noninvasion_comparisons_satisfied":original["both_printed_payoff_defenses_hold"],
        }
    return {
        "original_Source_1981_Fig1_row_payoffs":("3","0","5","1"),
        "original_source_1981_TFT_ALLD_payoff_boundary":"1/2",
        "original_source_1981_TFT_ALT_DC_payoff_boundary":"2/3",
        "original_full_strategy_evolutionary_stability_theorem_newly_reproved":False,
        "w_grid_exact_independent_closed_forms_against_state_cycles":results,
    }


def audited_finite_known_horizon_backward_induction(n):
    """Known public end N, stage D strictly dominates C, finite SPNE path.

    Sufficient assumptions: complete info, unique one-shot pure Nash,
    perfect monitoring. Not a claim about empirical finite experiment play.
    """
    n=_horizon(n,maximum=20)
    for other in ("C","D"):
        if not stage_payoffs("D",other)[0]>stage_payoffs("C",other)[0]:
            raise RepeatedGamesAuditError("R130_ONE_STAGE_D_NOT_STRICTLY_DOMINANT")
    return {"known_terminal_rounds":n,
            "inductively_unique_SPNE_action_path":("D",)*n,
            "real_human_actions_observed":0}


def single_first_round_implementation_error(strategy,rounds=8):
    """First action of row player forced D; no other error after round0."""
    s=_strategy(strategy)
    path=simulate_explicit_rounds(s,s,_horizon(rounds),initial_forced_row="D")
    return tuple(h["row"]+h["col"] for h in path)


def pavlov_original_1993_realized_action_mapping():
    """Next action for row WSLS after own previous actions/outcomes."""
    out={}
    for a,b in product(("C","D"),repeat=2):
        out[a+b]=policy_choice("WSLS",a,b,1)
    if out!={"CC":"C","CD":"D","DC":"D","DD":"C"}:
        raise RepeatedGamesAuditError("R130_ORIGINAL_PAVLOV_R_S_T_P_ORDER_DIVERGED")
    return out


def exhaustive_true_finite_vs_infinite_checks():
    """25 strategy pairs, 7 discounts, 6 horizons = 1050 identities."""
    checks=0
    detailed={}
    for s1,s2 in product(STRATEGIES,repeat=2):
        cycle=detect_finite_state_prefix_cycle(s1,s2)
        if not 1<=cycle["cycle_length"]<=16:
            raise RepeatedGamesAuditError("R130_FINITE_CYCLE_OUT_OF_BOUNDS")
        for w in DELTA_GRID:
            full=independent_infinite_state_cycle_value(s1,s2,w)
            for n in HORIZONS:
                direct=discounted_explicit_prefix(s1,s2,w,n)
                tail=independent_state_cycle_tail(s1,s2,w,n)
                if tuple(direct[i]+tail[i] for i in range(2))!=full:
                    raise RepeatedGamesAuditError("R130_EXPLICIT_FINITE_PLUS_INDEPENDENT_TAIL_NOT_INFINITE")
                checks+=1
            if (s1,s2)==("TFT","TFT") and w==F(3,5):
                detailed={
                    "TFT_TFT_delta":"3/5",
                    "TFT_TFT_infinite_first_player":str(full[0]),
                    "TFT_TFT_detected_period":cycle["cycle_length"],
                }
    if checks!=1050:
        raise RepeatedGamesAuditError("R130_NOT_ALL_1050_CASES_COMPLETE")
    return {
        "strategies":list(STRATEGIES),
        "all_ordered_two_strategy_profiles":len(STRATEGIES)**2,
        "all_discount_values":[str(v) for v in DELTA_GRID],
        "all_explicit_finite_round_counts":list(HORIZONS),
        "exact_finite_prefix_plus_independent_periodic_tail_checks":checks,
        "all_math_checks_use_exact_rational":True,
        "featured_1981_source":detailed,
        "original_1980_Axelrod_computer_tournament_rerun":False,
        "original_1993_Nowak_population_mutation_selection_simulation_rerun":False,
    }


def source_bounded_receipt():
    error_TFT=single_first_round_implementation_error("TFT",8)
    error_Pavlov=single_first_round_implementation_error("WSLS",8)
    if error_TFT!=("DC","CD","DC","CD","DC","CD","DC","CD"):
        raise RepeatedGamesAuditError("R130_TFT_ONE_ERROR_CYCLE_WRONG")
    if error_Pavlov!=("DC","DD","CC","CC","CC","CC","CC","CC"):
        raise RepeatedGamesAuditError("R130_PAVLOV_ONE_ERROR_REPAIR_WRONG")
    return {
        "study":"R130","catalogue":"05-006",
        "source_1981_double_threshold":audit_original_1981_double_constraint(),
        "source_1993_Pavlov_memory_one_action_response":pavlov_original_1993_realized_action_mapping(),
        "finite_exact_strategy_pair_cross_checks":exhaustive_true_finite_vs_infinite_checks(),
        "single_one_sided_mistake_TFT_realized_actions":list(error_TFT),
        "single_one_sided_mistake_Pavlov_realized_actions":list(error_Pavlov),
        "finite_terminal_N5_SPNE_path":list(audited_finite_known_horizon_backward_induction(5)["inductively_unique_SPNE_action_path"]),
        "source_1981_original_tournament_replayed":False,
        "source_1993_original_population_evolution_replayed":False,
        "new_real_human_E2_prediction_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(source_bounded_receipt(),indent=2,sort_keys=True))
