#!/usr/bin/env python3

import random
from src.minhash.minhash import k, VanillaMinHash
from src.minhash.similarity import jaccard_similarity, estimate_jaccard_similarity

SIZE = 10000


def main():
    A = set(random.sample(range(SIZE+5000), SIZE))
    B = set(random.sample(range(SIZE+5000), SIZE))

    S_A = VanillaMinHash(A)
    S_B = VanillaMinHash(B)

    actual = jaccard_similarity(A, B)
    estimate = estimate_jaccard_similarity(
        S_A.get_signature(), S_B.get_signature())

    print("Actual Jaccard similarity: " + str(actual))
    print("Estimated Jaccard similarity: " + str(estimate))


if __name__ == "__main__":
    main()
