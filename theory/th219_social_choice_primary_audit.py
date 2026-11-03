"""复核 Arrow 1950 和 Sen 1970 原刊示例的有限算术与逻辑。"""


def check(condition, label):
    """在普通及 Python -O 模式中均执行，避免 assert 被优化删除。"""
    if not condition:
        raise AssertionError(label)


def rank_scores(rankings, alternatives):
    """对每张排序表按当前候选数递减的位置权重计分。"""
    n = len(alternatives)
    scores = {a: 0 for a in alternatives}
    for ranking in rankings:
        remaining = [a for a in ranking if a in alternatives]
        check(len(remaining) == n, "invalid profile")
        for position, a in enumerate(remaining):
            scores[a] += n - position
    return scores


def prefers(ordering, better, worse):
    return ordering.index(better) < ordering.index(worse)


def main():
    # Arrow (1950) pp.337–338：删去y，原唯一胜者x变成与z并列。
    profiles = [("x", "y", "z", "w"), ("x", "y", "z", "w"),
                ("z", "w", "x", "y")]
    full = rank_scores(profiles, ("x", "y", "z", "w"))
    reduced = rank_scores(profiles, ("x", "z", "w"))
    check(full == {"x": 10, "y": 7, "z": 8, "w": 5}, "Arrow full scores")
    check(reduced == {"x": 7, "z": 7, "w": 4}, "Arrow reduced scores")
    check(all(prefers(p, "x", "y") for p in profiles), "Arrow Pareto dominance")
    check([a for a, s in full.items() if s == max(full.values())] == ["x"], "Arrow full winner")
    check({a for a, s in reduced.items() if s == max(reduced.values())} == {"x", "z"}, "Arrow tie")

    # Sen (1970) p.155：个人权利两条边及全体严格偏好一条边成环。
    person1 = ("z", "x", "y")
    person2 = ("x", "y", "z")
    check(prefers(person1, "z", "x"), "Sen person1 right")
    check(prefers(person2, "y", "z"), "Sen person2 right")
    check(all(prefers(p, "x", "y") for p in (person1, person2)), "Sen strict Pareto")
    social_edges = {("z", "x"), ("y", "z"), ("x", "y")}
    candidates = {"x", "y", "z"}
    check(all(any((other, candidate) in social_edges for other in candidates
                  if other != candidate) for candidate in candidates), "Sen incoming edges")
    check(not any(all((other, candidate) not in social_edges for other in candidates
                      if other != candidate) for candidate in candidates), "Sen no best option")
    print("TH219: 10 substantive checks PASS; human/history validation NOT_RUN")


if __name__ == "__main__":
    main()
