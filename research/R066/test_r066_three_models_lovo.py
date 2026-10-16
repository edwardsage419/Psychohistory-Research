"""Synthetic-only prespecified 16-village E2 source prediction invariants."""
import copy
import unittest
import numpy as np

from r066_three_models_lovo import (
    CLASSES, ALPHAS, EPSILONS, STEPS, response_index, evolve,
    make_grid, choose_training, score_lovo, precompute
)


class ThreeModelLOVOContracts(unittest.TestCase):
    def test_author_six_item_normalized_range(self):
        row={k+"1":"1" for k in ("noprob","fit","burden","values","land","threat")}
        self.assertEqual(response_index(row,"1"),0.0)
        row={k+"1":"5" for k in ("noprob","fit","burden","values","land","threat")}
        self.assertEqual(response_index(row,"1"),1.0)

    def test_missing_one_item_no_usable_score(self):
        row={k+"1":"3" for k in ("noprob","fit","burden","values","land","threat")}
        row["land1"]="."
        self.assertIsNone(response_index(row,"1"))

    def test_de_groot_two_node_average(self):
        x=np.array([0.0,1.0])
        y=evolve("degroot",x,((1,),(0,)),{"steps":1})
        np.testing.assert_allclose(y,[1.0,0.0])

    def test_fj_alpha_one_equals_degroot_all_frozen_steps(self):
        x=np.array([0.1,0.7,0.9])
        graph=((1,),(0,2),(1,))
        for step in STEPS:
            np.testing.assert_allclose(
                evolve("fj",x,graph,{"alpha":1.0,"steps":step}),
                evolve("degroot",x,graph,{"steps":step}))

    def test_fj_anchor_preserves_half_fixed_start(self):
        x=np.array([0.0,1.0])
        np.testing.assert_allclose(
            evolve("fj",x,((1,),(0,)),{"alpha":0.5,"steps":1}),[0.5,0.5])

    def test_isolates_de_groot_and_fj_unchanged(self):
        x=np.array([0.1,0.7,0.9])
        graph=((),(),())
        for m,p in (("degroot",{"steps":4}),("fj",{"steps":4,"alpha":0.75})):
            np.testing.assert_allclose(evolve(m,x,graph,p),x)

    def test_hk_global_full_confidence_consensus(self):
        x=np.array([0.0,0.2,1.0])
        y=evolve("hk",x,((),(),()),{"steps":1,"epsilon":1.0})
        np.testing.assert_allclose(y,[.4,.4,.4])

    def test_hk_small_radius_two_clusters(self):
        x=np.array([0.0,0.2,1.0])
        y=evolve("hk",x,((),(),()),{"steps":1,"epsilon":.3})
        np.testing.assert_allclose(y,[.1,.1,1.0])

    def test_unallowed_epsilon_fails_closed(self):
        with self.assertRaises(ValueError):
            evolve("hk",np.array([.1,.2]),((),()),{"epsilon":.6,"steps":1})

    def test_invalid_alpha_fails_closed(self):
        with self.assertRaises(ValueError):
            evolve("fj",np.array([.1,.2]),((1,),(0,)),
                   {"alpha":0.99,"steps":1})

    def test_all_grid_names_and_sizes_fixed(self):
        self.assertEqual(len(make_grid("persistence")),1)
        self.assertEqual(len(make_grid("degroot")),3)
        self.assertEqual(len(make_grid("fj")),12)
        self.assertEqual(len(make_grid("hk")),15)

    def test_only_training_village_outcomes_determine_selected_model(self):
        groups={
            "train":{"endline":np.array([.2,.8]),"mask":np.array([True,True])},
            "heldout":{"endline":np.array([.0,.0]),"mask":np.array([True,True])},
        }
        predictions={
            "candidate_a":{"train":np.array([.3,.7]),
                           "heldout":np.array([.1,.1])},
            "candidate_b":{"train":np.array([.4,.6]),
                           "heldout":np.array([.9,.9])},
        }
        a=choose_training(groups,predictions,"heldout")
        groups["heldout"]["endline"]=np.array([1.0,1.0])
        b=choose_training(groups,predictions,"heldout")
        self.assertEqual(a,b)

    def test_train_only_drift_equal_village_weight(self):
        groups={
            "train1":{"endline":np.array([.8,.8]),"mask":np.array([True,True])},
            "train2":{"endline":np.array([.4]),"mask":np.array([True])},
            "heldout":{"endline":np.array([0.]),"mask":np.array([True])},
        }
        predictor={"single":{k:np.zeros(len(v["endline"])) for k,v in groups.items()}}
        r=choose_training(groups,predictor,"heldout")
        self.assertAlmostEqual(r["train_drift"],.6,places=12)

    def test_variant_tie_follows_protocol_order(self):
        groups={
            "train":{"endline":np.array([.4]),"mask":np.array([True])},
            "heldout":{"endline":np.array([.5]),"mask":np.array([True])},
        }
        variants={
            "first":{name:np.array([.2]) for name in groups},
            "second":{name:np.array([.2]) for name in groups},
        }
        r=choose_training(groups,variants,"heldout")
        self.assertEqual(r["variant"],"first")

    def test_unknown_model_rejected(self):
        with self.assertRaises(ValueError):
            make_grid("unrecognized")
        with self.assertRaises(ValueError):
            evolve("unrecognized",np.array([0.5]),((),),{})

    def test_synthetic_repeated_predictions_stay_in_unit_interval(self):
        x=np.array([.01,.2,.98])
        g=((1,),(0,2),(1,))
        for model in CLASSES:
            for name,param in make_grid(model):
                y=evolve(model,x,g,param)
                self.assertTrue(np.all((y>=0)&(y<=1)),msg=f"{model}/{name}")

    def test_lovo_does_not_allow_one_village(self):
        with self.assertRaises(ValueError):
            score_lovo({"one":{}},{})


if __name__=="__main__":
    unittest.main()
