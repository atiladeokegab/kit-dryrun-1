import unittest

from triage.ingest import split


class SplitTests(unittest.TestCase):
    def test_blank_and_dash_boundaries_keep_order(self):
        messages = split(" first message \n\nsecond message\n-----\nthird message\n")
        self.assertEqual([(m.id, m.text) for m in messages],
                         [(1, "first message"), (2, "second message"), (3, "third message")])

    def test_email_headers_and_signoff(self):
        text = ("From: Priya Shah <priya@example.com>\nTo: agent@example.com\n"
                "Subject: Water\nDate: Mon, 28 Sep 2026 07:12\n\n"
                "A pipe has burst.\n\nPriya\n---\nnext message")
        first, second = split(text)
        self.assertEqual(first.sender, "Priya Shah <priya@example.com>")
        self.assertEqual(first.received, "Mon, 28 Sep 2026 07:12")
        self.assertEqual(first.text, "A pipe has burst.\nPriya")
        self.assertEqual((second.id, second.text), (2, "next message"))

    def test_from_header_starts_new_email_without_separator(self):
        messages = split("From: A\nfirst\nFrom: B\nsecond")
        self.assertEqual([(m.sender, m.text) for m in messages],
                         [("A", "first"), ("B", "second")])

    def test_both_sms_formats(self):
        text = ("[09:14] +447700900123: leaking tap\n\n"
                "28/09/2026 09:15 - Sam: broken lock")
        first, second = split(text)
        self.assertEqual((first.sender, first.received, first.text),
                         ("+447700900123", "09:14", "leaking tap"))
        self.assertEqual((second.sender, second.received, second.text),
                         ("Sam", "28/09/2026 09:15", "broken lock"))

    def test_voicemail_without_sender_uses_its_time(self):
        message, = split("Voicemail 09:40: hi it is Priya from flat 3")
        self.assertEqual((message.sender, message.received, message.text),
                         ("", "Voicemail 09:40", "hi it is Priya from flat 3"))

    def test_windows_line_endings_and_empty_input(self):
        messages = split("one\r\n\r\ntwo\r\n---\r\nthree\r\n")
        self.assertEqual([m.text for m in messages], ["one", "two", "three"])
        self.assertEqual(split(" \n\r\n -- \n "), [])


if __name__ == "__main__":
    unittest.main()
