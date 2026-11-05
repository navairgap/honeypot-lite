import json
import tempfile
import unittest
from pathlib import Path

from honeypot import EventWriter, _clean, _loopback


class HoneypotSafetyTests(unittest.TestCase):
    def test_event_log_obeys_byte_and_event_quotas(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            writer = EventWriter(path, max_bytes=1000, max_events=1)
            self.assertTrue(writer.record({"event": "first"}))
            self.assertFalse(writer.record({"event": "second"}))
            self.assertEqual(len(path.read_text().splitlines()), 1)

    def test_existing_log_size_counts_toward_quota(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text("x" * 100, encoding="utf-8")
            writer = EventWriter(path, max_bytes=100, max_events=10)
            self.assertFalse(writer.record({"event": "too-large"}))

    def test_input_metadata_is_printable_and_bounded(self):
        self.assertEqual(_clean("ok\\n\\x1b[31m", 20), "ok[31m")
        self.assertEqual(len(_clean("a" * 300, 20)), 20)

    def test_public_bind_requires_explicit_confirmation(self):
        self.assertTrue(_loopback("127.0.0.1"))
        self.assertTrue(_loopback("::1"))
        self.assertFalse(_loopback("0.0.0.0"))
        self.assertFalse(_loopback("192.0.2.1"))

    def test_jsonl_events_are_parseable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "events.jsonl"
            writer = EventWriter(path)
            self.assertTrue(writer.record({"path": "/health", "remote_ip": "127.0.0.1"}))
            event = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(event["path"], "/health")


if __name__ == "__main__":
    unittest.main()
