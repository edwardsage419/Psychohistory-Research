#!/usr/bin/env python3
"""R238 exact artificial diachronic embeddings and hidden-sense measurement.

Nine frozen 2-time, 4-word, 2-sense worlds. All rational coordinate, weighted
centroid, 4x4 Gram, inverse two-anchor linear alignment and hidden sense
covariance calculations are exact Fraction. Never uses a historical corpus.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)
FREEZE="7376538692ef9c468e21a2366e69db7d238f2a76"
WORDS=("A","B","C","D")
TIMES=(0,1)
SENSES=(0,1)
BASE_COORD={
    "A":(ONE,ZERO),"B":(ZERO,ONE),"C":(ONE,ONE),"D":(ONE,-ONE)
}
Q=((F(3,5),F(-4,5)),(F(4,5),F(3,5)))
DEFAULT_COUNTS=(4,4,2,2)
SHIFTED_COUNTS=(8,2,1,1)
WORLDS=(
    "STABLE_BASE",
    "GLOBAL_ROTATION",
    "TARGET_SEMANTIC_DRIFT",
    "ROTATED_TARGET_DRIFT",
    "GLOBAL_SCALE_2",
    "FREQUENCY_COMPOSITION_ONLY",
    "FREQUENCY_PLUS_TARGET_DRIFT",
    "ANCHOR_DRIFT_FALSE_ALIGNMENT",
    "SENSE_RECONFIGURATION_ALIAS"
)
DRIFT_WORLDS=("TARGET_SEMANTIC_DRIFT","ROTATED_TARGET_DRIFT","FREQUENCY_PLUS_TARGET_DRIFT")
FREQUENCY_WORLDS=("FREQUENCY_COMPOSITION_ONLY","FREQUENCY_PLUS_TARGET_DRIFT")
ROTATION_WORLDS=("GLOBAL_ROTATION","ROTATED_TARGET_DRIFT")

def config(world):
    if world not in WORLDS:raise ValueError("word embedding world not in frozen protocol")
    return world

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def subtract(a,b):return (a[0]-b[0],a[1]-b[1])
def multiply(s,a):return (F(s)*a[0],F(s)*a[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def matrix_apply(M,v):return (dot(M[0],v),dot(M[1],v))
def norm_sq(a):return dot(a,a)
def determinant(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def invert_2x2(M):
    det=determinant(M)
    if det==0:raise ValueError("invalid anchor alignment: collinear or zero anchors")
    return ((M[1][1]/det,-M[0][1]/det),(-M[1][0]/det,M[0][0]/det))

def word_count(world,t,word):
    config(world)
    if t not in TIMES or word not in WORDS:raise ValueError("outside time or word vocabulary")
    counts=SHIFTED_COUNTS if t==1 and world in FREQUENCY_WORLDS else DEFAULT_COUNTS
    return counts[WORDS.index(word)]

def true_senses(world,t,word):
    """Frozen oracle meaning coordinates, before arbitrary embedding frame."""
    config(world)
    if t not in TIMES or word not in WORDS:raise ValueError("outside time or word vocabulary")
    if word=="D":
        if t==1 and world=="SENSE_RECONFIGURATION_ALIAS":
            return ((ONE,F(-2)),(ONE,ZERO))
        baseline=((ZERO,-ONE),(F(2),-ONE))
        if t==1 and world in DRIFT_WORLDS:
            return tuple(add(v,(ONE,ZERO)) for v in baseline)
        return baseline
    base=BASE_COORD[word]
    if t==1 and world=="ANCHOR_DRIFT_FALSE_ALIGNMENT" and word in ("A","B"):
        base=matrix_apply(Q,base)
    return (base,base)

def coordinate_transform(world,t,vector):
    config(world)
    if t==1 and world in ROTATION_WORLDS:
        return matrix_apply(Q,vector)
    if t==1 and world=="GLOBAL_SCALE_2":
        return multiply(F(2),vector)
    return vector

def analytic_true_sense_centroid(world,t,word):
    a,b=true_senses(world,t,word)
    return multiply(F(1,2),add(a,b))

def independent_observed_embedding(world,t,word):
    """Analytic independent path: frozen semantic mixture and frame, no sources."""
    return coordinate_transform(world,t,analytic_true_sense_centroid(world,t,word))

def source_atom(world,t,word,sense):
    if sense not in SENSES:raise ValueError("invalid frozen sense index")
    semantic=true_senses(world,t,word)[sense]
    observed=independent_observed_embedding(world,t,word)
    count=word_count(world,t,word)
    return dict(
        world=world,time=t,word=word,oracle_sense=sense,
        oracle_true_semantic_sense_x=semantic[0],
        oracle_true_semantic_sense_y=semantic[1],
        observed_embedding_x=observed[0],observed_embedding_y=observed[1],
        observed_word_frequency=F(count,12),
        original_token_count_in_period=count,
        original_structural_source_probability=F(count,48)
    )

@lru_cache(maxsize=None)
def source_rows(world):
    config(world)
    result=tuple(source_atom(world,t,w,s) for t in TIMES for w in WORDS for s in SENSES)
    if len(result)!=16 or sum((r["original_structural_source_probability"] for r in result),ZERO)!=ONE:
        raise AssertionError("original sense universe incomplete")
    if any(r["original_structural_source_probability"]<=0 for r in result):
        raise AssertionError("unexpected zero source")
    return result

def observed_centroids_from_sources(world):
    """Normalize full latent source probabilities conditional on each (time,word)."""
    result={}
    for t in TIMES:
        for word in WORDS:
            rows=[r for r in source_rows(world) if r["time"]==t and r["word"]==word]
            normal=sum((r["original_structural_source_probability"] for r in rows),ZERO)
            if len(rows)!=2 or normal<=0:raise AssertionError("wrong sense source support")
            v=(
                sum((r["original_structural_source_probability"]*r["observed_embedding_x"] for r in rows),ZERO)/normal,
                sum((r["original_structural_source_probability"]*r["observed_embedding_y"] for r in rows),ZERO)/normal
            )
            if sum((r["original_structural_source_probability"] for r in rows),ZERO)!=F(word_count(world,t,word),24):
                raise AssertionError("source mass per word/time differs from explicit frequency")
            result[t,word]=v
    return result

def independent_centroids(world):
    return {(t,w):independent_observed_embedding(world,t,w) for t in TIMES for w in WORDS}

def visible_joint(world):
    """Actual observable period,word,embedding,frequency probability distribution."""
    joint=defaultdict(F)
    for r in source_rows(world):
        key=(r["time"],r["word"],r["observed_embedding_x"],
             r["observed_embedding_y"],r["observed_word_frequency"])
        joint[key]+=r["original_structural_source_probability"]
    return dict(sorted(joint.items()))

def gram(centroids,t):
    return tuple(tuple(dot(centroids[t,a],centroids[t,b]) for b in WORDS) for a in WORDS)

def alignment_inverse(centroids):
    """Two frozen anchor columns A,B. Not a fitted generalized Procrustes."""
    a=centroids[1,"A"]
    b=centroids[1,"B"]
    H=((a[0],b[0]),(a[1],b[1]))
    inv=invert_2x2(H)
    if matrix_apply(inv,a)!=(ONE,ZERO) or matrix_apply(inv,b)!=(ZERO,ONE):
        raise AssertionError("two-anchor exact alignment failed")
    return inv

def population_weighted_centroid(world,centroids,t):
    return (
        sum((F(word_count(world,t,w),12)*centroids[t,w][0] for w in WORDS),ZERO),
        sum((F(word_count(world,t,w),12)*centroids[t,w][1] for w in WORDS),ZERO)
    )

def independent_weighted_centroid(world,t):
    return population_weighted_centroid(world,independent_centroids(world),t)

def oracle_D_sense_covariance(world,t):
    values=true_senses(world,t,"D")
    mean=analytic_true_sense_centroid(world,t,"D")
    dif=tuple(subtract(v,mean) for v in values)
    return tuple(tuple(sum((d[i]*d[j] for d in dif),ZERO)/2 for j in range(2)) for i in range(2))

def source_D_sense_covariance(world,t):
    data=[r for r in source_rows(world) if r["time"]==t and r["word"]=="D"]
    mass=sum((r["original_structural_source_probability"] for r in data),ZERO)
    mean=(
        sum((r["original_structural_source_probability"]*r["oracle_true_semantic_sense_x"] for r in data),ZERO)/mass,
        sum((r["original_structural_source_probability"]*r["oracle_true_semantic_sense_y"] for r in data),ZERO)/mass
    )
    pairs=[(r["oracle_true_semantic_sense_x"],r["oracle_true_semantic_sense_y"]) for r in data]
    return tuple(tuple(sum((F(1,2)*(v[i]-mean[i])*(v[j]-mean[j]) for v in pairs),ZERO)
                       for j in range(2)) for i in range(2))

def oracle_D_centroid_change_sq(world):
    return norm_sq(subtract(analytic_true_sense_centroid(world,1,"D"),
                            analytic_true_sense_centroid(world,0,"D")))

def alias_certificates():
    v=visible_joint("STABLE_BASE")
    if v!=visible_joint("SENSE_RECONFIGURATION_ALIAS"):
        raise AssertionError("hidden sense redistribution changed fully observable embeddings")
    assert oracle_D_sense_covariance("STABLE_BASE",1)==((ONE,ZERO),(ZERO,ZERO))
    assert oracle_D_sense_covariance("SENSE_RECONFIGURATION_ALIAS",1)==((ZERO,ZERO),(ZERO,ONE))
    for a,b in (("GLOBAL_ROTATION","STABLE_BASE"),
                ("TARGET_SEMANTIC_DRIFT","ROTATED_TARGET_DRIFT")):
        ca=observed_centroids_from_sources(a)
        cb=observed_centroids_from_sources(b)
        if gram(ca,1)!=gram(cb,1):
            raise AssertionError("global rotation changed within-period observable Gram")
    return True

def world_result(world):
    centers=observed_centroids_from_sources(world)
    if centers!=independent_centroids(world):
        raise AssertionError("latent source centroid differs from independent analytic generation")
    for t in TIMES:
        freq=sum((F(word_count(world,t,w),12) for w in WORDS),ZERO)
        if freq!=ONE:raise AssertionError("token frequency no longer normalized")
        if population_weighted_centroid(world,centers,t)!=independent_weighted_centroid(world,t):
            raise AssertionError("weighted centroid disagrees with independent model")
        if source_D_sense_covariance(world,t)!=oracle_D_sense_covariance(world,t):
            raise AssertionError("source hidden sense covariance disagrees with semantic template")
    before=centers[0,"D"]
    after=centers[1,"D"]
    naive=norm_sq(subtract(after,before))
    align=alignment_inverse(centers)
    aligned=norm_sq(subtract(matrix_apply(align,after),before))
    oracle=oracle_D_centroid_change_sq(world)
    centroids=tuple(population_weighted_centroid(world,centers,t) for t in TIMES)
    corpus_change=norm_sq(subtract(centroids[1],centroids[0]))
    if world=="GLOBAL_ROTATION":
        assert naive==F(8,5) and aligned==ZERO and oracle==ZERO
        assert gram(centers,0)==gram(centers,1)
    if world=="GLOBAL_SCALE_2":
        assert naive==F(2) and aligned==ZERO and oracle==ZERO
        assert gram(centers,1)==tuple(tuple(4*x for x in row) for row in gram(centers,0))
    if world=="ANCHOR_DRIFT_FALSE_ALIGNMENT":
        assert naive==ZERO and aligned==F(8,5) and oracle==ZERO
    if world=="TARGET_SEMANTIC_DRIFT":
        assert naive==aligned==oracle==ONE
    if world=="ROTATED_TARGET_DRIFT":
        assert naive==F(5) and aligned==oracle==ONE
    if world=="FREQUENCY_COMPOSITION_ONLY":
        assert naive==aligned==oracle==ZERO and corpus_change>0
    if world=="FREQUENCY_PLUS_TARGET_DRIFT":
        assert aligned==oracle==ONE and corpus_change>0
    if world=="SENSE_RECONFIGURATION_ALIAS":
        assert naive==aligned==oracle==ZERO
        assert oracle_D_sense_covariance(world,0)!=oracle_D_sense_covariance(world,1)
    return dict(
        world=world,source_latent_sense_atoms=16,
        exact_observed_time_word_frequency_and_embedding_joint={
            "|".join(map(str,k)):str(v) for k,v in visible_joint(world).items()
        },
        observed_embeddings_by_time={
            str(t):{w:[str(v) for v in centers[t,w]] for w in WORDS} for t in TIMES
        },
        observed_word_frequencies_by_time={
            str(t):{w:str(F(word_count(world,t,w),12)) for w in WORDS} for t in TIMES
        },
        observed_gram_matrices={
            str(t):[[str(v) for v in row] for row in gram(centers,t)] for t in TIMES
        },
        exact_inverse_two_anchor_alignment=[[str(x) for x in row] for row in align],
        observed_target_D_naive_displacement_squared=str(naive),
        observed_target_D_anchor_aligned_displacement_squared=str(aligned),
        oracle_true_target_D_semantic_centroid_change_squared=str(oracle),
        observed_corpus_weighted_centroids_by_time=[[str(v) for v in c] for c in centroids],
        observed_corpus_weighted_centroid_displacement_squared=str(corpus_change),
        oracle_target_D_hidden_sense_covariance_by_time={
            str(t):[[str(v) for v in row] for row in oracle_D_sense_covariance(world,t)]
            for t in TIMES
        }
    )

def generate():
    alias_certificates()
    summary=dict(
        research_id="R238",original_catalogue_id="10-012",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_DIAchronic_EMBEDDING_ROTATION_ANCHOR_AND_SENSE",
        frozen_worlds=9,full_original_latent_sense_source_atoms=144,
        two_time_periods=2,artificial_word_types=4,latent_sense_modes=2,
        original_full_observation_alias=[
            "STABLE_BASE","SENSE_RECONFIGURATION_ALIAS"
        ],
        orthogonal_frame_gram_alias_pairs=[
            ["GLOBAL_ROTATION","STABLE_BASE"],
            ["TARGET_SEMANTIC_DRIFT","ROTATED_TARGET_DRIFT"]
        ],
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS]
    )
    src=HERE/"R238_ALL_144_ORIGINAL_HIDDEN_SENSE_AND_OBSERVED_EMBEDDING_SOURCES.csv"
    fields=list(source_atom("STABLE_BASE",0,"A",0))
    with src.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        wr.writeheader()
        for world in WORLDS:
            for r in source_rows(world):
                wr.writerow({k:str(r[k]) for k in fields})
    res=HERE/"R238_EXACT_RESULTS.json"
    res.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(
        research_id="R238",original_catalogue_id="10-012",
        frozen_worlds=9,original_full_hidden_sense_atoms=144,
        independent_observed_centroid_parity=True,
        full_observed_sense_reconfiguration_alias=True,
        source_vs_independent_hidden_sense_covariance=True,
        anchor_inverse_and_gram_rotation_invariance=True,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0
    )
    (HERE/"R238_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_world_count(self):self.assertEqual(len(WORLDS),9)
    def test_source_count(self):self.assertEqual(sum(len(source_rows(w)) for w in WORLDS),144)
    def test_orthogonal_Q(self):
        self.assertEqual(determinant(Q),ONE)
        self.assertEqual(dot(Q[0],Q[0]),ONE)
        self.assertEqual(dot(Q[1],Q[1]),ONE)
        self.assertEqual(dot(Q[0],Q[1]),ZERO)
    def test_gram_aliases(self):self.assertTrue(alias_certificates())
    def test_rotation_target(self):
        a=world_result("GLOBAL_ROTATION")
        self.assertEqual(a["observed_target_D_naive_displacement_squared"],"8/5")
        self.assertEqual(a["observed_target_D_anchor_aligned_displacement_squared"],"0")
    def test_anchor_false_alignment(self):
        a=world_result("ANCHOR_DRIFT_FALSE_ALIGNMENT")
        self.assertEqual(a["observed_target_D_naive_displacement_squared"],"0")
        self.assertEqual(a["observed_target_D_anchor_aligned_displacement_squared"],"8/5")
    def test_scale(self):
        a=world_result("GLOBAL_SCALE_2")
        self.assertEqual(a["observed_target_D_naive_displacement_squared"],"2")
        self.assertEqual(a["observed_target_D_anchor_aligned_displacement_squared"],"0")
    def test_rotated_true_target(self):
        a=world_result("ROTATED_TARGET_DRIFT")
        self.assertEqual(a["observed_target_D_naive_displacement_squared"],"5")
        self.assertEqual(a["observed_target_D_anchor_aligned_displacement_squared"],"1")
    def test_frequency_only(self):
        a=world_result("FREQUENCY_COMPOSITION_ONLY")
        self.assertEqual(a["observed_target_D_anchor_aligned_displacement_squared"],"0")
        self.assertGreater(F(a["observed_corpus_weighted_centroid_displacement_squared"]),ZERO)
    def test_hidden_sense_alias(self):
        a=world_result("STABLE_BASE");b=world_result("SENSE_RECONFIGURATION_ALIAS")
        self.assertEqual(a["exact_observed_time_word_frequency_and_embedding_joint"],
                         b["exact_observed_time_word_frequency_and_embedding_joint"])
        self.assertNotEqual(a["oracle_target_D_hidden_sense_covariance_by_time"]["1"],
                            b["oracle_target_D_hidden_sense_covariance_by_time"]["1"])
    def test_invert_singular(self):
        with self.assertRaises(ValueError):invert_2x2(((ONE,ONE),(ONE,ONE)))
    def test_bad_world(self):
        with self.assertRaises(ValueError):source_rows("UNKNOWN")

def _case(world,kind):
    def test(self):
        rows=source_rows(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_structural_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({(r["time"],r["word"],r["oracle_sense"]) for r in rows}),16)
        elif kind=="positive":
            self.assertTrue(all(r["original_structural_source_probability"]>0 for r in rows))
        elif kind=="centroid":
            self.assertEqual(observed_centroids_from_sources(world),independent_centroids(world))
        elif kind=="oracle_sense":
            for t in TIMES:
                self.assertEqual(source_D_sense_covariance(world,t),oracle_D_sense_covariance(world,t))
        elif kind=="full_visible":
            self.assertEqual(sum(visible_joint(world).values(),ZERO),ONE)
        elif kind=="anchors":
            c=observed_centroids_from_sources(world)
            inv=alignment_inverse(c)
            self.assertEqual(matrix_apply(inv,c[1,"A"]),(ONE,ZERO))
            self.assertEqual(matrix_apply(inv,c[1,"B"]),(ZERO,ONE))
        elif kind=="summary":
            self.assertEqual(world_result(world)["source_latent_sense_atoms"],16)
        else:raise AssertionError("unknown test")
    return test
for _w in WORLDS:
    for _kind in ("mass","unique","positive","centroid","oracle_sense","full_visible","anchors","summary"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r238"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
