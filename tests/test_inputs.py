import unittest

from source_fixture import load


class ExchangeInputs(unittest.TestCase):
    def test_related_source_records(self):
        exchange = load()
        initial = exchange["initial"]
        changes = exchange["changes"]
        self.assertNotIn(2, initial["/pos/closures"]["body"]["ranges"][0]["empty"])
        late = changes[1]["routes"]["/pos/sync"]["body"]["entries"][0]
        previous = changes[0]["routes"]["/merchant/progress"]["body"]["refunds"][0]
        self.assertEqual(late["right"], previous["right"])
        self.assertLess(late["occurred"], previous["time"])
