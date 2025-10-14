import mmh3

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
        for i in range(k):
            hx = h[i](x)
            if hx < self.signature[i]:
                self.signature[i] = hx
