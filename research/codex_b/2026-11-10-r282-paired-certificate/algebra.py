"""Independent GF(2) compilation/rank proof of frozen R282 paired counts.

Six columns are a0,b0,eA0,eB0,eA1,eB1 (bit0 is the first variable).
Coefficient rows encode XOR linear forms, not source-index binary numbers.
No original simulator, inverse oracle, CSV or archived counts are imported.
"""
SCHEDULES = ("SYNC", "A_THEN_B", "B_THEN_A")
# One-step coefficient rows over (old_a,old_b,eA,eB), from frozen definitions.
STEP_ROWS = {"SYNC": (6,9), "A_THEN_B": (6,14), "B_THEN_A": (13,9)}


def require(value, reason):
    if not value: raise ValueError(reason)


def rank(rows):
    require(type(rows) in (tuple,list) and all(type(r) is int and 0 <= r < 64 for r in rows), "GF2_ROWS")
    basis = {}
    for value in rows:
        while value:
            pivot = value.bit_length()-1
            if pivot in basis: value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def linear_states(schedule):
    require(type(schedule) is str and schedule in SCHEDULES, "UNFROZEN_SCHEDULE")
    states = [(1,2)]
    for innovations in ((4,8),(16,32)):
        old = states[-1]+innovations
        result = []
        for row in STEP_ROWS[schedule]:
            value = 0
            for column, expression in enumerate(old):
                if row & (1<<column): value ^= expression
            result.append(value)
        states.append(tuple(result))
    return tuple(states)


def evaluate(mask, bits):
    require(type(mask) is int and 0 <= mask < 64 and type(bits) is str and
            len(bits) == 6 and set(bits) <= {"0","1"}, "GF2_EVALUATION_INPUT")
    variables = sum(int(bit)<<column for column,bit in enumerate(bits))
    return (variables & mask).bit_count()%2


def certificates():
    synchronous = linear_states("SYNC")
    found = []
    for schedule in SCHEDULES[1:]:
        states = linear_states(schedule)
        for time in (1,2):
            difference = [x^y for x,y in zip(states[time],synchronous[time])]
            dimension = rank(difference)
            equal = 1 << (6-dimension)
            found.append({"schedule": schedule, "compared_to": "SYNC", "time": time,
                          "difference_masks": difference, "rank": dimension,
                          "equal_count": equal, "disagreement_count": 64-equal,
                          "source_count": 64})
    return found


def paired_counts():
    proof = certificates()
    return {schedule: [row["disagreement_count"] for row in proof if row["schedule"] == schedule]
            for schedule in SCHEDULES[1:]}
