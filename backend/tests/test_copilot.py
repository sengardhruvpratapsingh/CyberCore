import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

from pydantic import ValidationError

from app.forensic.copilot import (
    answer_with_router,
    execute_tool,
    validate_tool_selection,
)
from app.forensic.slm import SLMSelectionError
from app.schemas.copilot import ToolSelection


class CopilotTests(unittest.TestCase):
    def setUp(self):
        self.transaction = SimpleNamespace(
            id=1,
            transaction_id="TX-001",
            sender="A",
            receiver="B",
            amount=120000.0,
            timestamp=datetime(2025, 1, 1, 10, 0),
        )
        self.device = SimpleNamespace(
            id=2,
            record_id="DEV-001",
            phone_number="999",
            imei="359123456789012",
            timestamp=datetime(2025, 1, 1, 11, 0),
        )
        self.data = {
            "transactions": [self.transaction],
            "device_records": [self.device],
            "email_artifacts": [],
            "chains": [],
            "high_value": [self.transaction],
            "shared_devices": [],
            "email_findings": [],
            "risk_score": 8,
            "risk_level": "HIGH",
            "risk_signals": [{"name": "high value", "points": 2}],
            "risk_score_maximum": 10,
            "risk_score_display_denominator": 10,
        }

    def test_valid_selection_and_arguments(self):
        self.assertEqual(
            validate_tool_selection({
                "tool": "get_connected_entities",
                "arguments": {
                    "entity_type": "IMEI",
                    "entity_value": "359123456789012",
                },
            }),
            ("get_connected_entities", {
                "entity_type": "IMEI",
                "entity_value": "359123456789012",
            }),
        )

    def test_unknown_tool_rejected(self):
        with self.assertRaises(ValidationError):
            validate_tool_selection({"tool": "run_sql", "arguments": {}})

    def test_malformed_arguments_rejected(self):
        with self.assertRaises(ValidationError):
            validate_tool_selection({"tool": "get_risk_findings", "arguments": {"score": 99}})

    @patch("app.forensic.copilot.select_tool")
    def test_malformed_json_selection_falls_back(self, select_tool):
        select_tool.side_effect = SLMSelectionError("malformed")
        response = answer_with_router("What is the risk score?", self.data)
        self.assertEqual(response["mode"], "fallback")
        self.assertEqual(response["tool"], "get_risk_findings")

    @patch("app.forensic.copilot.select_tool")
    def test_ollama_unavailable_falls_back(self, select_tool):
        select_tool.side_effect = SLMSelectionError("unavailable")
        response = answer_with_router("Show high value transactions", self.data)
        self.assertEqual(response["mode"], "fallback")
        self.assertEqual(response["result"]["transaction_count"], 1)

    @patch("app.forensic.copilot.select_tool")
    def test_timeout_falls_back(self, select_tool):
        select_tool.side_effect = SLMSelectionError("timeout")
        response = answer_with_router("Show email findings", self.data)
        self.assertEqual(response["mode"], "fallback")
        self.assertEqual(response["tool"], "get_email_findings")

    @patch("app.forensic.slm.urlopen")
    def test_invalid_ollama_response_shape_falls_back(self, urlopen):
        urlopen.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.dict("os.environ", {"CYBERCORE_SLM_ENABLED": "true"}):
            response = answer_with_router("What is the risk score?", self.data)
        self.assertEqual(response["mode"], "fallback")
        self.assertEqual(response["tool"], "get_risk_findings")

    @patch("app.forensic.copilot.select_tool")
    def test_valid_slm_selection_executes_allowlisted_tool(self, select_tool):
        select_tool.return_value = ToolSelection(tool="get_risk_findings", arguments={})
        response = answer_with_router("Assess this case", self.data)
        self.assertEqual(response["mode"], "slm")
        self.assertEqual(response["tool"], "get_risk_findings")
        self.assertEqual(response["result"]["risk_score"], 8)

    def test_tool_execution_rejects_non_allowlisted_tool(self):
        with self.assertRaises(ValidationError):
            execute_tool("delete_all", {}, self.data)

    @patch("app.forensic.copilot.select_tool")
    def test_risk_result_and_answer_remain_grounded(self, select_tool):
        select_tool.return_value = ToolSelection(tool="get_risk_findings", arguments={})
        response = answer_with_router("What is the risk?", self.data)
        self.assertEqual(response["result"]["risk_score"], self.data["risk_score"])
        self.assertEqual(response["result"]["risk_level"], self.data["risk_level"])
        self.assertIn("8/10", response["answer"])
        self.assertNotIn("guilty", response["answer"].lower())
        self.assertNotIn("criminal", response["answer"].lower())

    @patch("app.forensic.copilot.select_tool")
    def test_unsupported_question_returns_limitation(self, select_tool):
        select_tool.side_effect = SLMSelectionError("invalid")
        response = answer_with_router("What will happen next year?", self.data)
        self.assertIsNone(response["tool"])
        self.assertTrue(response["limitations"])


if __name__ == "__main__":
    unittest.main()
