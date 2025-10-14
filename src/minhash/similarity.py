from .minhash import k


def jaccard_similarity(A: set, B: set) -> float:
    """Get the jaccard similarity between sets A and B"""
    if not A and not B:
        return 1.0
    return len(A.intersection(B)) / len(A.union(B))


def estimate_jaccard_similarity(signature_A: list, signature_B: list) -> float:
    """
    Estimate the jaccard similarity between two sets A and B using their
    k-MinHash signatures
    """
    num_matches = 0

    for i in range(k):
        if signature_A[i] == signature_B[i]:
            num_matches += 1

    return num_matches/k
