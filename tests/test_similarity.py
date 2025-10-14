import unittest
from src.minhash.minhash import k
from src.minhash.similarity import jaccard_similarity, estimate_jaccard_similarity


class TestSimilarityFunctions(unittest.TestCase):

    def test_jaccard_similarity_basic(self):
        A = {1, 2, 3}
        B = {2, 3, 4}
        self.assertEqual(jaccard_similarity(A, B), 2/4)

    def test_jaccard_similarity_disjoint(self):
        A = {1, 2}
        B = {3, 4}
        self.assertEqual(jaccard_similarity(A, B), 0.0)

    def test_jaccard_similarity_identical(self):
        A = {1, 2, 3}
        B = {1, 2, 3}
        self.assertEqual(jaccard_similarity(A, B), 1.0)

    def test_jaccard_similarity_empty_A(self):
        A = set()
        B = {1, 2, 3}
        self.assertEqual(jaccard_similarity(A, B), 0.0)

    def test_jaccard_similarity_empty_B(self):
        A = {1, 2, 3}
        B = set()
        self.assertEqual(jaccard_similarity(A, B), 0.0)

    def test_jaccard_similarity_both_empty(self):
        A = set()
        B = set()
        self.assertEqual(jaccard_similarity(A, B), 1.0)

    def test_jaccard_similarity_partial_overlap(self):
        A = {1, 2, 3, 4}
        B = {3, 4, 5, 6}
        self.assertEqual(jaccard_similarity(A, B), 2 / 6)

    def test_jaccard_similarity_single_element_sets(self):
        A = {1}
        B = {1}
        self.assertEqual(jaccard_similarity(A, B), 1.0)

        A = {1}
        B = {2}
        self.assertEqual(jaccard_similarity(A, B), 0.0)

    def test_estimate_jaccard_similarity_all_match(self):
        signature_A = [i for i in range(k)]
        signature_B = [i for i in range(k)]
        self.assertEqual(estimate_jaccard_similarity(
            signature_A, signature_B), 1.0)

    def test_estimate_jaccard_similarity_none_match(self):
        signature_A = [i for i in range(k)]
        signature_B = [i + k for i in range(k)]
        self.assertEqual(estimate_jaccard_similarity(
            signature_A, signature_B), 0.0)

    def test_estimate_jaccard_similarity_half_match(self):
        signature_A = [i for i in range(k)]
        signature_B = [i for i in range(k//2)] + [i+k for i in range(k//2, k)]
        expected = (k // 2) / k
        self.assertEqual(estimate_jaccard_similarity(
            signature_A, signature_B), expected)

    def test_estimate_jaccard_similarity_empty_signatures(self):
        if k == 0:
            self.assertEqual(estimate_jaccard_similarity([], []), 0.0)
