import mmh3

N = 100000
U = set(range(N))  # the simulated universe

k = 128

# k hash functions that are uniformly at random (UAR)
h = [lambda x, seed=i: mmh3.hash(str(x), seed=seed) for i in range(k)]


def H(A: set, h_i) -> list:
    """Apply a hash function h_i to all elements a of set A"""
    return [h_i(a) for a in A]


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
