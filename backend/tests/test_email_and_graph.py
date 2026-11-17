import unittest
from types import SimpleNamespace

from app.forensic.email_processor import process_eml_file
from app.forensic.unified_graph import build_unified_graph


class EmailAndGraphTests(unittest.TestCase):
    def test_process_eml_file_handles_utf8_bom(self):
        raw = (
            "\ufeffFrom: Alice <alice@example.com>\n"
            "To: Bob <bob@example.com>\n"
            "Reply-To: support@example.com\n"
            "Date: Tue, 21 Jan 2025 10:00:00 +0000\n"
            "Message-ID: <abc@test>\n"
            "Received: from mail.test (10.0.0.1)\n"
            "Subject: Test\n\n"
            "Body text\n"
        ).encode("utf-8")

        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.eml"
            path.write_bytes(raw)
            result = process_eml_file(str(path))

        self.assertIn("alice@example.com", result["from_address"])
        self.assertEqual(result["reply_to"], "support@example.com")
        self.assertEqual(result["source_ip"], "10.0.0.1")

    def test_build_unified_graph_includes_email_mismatch_edge(self):
        email_artifact = SimpleNamespace(
            id=1,
            message_id="<abc@test>",
            from_address="Alice <alice@example.com>",
            reply_to="support@example.com",
        )

        graph = build_unified_graph(
            transactions=[],
            device_records=[],
            email_artifacts=[email_artifact],
        )

        self.assertIn("alice@example.com", graph.nodes)
        self.assertIn("support@example.com", graph.nodes)
        self.assertTrue(any(
            data.get("kind") == "email"
            for _, _, data in graph.edges(data=True)
        ))


if __name__ == "__main__":
    unittest.main()
