#!/usr/bin/env python3
"""R311 S107 third-route exact Fraction/BFS oracle. Internal nonblind E1."""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter

V = (F(0), F(1, 2), F(1))
E = (F(0), F(1, 4), F(1, 2), F(1))

def main():
    connected_counts, clique_counts, gap_counts = Counter(), Counter(), Counter()
    false_positive = 0
    for opinions in product(V, repeat=4):
        observations = []
        for radius in E:
            neighbors = [set() for _ in range(4)]
            for i, j in combinations(range(4), 2):
                if abs(opinions[i] - opinions[j]) <= radius:
                    neighbors[i].add(j)
                    neighbors[j].add(i)
            visited, pending = {0}, [0]
            while pending:
                current = pending.pop()
                for neighbor in neighbors[current] - visited:
                    visited.add(neighbor)
                    pending.append(neighbor)
            connected = len(visited) == 4
            clique = sum(map(len, neighbors)) == 12
            observations.append((connected, clique))
            false_positive += connected and not clique
        c = next(radius for radius, (yes, _) in zip(E, observations) if yes)
        q = next(radius for radius, (_, yes) in zip(E, observations) if yes)
        connected_counts[str(c)] += 1
        clique_counts[str(q)] += 1
        gap_counts[str(q - c)] += 1
    result = dict(connected=dict(connected_counts), clique=dict(clique_counts),
                  gap=dict(gap_counts), connected_not_clique=false_positive,
                  vectors=81, worlds=324)
    if connected_counts != Counter({"0": 3, "1/2": 64, "1": 14}):
        raise ValueError("connected counts mismatch")
    if clique_counts != Counter({"0": 3, "1/2": 28, "1": 50}):
        raise ValueError("clique counts mismatch")
    if gap_counts != Counter({"0": 45, "1/2": 36}):
        raise ValueError("gap counts mismatch")
    if false_positive != 36:
        raise ValueError("false-positive count mismatch")
    print(result)
    print("PASS")

if __name__ == "__main__":
    main()
