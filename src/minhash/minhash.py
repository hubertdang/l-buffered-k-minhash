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
    return {(h_i(a), a) for a in A}


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
            self.signature.append(min(H(A, h[i])))

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
            if (h[i](x), x) < self.signature[i]:
                self.signature[i] = (h[i](x), x)


class BufferedMinHash:
    """An l-buffered k-MinHash sketch"""

    def __init__(self, A: set):
        if not isinstance(A, set):
            raise TypeError("A must be of type 'set'")
        if not A.issubset(U):
            raise ValueError("A is not a subset of the universe U")

        self.A = A
        self.sketch = []

        for i in range(k):
            B_Ai = smallest(H(A, h[i]), l)
            d_Ai = None

            if len(B_Ai) == l:
                d_Ai = max(B_Ai)
            else:
                d_Ai = (math.inf, math.inf)

            self.sketch.append((B_Ai, d_Ai))

    def get_signature(self):
        """
        Get the sketch's k-MinHash signature, a list of k MinHashes computed
        from k hash functions
        """
        signature = []

        for i in range(k):
            signature.append(min(self.sketch[i][0]))

        return signature

    def delete(self, x: int):
        """
        Delete an element x from the sketch.
        """
        if x not in self.A:
            return

        self.A.remove(x)

        for i in range(k):
            B_Ai = self.sketch[i][0]

            if (h[i](x), x) in B_Ai:
                B_Ai.remove((h[i](x), x))

            if len(B_Ai) == 0:
                self.__init__(self.A)

    def insert(self, x: int):
        """
        Inserts an element x into the sketch.
        """
        self.A.add(x)

        for i in range(k):
            B_Ai, d_Ai = self.sketch[i]

            if (h[i](x), x) <= d_Ai:
                B_Ai = smallest(set(B_Ai).union({(h[i](x), x)}), l)

                if len(B_Ai) == l:
                    d_Ai = max(B_Ai)
