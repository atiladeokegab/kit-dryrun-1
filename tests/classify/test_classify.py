import unittest

from triage.classify import classify
from triage.model import Message


class ClassifyTests(unittest.TestCase):
    def classify(self, text):
        return classify(Message(1, text))

    def test_emergency_beats_urgent(self):
        for text in ("Burst pipe and a leak", "FLOODING kitchen", "smell of gas",
                     "sparking socket", "fire in the flat", "smoke alarm",
                     "no heating and a newborn is here"):
            with self.subTest(text=text):
                self.assertEqual(self.classify(text).urgency, "emergency")

    def test_urgent_and_routine(self):
        for text in ("leaking tap", "no hot water", "boiler is off", "broken lock",
                     "mould on the wall", "rats in the kitchen"):
            with self.subTest(text=text):
                self.assertEqual(self.classify(text).urgency, "urgent")
        self.assertEqual(self.classify("parking question").urgency, "routine")

    def test_each_category(self):
        cases = {"burst pipe": "leak", "boiler off": "heating",
                 "sparks from socket": "electrical", "mice in kitchen": "pest",
                 "loud noise": "noise", "rent receipt": "admin", "hello": "other"}
        for text, category in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.classify(text).category, category)

    def test_whole_words_and_reason(self):
        self.assertEqual(self.classify("SMOKE").reason, "smoke")
        self.assertEqual(self.classify("smoker near a leaker").urgency, "routine")
        self.assertEqual(self.classify("hello").reason, "")


if __name__ == "__main__":
    unittest.main()
