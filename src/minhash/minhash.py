import mmh3
import math

N = 100000
U = set(range(N))  # the simulated universe

k = 128
l = 34

# k hash functions that are uniformly at random (UAR)
h = [lambda x, seed=i: mmh3.hash(str(x), seed=seed) for i in range(k)]


def H(A: set, h_i) -> list:
    """Apply a hash function h_i to all elements a of set A"""
    return {h_i(a) for a in A}


def smallest(X: set, r: int) -> list:
    """Return the r smallest unique elements of X"""
    return sorted(X)[:r]


class VanillaMinHash:
    """A k-MinHash sketch"""

    def __init__(self, A: set):
        if not isinstance(A, set):
            raise TypeError("A must be of type 'set'")

        if len(A) == 0:
            raise ValueError("A must not be empty")

        if not A.issubset(U):
            raise ValueError("A is not a subset of the universe U")

        self.signature = []

        for i in range(k):
            h_i = h[i]
            self.signature.append(min(H(A, h_i)))

    def get_signature(self):
        """
        Get the sketch's k-MinHash signature, a list of k MinHashes computed
        from k hash functions
        """
        return self.signature

    def insert(self, x: int):
        """
        Insert an element x into the sketch and update the k-MinHash signature
        if necessary
        """
        if not isinstance(x, int):
            raise TypeError("x must be of type 'int'")

        for i in range(k):
            h_i = h[i]

            if h_i(x) < self.signature[i]:
                self.signature[i] = h_i(x)


class BuferredMinHash:
    """An l-buffered k-MinHash sketch"""

    def __init__(self, A: set):
        if not isinstance(A, set):
            raise TypeError("A must be of type 'set'")

        if not A.issubset(U):
            raise ValueError("A is not a subset of the universe U")

        self.sketch = []

        for i in range(k):
            h_i = h[i]
            B_Ai = smallest(H(A, h_i), l)
            d = None

            if len(B_Ai) == l:
                d = max(B_Ai)
            else:
                d = (math.inf, math.inf)

            self.sketch.append(B_Ai, d)

    def get_signature(self):
        """
        Get the sketch's k-MinHash signature, a list of k MinHashes computed
        from k hash functions
        """
        signature = []

        for i in range(k):
            signature.append(min(self.sketch[i][0]))

        return signature
