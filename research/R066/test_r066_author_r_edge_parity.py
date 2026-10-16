"""R066 explicit full-set R/Python edge parity; synthetic-only inputs."""
import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from r066_author_r_edge_parity import (
    canonical, compare_edges, export_canonical_edges, parse_r_edge_file,
    python_edge_sets, read_author_rows,
)


def synthetic_rows():
    def row(v,hh,ego,members,visit):
        x={"village_number":v,"hhnum":hh,"ego":ego,"hhh":members[0]}
        for i in range(1,12):
            x["hh"+str(i)] = members[i] if len(members)>i else ""
        for family in ("visit","meal","borrow","rumor"):
            for n in range(1,6):
                x[family+str(n)]=""
        x["visit1"]=visit
        return x
    return [
        row("1","2","egoA",["familyA"],"familyB"),
        row("1","1","egoB",["familyB"],"familyA"),
        row("2","1","egoC",["familyC"],"familyB"), # no cross village mapping
    ]


class ParityContracts(unittest.TestCase):
    def test_canonical_undirected(self):
        self.assertEqual(canonical("1","visit",1,2),
                         canonical("1","visit",2,1))

    def test_parity_distinguishes_equal_edge_counts_with_different_sets(self):
        one={("1","visit",1,2),("1","meal",1,3)}
        two={("1","visit",1,2),("1","meal",2,3)}
        self.assertEqual(compare_edges(one,two)["status"],
                         "AUTHOR_R_CORE_EDGE_PARITY_FAIL")
        self.assertEqual(compare_edges(one,two)["only_r_edges"],1)

    def test_perfect_parity_reports_zero_differences(self):
        a={("1","visit",1,2),("1","borrow",1,2)}
        r=compare_edges(a,set(a))
        self.assertEqual(r["status"],"AUTHOR_R_CORE_EDGE_PARITY_PASS")
        self.assertEqual(r["only_r_edges"],0)
        self.assertEqual(r["only_python_edges"],0)

    def test_no_source_edges_rejects_fabricated_pass(self):
        with self.assertRaises(ValueError):
            compare_edges(set(),set())

    def test_synthetic_village_does_not_cross_join(self):
        rows=synthetic_rows()
        e=python_edge_sets(rows,require_full=False)
        self.assertEqual(e,{("1","visit",1,2)})

    def test_synthetic_ego_multi_household_expands_correctly(self):
        rows=synthetic_rows()
        rows[0]["hh1"]="familyB"  # one person in both households
        e=python_edge_sets(rows,require_full=False)
        self.assertEqual(e,{("1","visit",1,2)})

    def test_local_r_undirected_file_round_trip_only(self):
        edges={("1","visit",1,2),("2","meal",3,4)}
        with TemporaryDirectory() as d:
            f=Path(d)/"ephemeral_edges.tsv"
            export_canonical_edges(edges,f)
            self.assertEqual(parse_r_edge_file(f),edges)

    def test_duplicate_r_edges_are_rejected(self):
        with TemporaryDirectory() as d:
            f=Path(d)/"corrupt.tsv"
            f.write_text("1\tvisit\t1\t2\n1\tvisit\t2\t1\n")
            with self.assertRaises(ValueError):
                parse_r_edge_file(f)

    def test_no_person_identifiers_in_aggregate(self):
        r=compare_edges({("1","visit",1,2)},{("1","visit",1,2)})
        self.assertNotIn("egoA",str(r))
        self.assertFalse(r["individual_edges_emitted"])

    def test_nonexistent_original_files_fail_closed(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(OSError):
                read_author_rows(Path(d))

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValueError):
            canonical("1","PRIVATE_PERSONAL_NAME",1,2)


if __name__=="__main__":
    unittest.main()
