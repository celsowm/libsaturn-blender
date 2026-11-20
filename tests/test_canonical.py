import unittest
from libsaturn_toolkit.contract import canonical_bytes

class CanonicalTests(unittest.TestCase):
    def test_order_independent(self):
        a = {"id": "a", "kind": "ring", "position": [1, 2, 3]}
        b = {"id": "b", "kind": "goal", "position": [4, 5, 6]}
        self.assertEqual(canonical_bytes([a, b]), canonical_bytes([b, a]))
    def test_duplicate_rejected(self):
        a = {"id": "a", "kind": "ring", "position": [1, 2, 3]}
        with self.assertRaises(ValueError):
            canonical_bytes([a, a])
