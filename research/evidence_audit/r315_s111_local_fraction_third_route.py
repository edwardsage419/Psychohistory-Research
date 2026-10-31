#!/usr/bin/env python3
"""Third, nonimporting exact route for R315 S111. E1 only.

Independently reconstructs the finite original model. Does not import the
archived R scorer or B JavaScript checker, and does not read human data.
"""
from fractions import Fraction as F
from collections import defaultdict, deque

def ring(n):
    return {tuple(sorted((i, (i+d) % n))) for i in range(n) for d in (1, 2)}

def nbr(edges, vertex):
    return {y if x == vertex else x for x, y in edges if vertex in (x, y)}

def choices(edges, n, vertex, old, p):
    yield ("keep", -1, F(1)-p, edges)
    candidates = [t for t in range(n) if t != vertex and t not in nbr(edges, vertex)]
    for t in candidates:
        updated = edges - {tuple(sorted((vertex, old)))} | {tuple(sorted((vertex, t)))}
        yield ("rewire", t, p / len(candidates), updated)

def metrics(edges, n):
    clustering = []
    for i in range(n):
        a = sorted(nbr(edges, i))
        links = sum(tuple(sorted((x, y))) in edges for j, x in enumerate(a) for y in a[j+1:])
        clustering.append(F(links, len(a)*(len(a)-1)//2) if len(a) > 1 else F(0))
    distances = []
    connected = True
    for i in range(n):
        ds = {i: 0}
        queue = deque([i])
        while queue:
            x = queue.popleft()
            for y in nbr(edges, x):
                if y not in ds:
                    ds[y] = ds[x] + 1
                    queue.append(y)
        connected &= len(ds) == n
        distances.extend(ds[j] for j in range(i+1, n) if j in ds)
    return (sum(clustering, F(0))/n,
            F(sum(distances), n*(n-1)//2) if connected else None,
            1 if connected else 2)

def classify(n):
    ps = (F(0), F(1,2), F(1))
    base = ring(n)
    rows = []
    for p in ps:
        paths = []
        for a, t, w, e1 in choices(base, n, 0, 1, p):
            for b, u, z, e2 in choices(e1, n, 1, 2, p):
                paths.append((a, t, b, u, w*z, tuple(sorted(e2)), metrics(e2, n)))
        assert len(paths) == (19 if n == 8 else 41)
        assert sum((r[4] for r in paths), F(0)) == 1
        rows.append(paths)
    result = {}
    for kind in ("full_labeled_graph", "joint_C_L_components", "C", "L", "components"):
        bins = defaultdict(lambda: [F(0), F(0), F(0)])
        for i, paths in enumerate(rows):
            for a, t, b, u, weight, edges, (c, l, k) in paths:
                if not weight:
                    continue
                key = {"full_labeled_graph": edges,
                       "joint_C_L_components": (c, l, k),
                       "C": c, "L": l, "components": k}[kind]
                bins[key][i] += weight
        accuracy = sum((max(v) for v in bins.values()), F(0)) / 3
        result[kind] = (len(bins), str(accuracy))
    worlds = []
    for p, paths in zip(ps, rows):
        ec = sum((w*m[0] for _,_,_,_,w,_,m in paths), F(0))
        connected = sum((w for _,_,_,_,w,_,m in paths if m[2] == 1), F(0))
        el = sum((w*m[1] for _,_,_,_,w,_,m in paths if m[2] == 1), F(0))
        worlds.append((str(p), str(ec), str(connected),
                       str(el/connected) if connected else None,
                       sum(w > 0 for _,_,_,_,w,_,m in paths)))
    return result, worlds

EXPECTED = {
    8: {"full_labeled_graph": (19, "5/6"),
        "joint_C_L_components": (12, "13/16"), "C": (12, "13/16"),
        "L": (1, "1/3"), "components": (1, "1/3")},
    10: {"full_labeled_graph": (41, "5/6"),
         "joint_C_L_components": (27, "5/6"), "C": (19, "5/6"),
         "L": (5, "89/120"), "components": (1, "1/3")}
}
EXPECTED_WORLDS = {
    8: [("0", "1/2", "1", "10/7", 1),
        ("1/2", "611/1280", "1", "10/7", 19),
        ("1", "1403/2880", "1", "10/7", 12)],
    10: [("0", "1/2", "1", "5/3", 1),
         ("1/2", "3259/7200", "1", "4411/2700", 41),
         ("1", "31/72", "1", "1084/675", 30)]
}
if __name__ == "__main__":
    for n in (8, 10):
        observed, worlds = classify(n)
        assert observed == EXPECTED[n], (n, observed)
        assert worlds == EXPECTED_WORLDS[n], (n, worlds)
    print("PASS R315 S111 independent Python Fraction/BFS: 180 paths, 10 accuracy cells, 6 worlds")
