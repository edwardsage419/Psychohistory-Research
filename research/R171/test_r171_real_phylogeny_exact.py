"""R171 real (not synthesized) Gray 2009 Austronesian tree checks.

Evidence: source-descriptive exact arithmetic on already inferred Phlorest
linguistic source; tests do not establish origin-of-population predictions.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import unittest
from decimal import Decimal as D
from pathlib import Path
from r171_real_phylogeny_exact import (
    ORIGINAL_REPO,SOURCE_COMMIT,ORIGINAL_DOI,BLOB_SHA1,EXPECTED_BYTES,
    SOURCE,PAIRS,git_blob_id,verify_input,read_sources,newick_from_nexus,
    length_exact,parse_recursive,parse_iterative,flatten,root_depths,
    lca_distance,independent_undirected_paths,taxon_crosswalk,
    source_metadata_check,save_and_document
)


class TestR171(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=read_sources()
        cls.newick=newick_from_nexus(cls.raw["summary.trees"])
        cls.a=parse_recursive(cls.newick)
        cls.b=parse_iterative(cls.newick)
        cls.flat=flatten(cls.a)
        cls.depth=root_depths(cls.flat)
        cls.doc=save_and_document()

    def test_pinned_repository_full_identity(self):
        self.assertEqual(ORIGINAL_REPO,"phlorest/gray_et_al2009")
        self.assertEqual(SOURCE_COMMIT,"a2e535f07c05d214fe7d36fe03747f4cfd5f9ca5")

    def test_primary_paper_original_DOI(self):
        self.assertEqual(ORIGINAL_DOI,"10.1126/science.1166858")

    def test_all_four_original_hashes_against_git_blobs(self):
        for filename,original_bytes in self.raw.items():
            self.assertEqual(git_blob_id(original_bytes),BLOB_SHA1[filename])

    def test_all_four_original_raw_byte_lengths(self):
        for filename,original_bytes in self.raw.items():
            self.assertEqual(len(original_bytes),EXPECTED_BYTES[filename])

    def test_all_four_original_sha256_listed_in_output(self):
        refs=self.doc["source_identities"]
        self.assertEqual(set(refs),set(BLOB_SHA1))
        for filename,data in self.raw.items():
            self.assertEqual(refs[filename]["sha256"],hashlib.sha256(data).hexdigest())

    def test_original_source_hash_fails_if_modified(self):
        for filename,contents in self.raw.items():
            with self.assertRaises(ValueError):
                verify_input(filename,contents+b"x")

    def test_unknown_input_source_rejected(self):
        with self.assertRaises(ValueError):verify_input("invented_tree.nex",b"")

    def test_nonbyte_source_rejected(self):
        with self.assertRaises(ValueError):verify_input("summary.trees","fake")

    def test_actual_NEXUS_root_marker(self):
        self.assertTrue(self.raw["summary.trees"].startswith(b"#NEXUS"))
        self.assertIn(b"[&R]",self.raw["summary.trees"])

    def test_exactly_one_named_summary_tree(self):
        self.assertEqual(self.raw["summary.trees"].count(b"tree summary = "),1)

    def test_newick_contains_terminal_semicolon(self):
        self.assertTrue(self.newick.endswith(";"))
        self.assertTrue(self.newick.startswith("("))

    def test_independent_parser_canonical_tree_exact_match(self):
        self.assertEqual(self.a,self.b)

    def test_independent_parser_tip_label_count_exact_match(self):
        self.assertEqual(set(flatten(self.a)["tips"]),set(flatten(self.b)["tips"]))

    def test_independent_parser_branch_lengths_exact_match(self):
        self.assertEqual(flatten(self.a)["length"],flatten(self.b)["length"])

    def test_original_tree_terminal_labels_unique(self):
        ids=list(self.flat["tips"])
        self.assertEqual(len(ids),len(set(ids)))

    def test_original_tree_has_more_than_350_tips(self):
        self.assertGreater(len(self.flat["tips"]),350)

    def test_all_original_edges_have_nonnegative_decimal_length(self):
        lengths=self.flat["length"]
        self.assertIsNone(lengths[0])
        self.assertTrue(all(isinstance(v,D) and v>=0 for v in lengths[1:]))

    def test_every_original_internal_node_has_degree_at_least_two(self):
        for kids in self.flat["children"]:
            if kids:self.assertGreaterEqual(len(kids),2)

    def test_tree_has_connected_parent_graph(self):
        parents=self.flat["parent"]
        self.assertIsNone(parents[0])
        self.assertTrue(all(isinstance(x,int) and x<i for i,x in enumerate(parents) if i))

    def test_tree_node_edge_relation(self):
        self.assertEqual(len(self.flat["parent"])-1,len(self.flat["length"])-1)

    def test_exact_total_branch_length_matches_json(self):
        self.assertEqual(str(sum(self.flat["length"][1:],D(0))),
                         self.doc["tree_summary"]["total_branch_length"])

    def test_independent_root_to_tip_heights_nonnegative(self):
        self.assertTrue(all(self.depth[i]>=0 for i in self.flat["tips"].values()))

    def test_original_CLDF_language_ID_header(self):
        self.assertEqual(self.raw["languages.csv"].decode("utf-8-sig").splitlines()[0].split(",")[0],"ID")

    def test_original_summary_tree_declares_millennia(self):
        self.assertEqual(source_metadata_check(self.raw)["CLDF_branch_length_unit"],"millennia")

    def test_CLDF_tree_rooted_field_recorded_not_filled_by_guess(self):
        row=source_metadata_check(self.raw)
        self.assertEqual(row["CLDF_rooted_field"],"")
        self.assertEqual(row["rooted_NEXUS_marker"],"[&R]")

    def test_CLDF_metadata_has_language_and_tree_tables(self):
        tables=source_metadata_check(self.raw)["CLDF_tables_present"]
        self.assertIn("languages.csv",tables)
        self.assertIn("trees.csv",tables)

    def test_original_tip_coverage_exact_recomputed(self):
        self.assertEqual(taxon_crosswalk(self.raw["languages.csv"],self.flat["tips"]),
                         self.doc["crosswalk"])

    def test_language_table_duplicate_ids_rejected(self):
        bad=b"ID,Name\nTest,one\nTest,two\n"
        with self.assertRaises(ValueError):
            taxon_crosswalk(bad,{"Test"})

    def test_language_table_missing_id_column_rejected(self):
        with self.assertRaises(ValueError):
            taxon_crosswalk(b"Name,Some\nA,a\n",{"A"})

    def test_languages_not_substituted_by_generated_tip_names(self):
        actual=set(self.flat["tips"])
        all_ids=set(row["ID"] for row in csv.DictReader(
            io.StringIO(self.raw["languages.csv"].decode("utf-8-sig"))))
        self.assertEqual(self.doc["crosswalk"]["common_taxon_ids"],len(actual&all_ids))

    def test_pairwise_count_is_n_choose_two(self):
        n=len(self.flat["tips"])
        self.assertEqual(self.doc["complete_pairwise_distances"]["number_of_unordered_pairs"],n*(n-1)//2)

    def test_full_pairwise_CSV_is_original_complete_not_summary_only(self):
        file=Path(__file__).with_name("R171_ALL_PAIR_PATRISTIC_DISTANCES.csv")
        contents=file.read_bytes()
        self.assertEqual(hashlib.sha256(contents).hexdigest(),
                         self.doc["complete_pairwise_distances"]["original_full_matrix_csv_sha256"])
        self.assertEqual(len(contents),
                         self.doc["complete_pairwise_distances"]["original_full_matrix_csv_bytes"])

    def test_full_CSV_column_names(self):
        rows=csv.reader(io.StringIO(Path(__file__).with_name("R171_ALL_PAIR_PATRISTIC_DISTANCES.csv").read_text()))
        self.assertEqual(next(rows),["taxon_A","taxon_B","patristic_distance_millennia"])

    def test_CSV_sorted_pairs_and_no_self_pairs(self):
        data=csv.DictReader(Path(__file__).with_name("R171_ALL_PAIR_PATRISTIC_DISTANCES.csv").open())
        last=None;total=0
        for row in data:
            p=(row["taxon_A"],row["taxon_B"])
            self.assertLess(*p)
            if last:self.assertLess(last,p)
            last=p;total+=1
        self.assertEqual(total,self.doc["complete_pairwise_distances"]["number_of_unordered_pairs"])

    def test_full_all_pairs_source_distance_routes_agree(self):
        self.assertTrue(self.doc["complete_pairwise_distances"]["independent_all_pairs_ancestry_and_graph_walk_equal"])

    def test_every_named_taxon_has_zero_self_distance(self):
        for label in self.flat["tips"]:
            self.assertEqual(lca_distance(self.flat,self.depth,label,label),0)

    def test_full_graph_oracle_zero_self_distance(self):
        for label in self.flat["tips"]:
            self.assertEqual(independent_undirected_paths(self.flat,label)[label],0)

    def test_metric_symmetry_for_all_frozen_tip_pairs(self):
        for left,right in PAIRS:
            if left in self.flat["tips"] and right in self.flat["tips"]:
                self.assertEqual(lca_distance(self.flat,self.depth,left,right),
                                 lca_distance(self.flat,self.depth,right,left))

    def test_tree_distance_inferred_from_existing_tree_not_external_ground_truth(self):
        self.assertEqual(self.doc["new_human_independent_predictions"],0)
        self.assertEqual(self.doc["new_external_historical_predictions"],0)
        self.assertFalse(self.doc["original_Bayesian_posterior_inference_reproduced"])

    def test_source_descriptive_scientific_status(self):
        self.assertEqual(self.doc["scientific_status"],
                         "E1_SOURCE_DESCRIPTIVE_REAL_PUBLISHED_TREE_NOT_HISTORICAL_PREDICTION")

    def test_invalid_newick_truncated_rejected_by_both(self):
        for source in ("(A:1,B:2)","(A:1,B:2","(A:1,B:2));", ""):
            for parser in (parse_recursive,parse_iterative):
                with self.assertRaises(ValueError):parser(source)

    def test_invalid_newick_single_child_rejected_by_both(self):
        for parser in (parse_recursive,parse_iterative):
            with self.assertRaises(ValueError):parser("(A:1);")

    def test_duplicate_tip_rejected_on_flatten(self):
        for parser in (parse_recursive,parse_iterative):
            with self.assertRaises(ValueError):
                flatten(parser("(A:1,A:1);"))

    def test_invalid_negative_branch_rejected(self):
        for parser in (parse_recursive,parse_iterative):
            with self.assertRaises(ValueError):parser("(A:-1,B:2);")

    def test_nonfinite_branch_length_rejected(self):
        for number in ("NaN","Inf","Infinity","-Infinity"):
            with self.assertRaises(ValueError):length_exact(number)

    def test_malformed_branch_decimal_rejected(self):
        for number in ("", "aaa", "0xx", "--1"):
            with self.assertRaises(ValueError):length_exact(number)

    def test_root_length_rejected(self):
        with self.assertRaises(ValueError):flatten(parse_recursive("(A:1,B:2):3;"))

    def test_missing_terminal_label_rejected(self):
        for parser in (parse_recursive,parse_iterative):
            with self.assertRaises(ValueError):parser("(A:1,:2);")

    def test_invalid_newick_unterminated_quotes_rejected_by_independent(self):
        with self.assertRaises(ValueError):parse_iterative("('A:1,B:2);")

    def test_newick_polytomy_round_trip_two_parsers(self):
        text="(A:1,B:2,C:0,D:3);"
        self.assertEqual(parse_recursive(text),parse_iterative(text))
        self.assertEqual(len(parse_recursive(text)[2]),4)

    def test_newick_nested_topology_round_trip(self):
        text="((A:1,B:2):3,(C:0,D:5):2);"
        self.assertEqual(parse_recursive(text),parse_iterative(text))

    def test_newick_scientific_length_not_float_rounding(self):
        text="(A:0.000000000000123,B:1e-13);"
        self.assertEqual(parse_recursive(text),parse_iterative(text))
        self.assertEqual(parse_recursive(text)[2][0][1],D("0.000000000000123"))

    def test_malformed_nexus_header_rejected(self):
        with self.assertRaises(ValueError):
            newick_from_nexus(b"BEGIN TREES;\ntree summary = [&R] (A:1,B:1);\nEND;")

    def test_nonrooted_nexus_declaration_rejected(self):
        with self.assertRaises(ValueError):
            newick_from_nexus(b"#NEXUS\nBEGIN TREES;\ntree summary = [&U] (A:1,B:1);\nEND;")

    def test_multiple_trees_rejected(self):
        with self.assertRaises(ValueError):
            newick_from_nexus(b"#NEXUS\nBEGIN TREES;\ntree summary = [&R] (A:1,B:1);\ntree other = [&R] (A:1,B:1);\nEND;")

    def test_missing_source_tip_distance_is_explicitly_invalid(self):
        with self.assertRaises(ValueError):
            lca_distance(self.flat,self.depth,"nonexistent-language","SquliqAtayal")

    def test_preselected_pair_results_match_original_tree(self):
        for item in self.doc["preregistered_original_language_tip_pairs"]:
            if item["tip_pair_found"]:
                self.assertEqual(D(item["distance_millennia"]),
                                 lca_distance(self.flat,self.depth,item["taxon_A"],item["taxon_B"]))

    def test_distance_statistics_min_max_order(self):
        p=self.doc["complete_pairwise_distances"]
        self.assertGreaterEqual(D(p["mean_distance"]),D(p["minimum_distance"]))
        self.assertLessEqual(D(p["mean_distance"]),D(p["maximum_distance"]))

    def test_frozen_protocol_pair_list_pinned_count(self):
        self.assertEqual(len(PAIRS),9)

    def test_root_depth_extrema_in_output(self):
        heights=[self.depth[idx] for idx in self.flat["tips"].values()]
        self.assertEqual(str(min(heights)),self.doc["tree_summary"]["minimum_tip_root_height"])
        self.assertEqual(str(max(heights)),self.doc["tree_summary"]["maximum_tip_root_height"])

    def test_canonical_JSON_bytes(self):
        p=Path(__file__).with_name("R171_EXACT_RESULTS.json")
        if not p.exists():self.skipTest("initial pipeline generates original JSON before unittest")
        want=(json.dumps(self.doc,sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(p.read_bytes(),want)


# All frozen named pairs independently check original tip identity and exact
# LCA-vs-undirected-DFS distances, not synthetic oracle success variables.
for left,right in PAIRS:
    def create_pair(left=left,right=right):
        def test(self):
            src=self.flat["tips"]
            self.assertIn(left,src)
            self.assertIn(right,src)
            a=lca_distance(self.flat,self.depth,left,right)
            b=independent_undirected_paths(self.flat,left)[right]
            self.assertEqual(a,b)
            self.assertGreater(a,0)
        return test
    setattr(TestR171,"test_pinned_pair_"+left+"_and_"+right,create_pair())


ORIGINAL_TIP_CHECKS=(
"SquliqAtayal","CiuliAtayal","Sediq","Saisiat","Pazeh","Favorlang","Thao",
"Bunun","CentralAmis","Kavalan","Basai","Siraya","Paiwan","Bali","Sasak",
"Gayo","Javanese","OldJavanese","Lampung","Komering","Madurese","Sunda",
"Kerinci","Minangkabau","Ogan","MalayBahasaIndonesia","Melayu",
"Kanakanabu","Saaroa","Rukai","Tsou","OldChinese","Buyang"
)
for name in ORIGINAL_TIP_CHECKS:
    def create_tip(name=name):
        def test(self):
            self.assertIn(name,self.flat["tips"])
            self.assertGreaterEqual(self.depth[self.flat["tips"][name]],0)
        return test
    setattr(TestR171,"test_original_historical_tip_"+name,create_tip())


if __name__=="__main__":
    unittest.main()
