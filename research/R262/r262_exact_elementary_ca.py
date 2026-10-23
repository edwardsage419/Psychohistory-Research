#!/usr/bin/env python3
"""R262 nine finite elementary cellular automata, seven-cell periodic ring.

Complete 7-bit original initial states x 5 source time labels x nine frozen
elementary rules = 5760 complete finite artificial source rows. The original
Wolfram rule shift implementation is verified independently using a frozen
eight-neighborhood truth table per rule; exact 128->64/128 image information
loss, density and spatial shift alias do not imply infinite-grid complexity.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="8dc5cbb95ed011e5fd190d42e63336df938ccd40"
ZERO=F(0);ONE=F(1)
N=7
INITIALS=tuple(itertools.product((0,1),repeat=N))
TIMES=(0,1,2,3,4)
RULES={
 "ABSORB_ZERO":(0,"00000000"),
 "ABSORB_ONE":(255,"11111111"),
 "IDENTITY":(204,"11001100"),
 "SHIFT_RIGHT":(170,"10101010"),
 "SHIFT_LEFT":(240,"11110000"),
 "XOR_NEIGHBORS":(90,"01011010"),
 "XOR_THREE":(150,"10010110"),
 "RULE30":(30,"00011110"),
 "RULE110":(110,"01101110")
}
WORLDS=tuple(RULES)
EXPECTED_IMAGE_FIXED={
"ABSORB_ZERO":(1,1),
"ABSORB_ONE":(1,1),
"IDENTITY":(128,128),
"SHIFT_RIGHT":(128,2),
"SHIFT_LEFT":(128,2),
"XOR_NEIGHBORS":(64,1),
"XOR_THREE":(128,2),
"RULE30":(106,1),
"RULE110":(79,1)
}
EXPECTED_DENSITY={
"ABSORB_ZERO":("1/2","0","0","0","0"),
"ABSORB_ONE":("1/2","1","1","1","1"),
"IDENTITY":("1/2",)*5,
"SHIFT_RIGHT":("1/2",)*5,
"SHIFT_LEFT":("1/2",)*5,
"XOR_NEIGHBORS":("1/2",)*5,
"XOR_THREE":("1/2",)*5,
"RULE30":("1/2","1/2","1/2","1/2","61/128"),
"RULE110":("1/2","5/8","17/32","33/64","17/32")
}
def check(w):
    if w not in RULES:raise ValueError("not a frozen elementary CA")
def direct_wolfram_step(state,rule):
    if len(state)!=N or not 0<=rule<=255:raise ValueError("invalid finite CA")
    ans=[]
    for i in range(N):
        index=4*state[(i-1)%N]+2*state[i]+state[(i+1)%N]
        ans.append((rule>>index)&1)
    return tuple(ans)
def independent_truth_table_step(state,table):
    """No integer bit shifting, independent 8-neighborhood string mapping."""
    if len(state)!=N or len(table)!=8 or any(z not in "01" for z in table):
        raise ValueError("invalid frozen truth table")
    new=[]
    for i in range(N):
        neighborhood=(state[(i-1)%N],state[i],state[(i+1)%N])
        pattern="".join(str(v) for v in neighborhood)
        idx=("111","110","101","100","011","010","001","000").index(pattern)
        new.append(int(table[idx]))
    return tuple(new)
@lru_cache(None)
def trajectories(w):
    check(w);rule,_=RULES[w]
    paths={}
    for orig in INITIALS:
        path=[orig]
        for t in range(1,len(TIMES)):
            path.append(direct_wolfram_step(path[-1],rule))
        paths[orig]=tuple(path)
    return paths
def independent_state(w,orig,n):
    check(w)
    if n not in TIMES or orig not in INITIALS:raise ValueError("bad original state/time")
    table=RULES[w][1]
    v=orig
    for _ in range(n):v=independent_truth_table_step(v,table)
    return v
def source_atom(w,orig,n):
    if orig not in INITIALS or n not in TIMES:raise ValueError("not an original seven bit/time")
    state=trajectories(w)[orig][n]
    if state!=independent_state(w,orig,n):
        raise AssertionError("Wolfram bit rule disagrees independent full neighborhood truth table")
    row={"world":w,"frozen_Wolfram_rule_decimal":RULES[w][0]}
    for i in range(N):
        row[f"original_initial_cell_bit_{i}"]=orig[i]
        row[f"observed_cell_state_{i}_at_time"]=state[i]
    row["observed_time_index_n"]=n
    row["observed_number_cells_in_state_1"]=sum(state)
    row["observed_global_state_parity"]=sum(state)%2
    row["original_complete_initial_and_time_design_mass"]=F(1,640)
    return row
@lru_cache(None)
def sources(w):
    check(w)
    rows=tuple(source_atom(w,o,t) for o in INITIALS for t in TIMES)
    assert len(rows)==640
    assert sum((r["original_complete_initial_and_time_design_mass"] for r in rows),ZERO)==ONE
    return rows
def image_fixed(w):
    paths=trajectories(w)
    image={p[1] for p in paths.values()}
    fixed=sum(p[1]==p[0] for p in paths.values())
    return len(image),fixed
def densities(w):
    data=trajectories(w)
    return tuple(F(sum(sum(p[t]) for p in data.values()),len(INITIALS)*N) for t in TIMES)
def independent_image_densities(w):
    """Independent table step, no direct stored source paths."""
    one=[independent_truth_table_step(o,RULES[w][1]) for o in INITIALS]
    cardinality=len(set(one))
    fixed=sum(a==b for a,b in zip(INITIALS,one))
    averages=[]
    for n in TIMES:
        avg=sum(sum(independent_state(w,o,n)) for o in INITIALS)
        averages.append(F(avg,len(INITIALS)*N))
    return cardinality,fixed,tuple(averages)
def frozen_claims():
    for w in WORLDS:
        a,b=image_fixed(w),densities(w)
        independent=independent_image_densities(w)
        if a!=EXPECTED_IMAGE_FIXED[w] or tuple(map(str,b))!=EXPECTED_DENSITY[w]:
            raise AssertionError(f"{w} rule image cardinality/density disagrees frozen finite source {a} {b}")
        if independent!=(a[0],a[1],b):
            raise AssertionError(f"{w} full independent truth table results mismatch")
    # Rule90's map over the 7-ring is 2-to-1, each image has even parity.
    map90=[direct_wolfram_step(orig,90) for orig in INITIALS]
    preimage_counts=Counter(map90)
    assert len(preimage_counts)==64 and set(preimage_counts.values())=={2}
    assert all(sum(out)%2==0 for out in map90)
    map150=[direct_wolfram_step(orig,150) for orig in INITIALS]
    assert len(set(map150))==128
    assert all(sum(o)%2==sum(n)%2 for o,n in zip(INITIALS,map150))
    # Every initial state has matching aggregate population under opposing shifts,
    # but only the two homogeneous states match the full first-step observation.
    differences=0
    for orig in INITIALS:
        p=trajectories("SHIFT_RIGHT")[orig]
        q=trajectories("SHIFT_LEFT")[orig]
        assert all(sum(a)==sum(b)==sum(orig) for a,b in zip(p,q))
        differences+=int(p[1]!=q[1])
    assert differences==126
    return True
def world_result(w):
    n,f=image_fixed(w)
    independent=independent_image_densities(w)
    assert (n,f)==independent[:2] and densities(w)==independent[2]
    return dict(world=w,frozen_Wolfram_rule=RULES[w][0],
        frozen_truth_table_111_to_000=RULES[w][1],
        original_initial_time_source_atoms=640,
        one_step_distinct_full_sevenbit_images=n,
        one_step_original_initial_fixed_point_count=f,
        all_five_time_uniform_original_source_expected_one_density=[str(x) for x in densities(w)],
        all_128_initials_all_5_times_independent_truth_table_parity=True,
        xor90_one_step_two_to_one_even_parity_image=(w=="XOR_NEIGHBORS"),
        xor150_one_step_permutation_parity_preservation=(w=="XOR_THREE"))
def emit():
    frozen_claims()
    result=dict(research_id="R262",original_catalogue_id="11-022",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_ELEMENTARY_CA_SEVEN_SITE_PERIODIC_RING",
       frozen_worlds=9,all_original_sevenbit_initial_time_source_atoms=5760,
       each_world_complete_initial_sevenbit_configs=128,
       time_samples_per_same_initial_configuration=5,
       no_infinite_CA_chaos_universality_or_historical_dynamics_claim=True,
       rule90_exact_one_step_image_size=64,
       rule90_each_distinct_image_has_two_original_preimages=True,
       rule150_exact_one_step_image_size=128,
       opposing_shifts_identical_population_all_source_times_but_different_first_microstate_count=126,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R262_ALL_5760_ORIGINAL_SEVEN_RING_CA_SOURCE_ATOMS.csv"
    keys=list(sources(WORLDS[0])[0])
    with out.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for z in sources(w):wr.writerow({k:str(z[k]) for k in keys})
    jp=HERE/"R262_EXACT_RESULTS.json"
    jp.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R262",original_catalogue_id="11-022",
       frozen_worlds=9,all_original_sevenbit_time_atoms=5760,
       full_wolfram_rule_bits_vs_independent_eight_neighborhood_truth_table=True,
       finite_rule_image_cardinality_and_fixed_point_counts_verified=True,
       rule90_two_to_one_image_exact_information_loss_one_bit=True,
       rule150_full_128_permutation_parity_invariance=True,
       left_right_shift_identical_aggregate_and_micro_different_for_126=True,
       source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R262_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_full_source(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),5760)
    def test_frozen_results(self):self.assertTrue(frozen_claims())
    def test_rule90_loss(self):self.assertEqual(image_fixed("XOR_NEIGHBORS"),(64,1))
    def test_rule150_reversible(self):self.assertEqual(image_fixed("XOR_THREE"),(128,2))
    def test_rule30_images(self):self.assertEqual(image_fixed("RULE30"),(106,1))
    def test_rule110_density(self):self.assertEqual(str(densities("RULE110")[1]),"5/8")
    def test_identity_fixed(self):self.assertEqual(image_fixed("IDENTITY"),(128,128))
    def test_xor90_parity(self):
        self.assertTrue(all(sum(direct_wolfram_step(o,90))%2==0 for o in INITIALS))
    def test_invalid_world(self):
        with self.assertRaises(ValueError):sources("INVALID")
def _case(w,k):
    def t(self):
        src=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_complete_initial_and_time_design_mass"] for r in src),ZERO),ONE)
        elif k=="unique":
            keys=[f"original_initial_cell_bit_{i}" for i in range(N)]+["observed_time_index_n"]
            self.assertEqual(len({tuple(r[z] for z in keys) for r in src}),640)
        elif k=="positive":self.assertTrue(all(r["original_complete_initial_and_time_design_mass"]==F(1,640) for r in src))
        elif k=="states":
            for r in src:
                self.assertEqual(sum(r[f"observed_cell_state_{i}_at_time"] for i in range(N)),r["observed_number_cells_in_state_1"])
        elif k=="parity":
            for r in src:self.assertEqual(r["observed_global_state_parity"],r["observed_number_cells_in_state_1"]%2)
        elif k=="independent":
            for init in INITIALS:
                for n in TIMES:self.assertEqual(trajectories(w)[init][n],independent_state(w,init,n))
        elif k=="image":self.assertEqual(image_fixed(w),EXPECTED_IMAGE_FIXED[w])
        elif k=="report":self.assertEqual(world_result(w)["original_initial_time_source_atoms"],640)
        else:raise AssertionError("unknown frozen test")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","states","parity","independent","image","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r262"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
