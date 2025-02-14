
# ToDo comments

class IndexSearchParamBase:

    def __init__(self, k: int):
        self.k : int = k

class IndexSearchParamBruteForce(IndexSearchParamBase):

    def __init__(self, k: int):
        super().__init__(k)

class IndexSearchParamHnsw(IndexSearchParamBase):

    def __init__(self, k: int, ef: int):
        super().__init__(k)
        self.ef: int = ef

class IndexSearchParamIvf(IndexSearchParamBase):

    def __init__(self, k: int, nprobe: int):
        super().__init__(k)
        self.nprobe: int = nprobe
