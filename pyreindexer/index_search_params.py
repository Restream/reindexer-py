class IndexSearchParamBruteForce:
    """Index search param for brute force index. Equal to basic parameters

    #### Attributes:
        k (int): should not be less than 1

    """

    def __init__(self, k: int):
        if k < 1:
            raise ValueError("KNN limit 'k' should not be less than 1")
        self.k = k


class IndexSearchParamHnsw:
    """Index search param for HNSW index.

    #### Attributes:
        k (int): should not be less than 1
        ef (int): should not be less than 'k'

    """

    def __init__(self, k: int, ef: int):
        if k < 1:
            raise ValueError("KNN limit 'k' should not be less than 1")
        if ef < k:
            raise ValueError("'ef' should not be less than 'k'")
        self.k = k
        self.ef = ef


class IndexSearchParamIvf:
    """Index search param for HNSW index.

    #### Attributes:
        k (int): should not be less than 1
        nprobe (int): should not be less than 1

    """

    def __init__(self, k: int, nprobe: int):
        if k < 1:
            raise ValueError("KNN limit 'k' should not be less than 1")
        if nprobe < 1:
            raise ValueError("'nprobe' should not be less than 1")
        self.k = k
        self.nprobe = nprobe
