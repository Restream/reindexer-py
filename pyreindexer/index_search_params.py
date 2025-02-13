
# ToDo comments

class IndexBruteForceSearchParam:

    def __init__(self, k: int):
        self.k : int = k

class IndexHnswSearchParam:

    def __init__(self, k: int, ef: int):
        self.k : int = k
        self.ef: int = ef

class IndexIvfSearchParam:

    def __init__(self, k: int, nprobe: int):
        self.k : int = k
        self.nprobe: int = nprobe
