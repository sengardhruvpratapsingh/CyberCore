import unittest
from types import SimpleNamespace

from app.forensic.risk import (
    MAX_RISK_SCORE,
    calculate_risk_assessment,
    calculate_risk_score,
    get_risk_level,
)


class RiskScoringTests(unittest.TestCase):
    def test_old_rule_matches_fixture_scores(self):
        self.assertEqual(calculate_risk_score(1, 0), 3)
        self.assertEqual(calculate_risk_score(1, 1), 5)
        self.assertEqual(calculate_risk_score(3, 3), 9)

    def test_old_rule_caps_at_ten(self):
        self.assertEqual(calculate_risk_score(10, 10), 9)
        self.assertEqual(MAX_RISK_SCORE, 10)

    def test_old_rule_uses_expected_risk_bands(self):
        self.assertEqual(get_risk_level(3), "LOW")
        self.assertEqual(get_risk_level(4), "MEDIUM")
        self.assertEqual(get_risk_level(6), "MEDIUM")
        self.assertEqual(get_risk_level(7), "HIGH")
        self.assertEqual(get_risk_level(10), "HIGH")

    def test_assessment_exposes_old_rule_breakdown(self):
        assessment = calculate_risk_assessment(
            transaction_chains=[{"transaction_ids": ["TXN-001"]}],
            high_value_transactions=[
                SimpleNamespace(transaction_id="TXN-002")
            ],
        )

        self.assertEqual(assessment["score"], 5)
        self.assertEqual(assessment["level"], "MEDIUM")
        self.assertEqual(assessment["maximum"], 10)
        self.assertEqual(assessment["display_denominator"], 10)
        self.assertEqual(
            [signal["points"] for signal in assessment["signals"]],
            [2, 2],
        )

    def test_no_observed_signals_start_at_one(self):
        assessment = calculate_risk_assessment(
            transaction_chains=[],
            high_value_transactions=[],
        )

        self.assertEqual(assessment["score"], 1)
        self.assertEqual(assessment["level"], "LOW")
        self.assertEqual(assessment["signals"], [])


if __name__ == "__main__":
    unittest.main()
