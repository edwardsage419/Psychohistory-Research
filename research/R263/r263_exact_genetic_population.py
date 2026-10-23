#!/usr/bin/env python3
"""R263 exact one-generation 3-bit two-parent genetic search and elite selection.

Nine frozen artificial worlds, each 6 original parent bits + one crossover
flag + one crossover-cut bit + two independently fair mutation trigger bits;
1024 sources/world = 9216. All fractional arithmetic and full conditional
offspring-pair laws independently verified against an integer-mask generator.
This is a deliberately restricted one-generation toy, not evidence for long
run GA convergence or biological/historical adaptation.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="e50f54089dac1bab48bd898b3fc1f1dd89c20ebf"
BITS=(0,1);ZERO=F(0);ONE=F(1)
GENOMES=tuple(itertools.product(BITS,repeat=3))
INITIAL_PARENT_PAIRS=tuple(itertools.product(GENOMES,repeat=2))
ALL_10BIT=tuple(itertools.product(BITS,repeat=10))
OPERATOR_4BIT=tuple(itertools.product(BITS,repeat=4))
CONFIG={
 "CLONAL_ONEMAX":(False,False,False,"ONEMAX"),
 "CROSS_ONEMAX":(True,False,False,"ONEMAX"),
 "MUTATE_ONEMAX":(False,True,False,"ONEMAX"),
 "CROSS_MUTATE_ONEMAX":(True,True,False,"ONEMAX"),
 "ELITE_CLONAL_ONEMAX":(False,False,True,"ONEMAX"),
 "ELITE_CROSS_ONEMAX":(True,False,True,"ONEMAX"),
 "ELITE_MUTATE_ONEMAX":(False,True,True,"ONEMAX"),
 "ELITE_CROSS_MUTATE_ONEMAX":(True,True,True,"ONEMAX"),
 "ELITE_CROSS_MUTATE_TRAP":(True,True,True,"TRAP")
}
WORLDS=tuple(CONFIG)
def check(w):
    if w not in CONFIG:raise ValueError("unfrozen two-individual GA world")
def fitness(genome,objective):
    if genome not in GENOMES:raise ValueError("invalid frozen genome")
    n=sum(genome)
    return 4 if objective=="TRAP" and n==0 else n
def direct_bits_source(w,bits):
    """First source route: tuple slicing and explicit immutable bit flips."""
    check(w)
    if len(bits)!=10 or any(b not in BITS for b in bits):
        raise ValueError("10 independent original bits required")
    cross_enabled,mutation_enabled,elite,obj=CONFIG[w]
    p0=tuple(bits[:3]);p1=tuple(bits[3:6])
    crossflag,cutbit,m0,m1=bits[6:]
    if cross_enabled and crossflag:
        cut=1+cutbit
        c0=p0[:cut]+p1[cut:]
        c1=p1[:cut]+p0[cut:]
    else:c0,c1=p0,p1
    if mutation_enabled and m0:
        c0=(1-c0[0],c0[1],c0[2])
    if mutation_enabled and m1:
        c1=(c1[0],c1[1],1-c1[2])
    if elite:
        ranked=sorted(enumerate((p0,p1,c0,c1)),
                      key=lambda t:(-fitness(t[1],obj),t[1],t[0]))
        s0,s1=ranked[0][1],ranked[1][1]
    else:s0,s1=c0,c1
    pb=max(fitness(p0,obj),fitness(p1,obj))
    sb=max(fitness(s0,obj),fitness(s1,obj))
    return p0,p1,c0,c1,s0,s1,pb,sb
def as_int(bits):return bits[0]*4+bits[1]*2+bits[2]
def from_int(n):return ((n>>2)&1,(n>>1)&1,n&1)
def independent_integer_offspring(w,pair,ops):
    """Independent integer mask recombination and mutation, not tuple slicing."""
    check(w)
    cross,mut,elite,obj=CONFIG[w]
    a,b=map(as_int,pair)
    switch,cutbit,m0,m1=ops
    if cross and switch:
        cut=1+cutbit
        low=(1<<(3-cut))-1
        c=(a&~low)|(b&low)
        d=(b&~low)|(a&low)
    else:c,d=a,b
    if mut and m0:c^=4
    if mut and m1:d^=1
    def rank(z):
        score=4 if obj=="TRAP" and z==0 else z.bit_count()
        return -score,z
    if elite:
        choices=[a,b,c,d]
        ranks=sorted(range(4),key=lambda i:(*rank(choices[i]),i))
        surv=(choices[ranks[0]],choices[ranks[1]])
    else:surv=(c,d)
    return tuple(from_int(v) for v in surv)
@lru_cache(None)
def sources(w):
    check(w);rows=[]
    for bits in ALL_10BIT:
        p0,p1,c0,c1,s0,s1,pbest,nbest=direct_bits_source(w,bits)
        row={"world":w,
             "frozen_crossover_enabled":int(CONFIG[w][0]),
             "frozen_mutation_enabled":int(CONFIG[w][1]),
             "frozen_elite_survival":int(CONFIG[w][2]),
             "frozen_objective":CONFIG[w][3]}
        for i in range(10):row[f"oracle_original_bit_{i}"]=bits[i]
        for label,bg in (("parent0",p0),("parent1",p1),
                         ("candidate_child0",c0),("candidate_child1",c1),
                         ("survivor0",s0),("survivor1",s1)):
            row[f"observed_{label}_threebit_genome"]="".join(map(str,bg))
            row[f"observed_{label}_fitness"]=fitness(bg,CONFIG[w][3])
        row["observed_original_parent_best_fitness"]=pbest
        row["observed_next_survivor_best_fitness"]=nbest
        row["observed_next_minus_original_best_fitness"]=nbest-pbest
        row["original_complete_tenbit_source_mass"]=F(1,1024)
        rows.append(row)
    assert len(rows)==1024 and sum((z["original_complete_tenbit_source_mass"] for z in rows),ZERO)==ONE
    return tuple(rows)
def conditional_joint_from_full_sources(w,pair):
    d=defaultdict(F)
    pair_s=("".join(map(str,pair[0])),"".join(map(str,pair[1])))
    rows=(z for z in sources(w) if (z["observed_parent0_threebit_genome"],z["observed_parent1_threebit_genome"])==pair_s)
    for z in rows:
        d[(z["observed_survivor0_threebit_genome"],z["observed_survivor1_threebit_genome"])]+=F(1,16)
    assert sum(d.values(),ZERO)==ONE
    return dict(d)
def conditional_joint_from_independent_int_masks(w,pair):
    d=defaultdict(F)
    for ops in OPERATOR_4BIT:
        survivor=independent_integer_offspring(w,pair,ops)
        d[("".join(map(str,survivor[0])),"".join(map(str,survivor[1])))]+=F(1,16)
    assert sum(d.values(),ZERO)==ONE
    return dict(d)
def independent_distribution_verified(w):
    return all(conditional_joint_from_full_sources(w,pair)==
               conditional_joint_from_independent_int_masks(w,pair)
               for pair in INITIAL_PARENT_PAIRS)
def summary(w):
    rows=sources(w)
    deltas=[z["observed_next_minus_original_best_fitness"] for z in rows]
    return dict(world=w,all_original_tenbit_source_atoms=1024,
        frozen_crossover_enabled=CONFIG[w][0],
        frozen_mutation_enabled=CONFIG[w][1],
        frozen_elitism_enabled=CONFIG[w][2],
        frozen_fitness_objective=CONFIG[w][3],
        exact_parent_best_mean=str(sum((F(z["observed_original_parent_best_fitness"],1024) for z in rows),ZERO)),
        exact_survivor_best_mean=str(sum((F(z["observed_next_survivor_best_fitness"],1024) for z in rows),ZERO)),
        exact_best_fitness_gain_mean=str(sum((F(x,1024) for x in deltas),ZERO)),
        original_sources_fitness_increase=sum(x>0 for x in deltas),
        original_sources_fitness_tie=sum(x==0 for x in deltas),
        original_sources_fitness_decrease=sum(x<0 for x in deltas),
        original_sources_reaching_global_best_fitness=sum(z["observed_next_survivor_best_fitness"]==(4 if CONFIG[w][3]=="TRAP" else 3) for z in rows),
        entire_64_parent_pair_conditioned_survivor_law_verified=independent_distribution_verified(w))
def frozen_claims():
    for w in WORLDS:
        if not independent_distribution_verified(w):
            raise AssertionError(f"{w}: original full source and independent integer mask conditional law differ")
        stats=summary(w)
        assert stats["original_sources_fitness_increase"]+stats["original_sources_fitness_tie"]+stats["original_sources_fitness_decrease"]==1024
        if CONFIG[w][2]:
            assert stats["original_sources_fitness_decrease"]==0
        if w=="CLONAL_ONEMAX":
            assert stats["original_sources_fitness_increase"]==stats["original_sources_fitness_decrease"]==0
        if w in ("CROSS_ONEMAX","MUTATE_ONEMAX","CROSS_MUTATE_ONEMAX"):
            assert stats["original_sources_fitness_decrease"]>0
            assert stats["original_sources_fitness_increase"]>0
        if w in ("CROSS_ONEMAX","ELITE_CROSS_ONEMAX"):
            for z in sources(w):
                old=sum(int(b) for i in range(2) for b in z[f"observed_parent{i}_threebit_genome"])
                new=sum(int(b) for i in range(2) for b in z[f"observed_candidate_child{i}_threebit_genome"])
                assert old==new
    # Distinct parent/candidate populations with identical best possible.
    a=summary("CLONAL_ONEMAX");b=summary("ELITE_CLONAL_ONEMAX")
    assert a["exact_survivor_best_mean"]==b["exact_survivor_best_mean"]
    assert fitness((0,0,0),"TRAP")==4 and fitness((1,1,1),"TRAP")==3
    return True
def emit():
    frozen_claims()
    data=dict(research_id="R263",original_catalogue_id="11-023",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_TWO_INDIVIDUAL_THREEBIT_ONE_GENERATION_GENETIC_ALGORITHMS",
       frozen_worlds=9,complete_original_tenbit_source_atoms=9216,
       independent_full_conditional_survivor_joint_laws_for_all_64_parent_pairs=True,
       elite_never_loses_parent_best_one_generation_sourcewise=True,
       crossed_allele_count_conserved_if_no_mutation=True,
       trap_fitness_000_equals_4_greater_than_111_equals_3=True,
       no_long_run_global_convergence_or_human_biological_adaptation_proven=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[summary(w) for w in WORLDS])
    out=HERE/"R263_ALL_9216_ORIGINAL_TWO_PARENT_GENETIC_SOURCE_ATOMS.csv"
    keys=list(sources(WORLDS[0])[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for z in sources(w):wr.writerow({k:str(z[k]) for k in keys})
    jp=HERE/"R263_EXACT_RESULTS.json"
    jp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R263",original_catalogue_id="11-023",frozen_worlds=9,
      all_original_tenbit_genetic_atoms=9216,
      every_conditional_parent_two_survivor_PMF_verified_by_independent_integer_mask_route=True,
      elitist_parent_best_monotonicity_verified=True,
      nonelite_sometimes_loses_best_one_generation=True,
      mutation_free_crossover_conserves_population_allele_counts=True,
      source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
      new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R263_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_full(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),9216)
    def test_locked(self):self.assertTrue(frozen_claims())
    def test_clonal(self):self.assertEqual(summary("CLONAL_ONEMAX")["exact_best_fitness_gain_mean"],"0")
    def test_elite(self):self.assertEqual(summary("ELITE_CROSS_MUTATE_ONEMAX")["original_sources_fitness_decrease"],0)
    def test_non_elite(self):self.assertGreater(summary("CROSS_ONEMAX")["original_sources_fitness_decrease"],0)
    def test_trap(self):self.assertEqual(fitness((0,0,0),"TRAP"),4)
    def test_independent(self):self.assertTrue(independent_distribution_verified("ELITE_CROSS_MUTATE_TRAP"))
    def test_original_unique(self):self.assertEqual(len(ALL_10BIT),1024)
    def test_invalid(self):
        with self.assertRaises(ValueError):sources("OTHER_WORLD")
def _test(w,k):
    def test(self):
        rows=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_complete_tenbit_source_mass"] for r in rows),ZERO),ONE)
        elif k=="unique":self.assertEqual(len({tuple(r[f"oracle_original_bit_{i}"] for i in range(10)) for r in rows}),1024)
        elif k=="positive":self.assertTrue(all(r["original_complete_tenbit_source_mass"]==F(1,1024) for r in rows))
        elif k=="conditional":self.assertTrue(independent_distribution_verified(w))
        elif k=="cost":
            for r in rows:
                self.assertEqual(r["observed_next_minus_original_best_fitness"],r["observed_next_survivor_best_fitness"]-r["observed_original_parent_best_fitness"])
        elif k=="survivor":
            for r in rows:
                self.assertTrue(all(len(r[f"observed_{p}_threebit_genome"])==3 for p in ("parent0","parent1","candidate_child0","candidate_child1","survivor0","survivor1")))
        elif k=="summary":self.assertEqual(summary(w)["all_original_tenbit_source_atoms"],1024)
        elif k=="elite":
            if CONFIG[w][2]:self.assertEqual(summary(w)["original_sources_fitness_decrease"],0)
        else:raise AssertionError("unknown test case")
    return test
for w in WORLDS:
    for k in ("mass","unique","positive","conditional","cost","survivor","summary","elite"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_test(w,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();x=p.add_mutually_exclusive_group(required=True)
    x.add_argument("--test",action="store_true");x.add_argument("--emit",action="store_true")
    opts=p.parse_args()
    if opts.test:unittest.main(argv=["r263"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
