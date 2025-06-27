class IndexSearchParamBruteForce:
    """Index search param for brute force index. Equal to basic parameters

    #### Attributes:
        k (int): Expected size of KNN index results. Should not be less than 1
        radius (float): In addition to the parameter `k`, the query results can also be filtered by a `rank` -
            value using the parameter, witch called `radius`. It's named so because, under the `L2`-metric,
            it restricts vectors from query result to a sphere of the specified radius

    """

    def __init__(self, k: int = None, radius: float = None):
        if k is None and radius is None:
            raise ValueError("Either 'k' or 'radius' needs to be specified")
        if k is not None and k < 1:
            raise ValueError("KNN limit 'k' should not be less than 1")
        self.k = k
        self.radius = radius


class IndexSearchParamHnsw:
    """Index search param for HNSW index.

    #### Attributes:
        k (int): Expected size of KNN index results. Should not be less than 1
        ef (int): Size of nearest neighbor buffer that will be filled during fetching. Should not be less than 'k',
            good story when `ef` ~= 1.5 * `k`
        radius (float): In addition to the parameter `k`, the query results can also be filtered by a `rank` -
            value using the parameter, witch called `radius`. It's named so because, under the `L2`-metric,
            it restricts vectors from query result to a sphere of the specified radius

    """

    def __init__(self, ef: int, k: int = None, radius: float = None):
        if k is None and radius is None:
            raise ValueError("Either 'k' or 'radius' needs to be specified")
        if k is not None:
            if k < 1:
                raise ValueError("KNN limit 'k' should not be less than 1")
            if ef < k:
                raise ValueError("'ef' should not be less than 'k'")
        self.k = k
        self.radius = radius
        self.ef = ef


class IndexSearchParamIvf:
    """Index search param for IVF index.

    #### Attributes:
        k (int): Expected size of KNN index results. Should not be less than 1
        nprobe (int): Number of centroids that will be scanned in where. Should not be less than 1
        radius (float): In addition to the parameter `k`, the query results can also be filtered by a `rank` -
            value using the parameter, witch called `radius`. It's named so because, under the `L2`-metric,
            it restricts vectors from query result to a sphere of the specified radius

    """

    def __init__(self, nprobe: int, k: int = None, radius: float = None):
        if k is None and radius is None:
            raise ValueError("Either 'k' or 'radius' needs to be specified")
        if k is not None and k < 1:
            raise ValueError("KNN limit 'k' should not be less than 1")
        if nprobe < 1:
            raise ValueError("'nprobe' should not be less than 1")
        self.nprobe = nprobe
        self.k = k
        self.radius = radius
