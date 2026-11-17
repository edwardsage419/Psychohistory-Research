import unittest
import csv
import io
import json
from pathlib import Path
from source_join import identical_bytes,compare_sources,compare_risks

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'research/R273/R273_ALL_1728_ORIGINAL_CROSS_POPULATION_SOURCES.csv'
PAIR=ROOT/'research/validation/R273_S69_ALL_576_PAIRED_SOURCE_ROWS_2026-10-30.csv'

def rewritten(raw,edit):
    reader=csv.DictReader(io.StringIO(raw.decode(),newline=''));fields=reader.fieldnames;rows=list(reader)
    edit(rows)
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    return out.getvalue().encode()

class SourceJoinTests(unittest.TestCase):
    def test_changed_native_bytes_rejected(self):
        with self.assertRaises(ValueError):identical_bytes(b'1/4\n',b'1/2\n')

    def test_full_source_join_and_27_risks(self):
        result=compare_sources(PAIR.read_bytes(),BASE.read_bytes())
        self.assertEqual(result,{'paired_rows':576,'original_rows':1728,'model_source_joins':1728,'worlds':9,'probability_masses_each':4096})
        extension=json.loads((ROOT/'research/validation/R273_S69_PAIRED_TARGET_RANK_EXACT_RESULTS_2026-10-30.json').read_text())
        original=json.loads((ROOT/'research/R273/R273_EXACT_CROSS_POPULATION_RESULTS.json').read_text())
        self.assertEqual(compare_risks(extension,original),27)

    def test_each_source_order_is_independent(self):
        paired,base=PAIR.read_bytes(),BASE.read_bytes()
        wanted=compare_sources(paired,base)
        self.assertEqual(compare_sources(rewritten(paired,lambda rows:rows.reverse()),base),wanted)
        self.assertEqual(compare_sources(paired,rewritten(base,lambda rows:rows.reverse())),wanted)

    def test_bad_paired_source_rejected(self):
        paired,base=PAIR.read_bytes(),BASE.read_bytes()
        mutations=[lambda rows:rows.pop(),lambda rows:rows.__setitem__(-1,dict(rows[0]))]
        for field in ('weight_num_4096','source_forecast_num_12','source_score_num_288'):
            mutations.append(lambda rows,f=field:rows[0].__setitem__(f,str(int(rows[0][f])+1)))
        mutations.append(lambda rows:rows[0].__setitem__('paired_outcome','S_BETTER'))
        for i,mutate in enumerate(mutations):
            with self.subTest(case=i),self.assertRaises(ValueError):compare_sources(rewritten(paired,mutate),base)

    def test_bad_original_source_and_risk_rejected(self):
        base=rewritten(BASE.read_bytes(),lambda rows:rows.__setitem__(-1,dict(rows[0])))
        with self.assertRaises(ValueError):compare_sources(PAIR.read_bytes(),base)
        extension=json.loads((ROOT/'research/validation/R273_S69_PAIRED_TARGET_RANK_EXACT_RESULTS_2026-10-30.json').read_text())
        original=json.loads((ROOT/'research/R273/R273_EXACT_CROSS_POPULATION_RESULTS.json').read_text())
        original['world_results'][0]['complete_source_expected_target_test_Brier']='999'
        with self.assertRaises(ValueError):compare_risks(extension,original)

if __name__=='__main__':unittest.main(verbosity=2)
