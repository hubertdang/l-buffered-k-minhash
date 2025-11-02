import mmh3
import math

N = 100000
U = set(range(N))  # the simulated universe

k = 128
l = 34

# k hash functions that are uniformly at random (UAR)
h = [lambda x, seed=i: mmh3.hash(str(x), seed=seed) for i in range(k)]


def H(A: set, h_i) -> set:
    """Apply a hash function h_i to all elements a of set A"""
    return {(h_i(a), a) for a in A}


def smallest(X: set, r: int) -> list:
    """Return the r smallest elements of X"""
    return sorted(X)[:r]


class VanillaMinHash:
    """A k-MinHash sketch"""

    def __init__(self, A: set):
        self.A = A  # Simulate the current state of A, stored elsewhere
        self.signature = []

        for i in range(k):
            self.signature.append(min(H(A, h[i])))

    def get_signature(self):
        """Get the sketch's k-MinHash signature"""
        return self.signature

    def delete(self, x: int):
        """Delete an element x from the sketch"""
        self.A.remove(x)
        self.__init__(self.A)

    def insert(self, x: int):
        """Insert an element x into the sketch"""
        if not isinstance(x, int):
            raise TypeError("x must be of type 'int'")

        self.A.add(x)

        for i in range(k):
            if (h[i](x), x) < self.signature[i]:
                self.signature[i] = (h[i](x), x)


class BufferedMinHash:
    """An l-buffered k-MinHash sketch"""

    def __init__(self, A: set):
        self.A = A  # Simulate the current state of A, stored elsewhere
        self.SA = []  # l-buffered k-MinHash sketch of A

        for i in range(k):
            B_Ai = smallest(H(A, h[i]), l)  # buffer of <= l tuples (h_i(x), x)
            d_Ai = None  # dynamic threshold >= 0

            if len(B_Ai) == l:
                d_Ai = max(B_Ai)
            else:
                d_Ai = (math.inf, math.inf)

            self.SA.append((B_Ai, d_Ai))

    def get_signature(self):
        """Get the sketch's k-MinHash signature"""
        return [min(B_Ai[0]) for B_Ai in self.SA]

    def delete(self, x: int):
        """Delete an element x from the sketch"""
        self.A.discard(x)  # Simulate the current state of A being updated

        for i in range(k):
            B_Ai = self.SA[i][0]

            if (h[i](x), x) in B_Ai:
                B_Ai.remove((h[i](x), x))

            # "fault" occurs, i.e., a MinHash was deleted & broke the signature
            if len(B_Ai) == 0:
                # Simulate access to current state of A by a recovery query
                self.__init__(self.A)
                return

    def insert(self, x: int):
        """Insert an element x into the sketch"""
        self.A.add(x)  # Simulate the current state of A being updated

        for i in range(k):
            B_Ai, d_Ai = self.SA[i]

            # Don't add (h_i(x), x) to S(A) if it's not one of the smallest
            if (h[i](x), x) <= d_Ai:
                B_Ai.append((h[i](x), x))  # add the new element
                B_Ai = smallest(set(B_Ai), l)  # keep l smallest

                # Recompute threshold if l-buffer is full
                if len(B_Ai) == l:
                    d_Ai = max(B_Ai)

            self.SA[i] = (B_Ai, d_Ai)
