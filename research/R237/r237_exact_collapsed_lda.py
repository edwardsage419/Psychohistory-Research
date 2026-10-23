#!/usr/bin/env python3
"""R237 exact, finite, fixed-length collapsed Latent Dirichlet Allocation.

Nine prescore-frozen two-topic three-token artificial worlds, full 2^3*3^3
latent-topic/observed-word structural atoms per world. All probabilities use
fractions; observed word patterns never read latent z or posterior topics.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)
FREEZE="9551877b185684dadf163de8c620acce4a80e939"
TOPIC_PATTERN=tuple(itertools.product((0,1),repeat=3))
WORD_PATTERN=tuple(itertools.product((0,1,2),repeat=3))
BASE_BETA=((F(1,2),F(1,3),F(1,6)),(F(1,6),F(1,3),F(1,2)))
DUP_BETA=(BASE_BETA[0],BASE_BETA[0])
CONTRAST_BETA=((F(2,3),F(1,6),F(1,6)),(F(1,6),F(1,6),F(2,3)))
UNIFORM_BETA=((F(1,3),)*3,(F(1,3),)*3)
# Frozen alpha and conditional word distributions for each artificial topic.
WORLDS={
    "BASE_TOPICS":((ONE,ONE),BASE_BETA),
    "LABEL_SWAP_ALIAS":((ONE,ONE),(BASE_BETA[1],BASE_BETA[0])),
    "DUPLICATE_TOPICS_A":((ONE,ONE),DUP_BETA),
    "DUPLICATE_TOPICS_B":((F(3),ONE),DUP_BETA),
    "CONTRASTED_TOPICS":((ONE,ONE),CONTRAST_BETA),
    "ALPHA_CONCENTRATED":((F(4),F(4)),BASE_BETA),
    "ALPHA_SPARSE":((F(1,4),F(1,4)),BASE_BETA),
    "UNIFORM_WORDS":((ONE,ONE),UNIFORM_BETA),
    "ASYMMETRIC_ALPHA":((F(3),ONE),BASE_BETA),
}
FROZEN_COVARIANCES={
    "BASE_TOPICS":F(1,108),
    "LABEL_SWAP_ALIAS":F(1,108),
    "DUPLICATE_TOPICS_A":ZERO,
    "DUPLICATE_TOPICS_B":ZERO,
    "CONTRASTED_TOPICS":F(1,48),
    "ALPHA_CONCENTRATED":F(1,324),
    "ALPHA_SPARSE":F(1,54),
    "UNIFORM_WORDS":ZERO,
    "ASYMMETRIC_ALPHA":F(1,240),
}
def params(world):
    if world not in WORLDS:
        raise ValueError("world not in prescore-frozen nine LDA populations")
    alpha,beta=WORLDS[world]
    if sum(alpha,ZERO)<=0 or any(v<=0 for v in alpha):
        raise AssertionError("invalid fixed positive Dirichlet alpha")
    if any(sum(b,ZERO)!=ONE or any(p<=0 for p in b) for b in beta):
        raise AssertionError("topic word categorical mass invalid")
    return alpha,beta

def rising(x,n):
    x=F(x)
    if not isinstance(n,int) or n<0: raise ValueError("rising degree must be nonnegative integer")
    v=ONE
    for j in range(n):v*=x+j
    return v

def collapsed_topic_probability(world,z):
    if z not in TOPIC_PATTERN:raise ValueError("invalid 3-topic latent assignment")
    alpha,_=params(world)
    n0=z.count(0)
    n1=z.count(1)
    return rising(alpha[0],n0)*rising(alpha[1],n1)/rising(sum(alpha,ZERO),3)

def polya_urn_topic_probability(world,z):
    """Independent sequential integration, not using the rising product."""
    if z not in TOPIC_PATTERN:raise ValueError("invalid latent topic sequence")
    alpha,_=params(world)
    counts=[0,0]
    q=ONE
    for i,k in enumerate(z):
        q*=(alpha[k]+counts[k])/(sum(alpha,ZERO)+i)
        counts[k]+=1
    return q

def emission_probability(world,z,w):
    if z not in TOPIC_PATTERN or w not in WORD_PATTERN:
        raise ValueError("unsupported topic or word pattern")
    _,beta=params(world)
    result=ONE
    for topic,word in zip(z,w):result*=beta[topic][word]
    return result

@lru_cache(maxsize=None)
def source_rows(world):
    params(world)
    rows=[]
    for z in TOPIC_PATTERN:
        pz=collapsed_topic_probability(world,z)
        if pz!=polya_urn_topic_probability(world,z):
            raise AssertionError("collapsed Gamma rising vs Polya urn conflict")
        for w in WORD_PATTERN:
            emit=emission_probability(world,z,w)
            rows.append(dict(
                world=world,
                oracle_z1=z[0],oracle_z2=z[1],oracle_z3=z[2],
                observed_word1=w[0],observed_word2=w[1],observed_word3=w[2],
                oracle_topic0_count=z.count(0),oracle_topic1_count=z.count(1),
                full_dirichlet_collapsed_topic_sequence_probability=pz,
                conditional_emission_probability=emit,
                full_original_latent_word_atom_probability=pz*emit
            ))
    if len(rows)!=216 or sum((r["full_original_latent_word_atom_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("full finite LDA generative universe incomplete")
    if any(r["full_original_latent_word_atom_probability"]<=0 for r in rows):
        raise AssertionError("unexpected structural zero in prescore positive models")
    return tuple(rows)

@lru_cache(maxsize=None)
def observed_document_joint(world):
    """Integrate z out of 216 original source rows. Observed w only."""
    joint=defaultdict(F)
    for r in source_rows(world):
        w=(r["observed_word1"],r["observed_word2"],r["observed_word3"])
        joint[w]+=r["full_original_latent_word_atom_probability"]
    if len(joint)!=27 or sum(joint.values(),ZERO)!=ONE:
        raise AssertionError("observed complete ordered document probability invalid")
    return dict(sorted(joint.items()))

def independently_integrated_word_probability(world,w):
    """Sum over 8 latent assignments from the independent Polya sequence law."""
    if w not in WORD_PATTERN:raise ValueError("invalid ordered word triple")
    return sum((polya_urn_topic_probability(world,z)*emission_probability(world,z,w)
                for z in TOPIC_PATTERN),ZERO)

def expected_word0_marginal(world):
    alpha,beta=params(world)
    return (alpha[0]*beta[0][0]+alpha[1]*beta[1][0])/sum(alpha,ZERO)

def independent_word0_pair_covariance(world):
    """Dirichlet variance theta_0 multiplied by squared topic word0 contrast."""
    alpha,beta=params(world)
    n=sum(alpha,ZERO)
    var_theta=alpha[0]*alpha[1]/(n*n*(n+1))
    return var_theta*(beta[0][0]-beta[1][0])**2

def observed_word0_pair_covariance(world):
    joint=observed_document_joint(world)
    p0=sum((q for w,q in joint.items() if w[0]==0),ZERO)
    p00=sum((q for w,q in joint.items() if w[0]==0 and w[1]==0),ZERO)
    return p00-p0*p0

def predictive_third_zero_given_two_zero(world):
    joint=observed_document_joint(world)
    numerator=joint[(0,0,0)]
    denominator=sum((joint[(0,0,w)] for w in (0,1,2)),ZERO)
    if denominator<=0:raise AssertionError("unexpected unsupported observed prefix")
    return numerator/denominator

def oracle_topic000_posterior_given_word000(world):
    joint=observed_document_joint(world)
    mass=joint[(0,0,0)]
    if mass<=0:raise AssertionError("null observed word document")
    original=next(r for r in source_rows(world)
                  if (r["oracle_z1"],r["oracle_z2"],r["oracle_z3"])==(0,0,0)
                  and (r["observed_word1"],r["observed_word2"],r["observed_word3"])==(0,0,0))
    return original["full_original_latent_word_atom_probability"]/mass

def all_observation_alias_certificates():
    a=observed_document_joint("BASE_TOPICS")
    b=observed_document_joint("LABEL_SWAP_ALIAS")
    if a!=b:raise AssertionError("topic label switching broke full observation equivalence")
    for z in TOPIC_PATTERN:
        zz=tuple(1-v for v in z)
        for w in WORD_PATTERN:
            base=collapsed_topic_probability("BASE_TOPICS",z)*emission_probability("BASE_TOPICS",z,w)
            swapped=collapsed_topic_probability("LABEL_SWAP_ALIAS",zz)*emission_probability("LABEL_SWAP_ALIAS",zz,w)
            if base!=swapped:raise AssertionError("label-swapped per-atom mass does not have a bijection")
    if observed_document_joint("DUPLICATE_TOPICS_A")!=observed_document_joint("DUPLICATE_TOPICS_B"):
        raise AssertionError("identical beta must make alpha unobservable")
    if collapsed_topic_probability("DUPLICATE_TOPICS_A",(0,0,0))==collapsed_topic_probability("DUPLICATE_TOPICS_B",(0,0,0)):
        raise AssertionError("different alphas did not change original latent assignment law")
    if oracle_topic000_posterior_given_word000("BASE_TOPICS")!=next(
       r["full_original_latent_word_atom_probability"] for r in source_rows("LABEL_SWAP_ALIAS")
       if (r["oracle_z1"],r["oracle_z2"],r["oracle_z3"])==(1,1,1)
       and (r["observed_word1"],r["observed_word2"],r["observed_word3"])==(0,0,0))/b[(0,0,0)]:
        raise AssertionError("posterior label complement mapping failed")
    return True

def world_result(world):
    joint=observed_document_joint(world)
    for w in WORD_PATTERN:
        if joint[w]!=independently_integrated_word_probability(world,w):
            raise AssertionError("source marginal and independent Polya-integrated marginal differ")
        for perm in set(itertools.permutations(w)):
            if joint[w]!=joint[perm]:
                raise AssertionError("fixed-length LDA word exchangeability violated")
    p0=sum((p for w,p in joint.items() if w[0]==0),ZERO)
    if p0!=expected_word0_marginal(world):
        raise AssertionError("analytic unigram and observed mass differ")
    cov=observed_word0_pair_covariance(world)
    if cov!=independent_word0_pair_covariance(world) or cov!=FROZEN_COVARIANCES[world]:
        raise AssertionError("independent Dirichlet covariance formula failed frozen world")
    pred=predictive_third_zero_given_two_zero(world)
    if world in ("DUPLICATE_TOPICS_A","DUPLICATE_TOPICS_B","UNIFORM_WORDS"):
        if pred!=p0:
            raise AssertionError("duplicated topics should yield iid word probabilities")
    if world in ("BASE_TOPICS","ALPHA_CONCENTRATED","ALPHA_SPARSE","CONTRASTED_TOPICS"):
        if pred<=p0:
            raise AssertionError("positive document topic heterogeneity should update word0 prediction after two word0")
    if world=="UNIFORM_WORDS":
        if any(q!=F(1,27) for q in joint.values()):
            raise AssertionError("uniform iid symbols expected exact 1/27 ordered document mass")
    return dict(
      world=world,
      alpha_dirichlet_parameters=[str(x) for x in params(world)[0]],
      frozen_topic_word_probabilities=[[str(v) for v in b] for b in params(world)[1]],
      full_original_topic_word_source_atoms=216,
      observed_full_document_support_size=len(joint),
      observable_unigram_word0_probability=str(p0),
      observable_word0_same_document_pair_covariance=str(cov),
      independently_calculated_dirichlet_pair_covariance=str(independent_word0_pair_covariance(world)),
      observable_predictive_third_word0_given_first_two_word0=str(pred),
      oracle_topic000_posterior_given_word000=str(oracle_topic000_posterior_given_word000(world)),
      exact_observable_three_position_word_joint={"".join(map(str,w)):str(p) for w,p in joint.items()}
    )

def generate():
    all_observation_alias_certificates()
    worlds=[world_result(w) for w in WORLDS]
    result=dict(
      research_id="R237",original_catalogue_id="10-011",
      prescore_freeze_commit=FREEZE,
      scientific_scope="FINITE_ARTIFICIAL_E1_COLLAPSED_LDA_LABEL_SWITCHING_AND_HYPERPRIOR_AMBIGUITY",
      fixed_document_length=3,vocabulary_size=3,topic_count=2,
      worlds=9,all_complete_original_source_atoms=1944,
      two_full_observation_alias_pairs=[
        ["BASE_TOPICS","LABEL_SWAP_ALIAS"],["DUPLICATE_TOPICS_A","DUPLICATE_TOPICS_B"]
      ],
      exact_full_joint_source_and_polya_marginal_parity=True,
      independent_dirichlet_second_moment_parity=True,
      new_real_human_E2=0,new_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",world_results=worlds
    )
    src=HERE/"R237_ALL_1944_ORIGINAL_LATENT_TOPIC_WORD_ATOMS.csv"
    fields=list(source_rows("BASE_TOPICS")[0])
    with src.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        wr.writeheader()
        for world in WORLDS:
            for row in source_rows(world):
                wr.writerow({k:str(row[k]) for k in fields})
    res=HERE/"R237_EXACT_RESULTS.json"
    res.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(
        research_id="R237",original_catalogue_id="10-011",
        nine_frozen_worlds=9,original_full_topic_word_atoms=1944,
        all_source_probability_masses_normalized=True,
        label_swap_source_bijection_certified=True,
        duplicate_topics_distinct_alpha_observation_alias_certified=True,
        observed_pair_covariance_independently_derived=True,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0
    )
    (HERE/"R237_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_all_1944_complete_atoms(self):
        self.assertEqual(sum(len(source_rows(w)) for w in WORLDS),1944)
    def test_topic_probability_by_polya(self):
        for z in TOPIC_PATTERN:
            self.assertEqual(collapsed_topic_probability("BASE_TOPICS",z),
                             polya_urn_topic_probability("BASE_TOPICS",z))
    def test_label_complement(self):self.assertTrue(all_observation_alias_certificates())
    def test_duplicate_topic_alpha_unobserved(self):
        self.assertEqual(observed_document_joint("DUPLICATE_TOPICS_A"),
                         observed_document_joint("DUPLICATE_TOPICS_B"))
        self.assertNotEqual(collapsed_topic_probability("DUPLICATE_TOPICS_A",(0,0,0)),
                            collapsed_topic_probability("DUPLICATE_TOPICS_B",(0,0,0)))
    def test_base_word0_unigram(self):self.assertEqual(expected_word0_marginal("BASE_TOPICS"),F(1,3))
    def test_sparse_vs_dense_covariance(self):
        self.assertGreater(observed_word0_pair_covariance("ALPHA_SPARSE"),
                           observed_word0_pair_covariance("BASE_TOPICS"))
        self.assertGreater(observed_word0_pair_covariance("BASE_TOPICS"),
                           observed_word0_pair_covariance("ALPHA_CONCENTRATED"))
    def test_all_zero_covariance_for_duplicate_topics(self):
        for w in ("DUPLICATE_TOPICS_A","DUPLICATE_TOPICS_B","UNIFORM_WORDS"):
            self.assertEqual(observed_word0_pair_covariance(w),ZERO)
    def test_uniform_word_sequences(self):
        self.assertTrue(all(v==F(1,27) for v in observed_document_joint("UNIFORM_WORDS").values()))
    def test_word0_prediction_updated(self):
        self.assertGreater(predictive_third_zero_given_two_zero("BASE_TOPICS"),
                           expected_word0_marginal("BASE_TOPICS"))
    def test_alpha_concentration_predictive(self):
        self.assertGreater(predictive_third_zero_given_two_zero("ALPHA_SPARSE"),
                           predictive_third_zero_given_two_zero("ALPHA_CONCENTRATED"))
    def test_asymmetric_prior_unigram(self):
        self.assertEqual(expected_word0_marginal("ASYMMETRIC_ALPHA"),F(5,12))
    def test_oracle_posterior_not_direct_word_observation(self):
        self.assertGreater(oracle_topic000_posterior_given_word000("BASE_TOPICS"),ZERO)
        self.assertLess(oracle_topic000_posterior_given_word000("BASE_TOPICS"),ONE)
    def test_negative_rising(self):
        with self.assertRaises(ValueError):rising(F(1),-1)
    def test_unknown_world(self):
        with self.assertRaises(ValueError):source_rows("UNFROZEN")

def _case(world,kind):
    def test(self):
        rows=source_rows(world)
        if kind=="mass":
            self.assertEqual(sum((r["full_original_latent_word_atom_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({(r["oracle_z1"],r["oracle_z2"],r["oracle_z3"],
                                   r["observed_word1"],r["observed_word2"],r["observed_word3"]) for r in rows}),216)
        elif kind=="strict_positive":
            self.assertTrue(all(r["full_original_latent_word_atom_probability"]>0 for r in rows))
        elif kind=="collapsed_topic":
            self.assertEqual(sum((collapsed_topic_probability(world,z) for z in TOPIC_PATTERN),ZERO),ONE)
        elif kind=="polya":
            for z in TOPIC_PATTERN:
                self.assertEqual(collapsed_topic_probability(world,z),polya_urn_topic_probability(world,z))
        elif kind=="observed":
            self.assertEqual(sum(observed_document_joint(world).values(),ZERO),ONE)
        elif kind=="covariance":
            self.assertEqual(observed_word0_pair_covariance(world),independent_word0_pair_covariance(world))
        elif kind=="prediction":
            self.assertGreater(predictive_third_zero_given_two_zero(world),ZERO)
        elif kind=="result":
            self.assertEqual(world_result(world)["full_original_topic_word_source_atoms"],216)
        else:raise AssertionError("unfrozen test")
    return test

for _w in WORLDS:
    for _kind in ("mass","unique","strict_positive","collapsed_topic","polya",
                  "observed","covariance","prediction","result"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["r237"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
