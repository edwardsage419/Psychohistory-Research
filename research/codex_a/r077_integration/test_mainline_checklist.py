import copy
import unittest
from pathlib import Path

import mainline_checklist as checklist

ROOT = Path(__file__).resolve().parents[3]


class ChecklistTests(unittest.TestCase):
    def test_current_source_and_retained_evidence_keep_production_blocked(self):
        result = checklist.verify(ROOT)
        self.assertIs(result['production_ready'], False)
        self.assertEqual(result['exit_code'], 2)
        self.assertEqual(result['original_failure_cases'], 11)
        self.assertEqual(result['candidate_correct_orders'], 35)
        self.assertEqual(result['mathematical_programs_rerun'], False)
        self.assertEqual(result['checks']['production_hook'], 'NOT_INSTALLED')

    def test_retained_fake_success_is_rejected(self):
        data, _ = checklist.retained(ROOT)
        for field, value in [('production_ready', True), ('original_failure_cases', 0)]:
            changed = copy.deepcopy(data);changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                checklist.validate_evidence(changed, data['sources'], data['candidate_shadow']['sources'])

    def test_retained_input_identity_change_is_rejected(self):
        data, _ = checklist.retained(ROOT)
        sources = copy.deepcopy(data['candidate_shadow']['sources'])
        sources[next(iter(sources))]['sha256'] = '0'*64
        with self.assertRaises(ValueError):checklist.validate_evidence(data, data['sources'], sources)


if __name__ == '__main__':unittest.main()
