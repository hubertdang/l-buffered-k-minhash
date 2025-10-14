import unittest
from src.minhash.minhash import k, VanillaMinHash


class TestVanillaMinHash(unittest.TestCase):

    def test_signature_length(self):
        A = {1, 2, 3}
        min_hash = VanillaMinHash(A)
        self.assertEqual(len(min_hash.get_signature()), k)

    def test_signature_deterministic(self):
        A = {1, 2, 3}
        signature_1 = VanillaMinHash(A).get_signature()
        signature_2 = VanillaMinHash(A).get_signature()
        self.assertEqual(signature_1, signature_2)

    def test_signature_different_sets(self):
        A = {1, 2, 3}
        B = {4, 5, 6}
        signature_A = VanillaMinHash(A).get_signature()
        signature_B = VanillaMinHash(B).get_signature()
        self.assertNotEqual(signature_A, signature_B)

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            VanillaMinHash([1, 2, 3])

    def test_empty_set(self):
        A = set()
        with self.assertRaises(ValueError):
            min_hash = VanillaMinHash(A)
