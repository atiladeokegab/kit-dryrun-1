import json
import unittest
from contextlib import redirect_stderr
from io import StringIO

from triage.__main__ import main, rank, render_json, render_table
from triage.model import Message, Triage


def t(i, urgency, category="other", reason=""):
    return Triage(Message(i, f"message {i}", sender="Sam"), urgency, category, reason)


class CliTest(unittest.TestCase):
    def test_rank_puts_most_urgent_first_then_dump_order(self):
        items = [t(1, "routine"), t(2, "emergency"), t(3, "urgent"), t(4, "emergency")]
        self.assertEqual([x.message.id for x in rank(items)], [2, 4, 3, 1])

    def test_json_shape(self):
        out = json.loads(render_json([t(1, "urgent", "leak", "leak")]))
        self.assertEqual(out, [{"id": 1, "urgency": "urgent", "category": "leak", "sender": "Sam",
                                "received": "", "text": "message 1", "reason": "leak"}])

    def test_table_has_header_and_one_row_per_message(self):
        lines = render_table([t(1, "urgent"), t(2, "routine")]).splitlines()
        self.assertEqual(len(lines), 3)
        self.assertIn("URGENCY", lines[0])
        self.assertIn("URGENT", lines[1])

    def test_missing_file_exits_2(self):
        with redirect_stderr(StringIO()) as err:
            self.assertEqual(main(["/no/such/file.txt"]), 2)
        self.assertIn("cannot read", err.getvalue())


if __name__ == "__main__":
    unittest.main()
