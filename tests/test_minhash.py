import unittest
from src.minhash.minhash import U, k, VanillaMinHash, BufferedMinHash


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

    def test_insert_new_integer(self):
        A = {1, 2, 3}
        min_hash = VanillaMinHash(A)
        original_signature = min_hash.get_signature().copy()
        min_hash.insert(10)
        self.assertEqual(len(min_hash.get_signature()), k)

    def test_insert_existing_integer(self):
        A = {1, 2, 3}
        min_hash = VanillaMinHash(A)
        original_signature = min_hash.get_signature().copy()
        min_hash.insert(2)
        self.assertEqual(original_signature, min_hash.get_signature())

    def test_valid_subset(self):
        A = {0, 1, 2}
        min_hash = VanillaMinHash(A)
        self.assertEqual(min_hash.get_signature().__class__, list)


class TestBufferedMinHash(unittest.TestCase):

    def setUp(self):
        """Create a sample set for testing"""
        self.A = {1, 2, 3, 4}

    def test_signature_length(self):
        min_hash = BufferedMinHash(self.A)
        self.assertEqual(len(min_hash.get_signature()), k)

    def test_signature_deterministic(self):
        signature_1 = BufferedMinHash(self.A).get_signature()
        signature_2 = BufferedMinHash(self.A).get_signature()
        self.assertEqual(signature_1, signature_2)

    def test_signature_different_sets(self):
        A = {1, 2, 3}
        B = {4, 5, 6}
        signature_A = BufferedMinHash(A).get_signature()
        signature_B = BufferedMinHash(B).get_signature()
        self.assertNotEqual(signature_A, signature_B)

    def test_delete_existing_element(self):
        min_hash = BufferedMinHash(self.A)
        x = 2
        min_hash.delete(x)
        self.assertNotIn(x, min_hash.A)
        self.assertEqual(len(min_hash.get_signature()), k)

    def test_delete_nonexistent_element(self):
        min_hash = BufferedMinHash(self.A)
        x = 9  # Not in the set
        old_signature = min_hash.get_signature().copy()
        min_hash.delete(x)
        self.assertEqual(min_hash.A, self.A)
        self.assertEqual(old_signature, min_hash.get_signature())

    def test_delete_fault_reinitialization(self):
        small_set = {1}
        min_hash = BufferedMinHash(small_set)
        min_hash.delete(1)
        self.assertEqual(min_hash.A, set())
        for B, d in min_hash.SA:
            self.assertEqual(B, [])
            self.assertEqual(d, (float('inf'), float('inf')))

    def test_get_signature_type(self):
        min_hash = BufferedMinHash(self.A)
        self.assertIsInstance(min_hash.get_signature(), list)

    def test_insert_new_element(self):
        min_hash = BufferedMinHash(self.A)
        old_signature = min_hash.get_signature().copy()
        min_hash.insert(5)
        self.assertEqual(len(min_hash.get_signature()), k)

    def test_insert_existing_element(self):
        min_hash = BufferedMinHash(self.A)
        old_signature = min_hash.get_signature().copy()
        min_hash.insert(2)
        self.assertEqual(old_signature, min_hash.get_signature())
