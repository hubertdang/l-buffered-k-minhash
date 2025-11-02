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

    # Accuracy (static): |estimated JS - true JS|
    # Accuracy (dynamic): |estimated JS - true JS| after deletions
    # Query speed (static): speed of get_signature operation
    # Query speed (dynamic):
    # Frequency of faults and cost of recovery in buffered k-MinHash


if __name__ == "__main__":
    main()
