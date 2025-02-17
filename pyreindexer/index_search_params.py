from dataclasses import dataclass


@dataclass
class IndexSearchParamBase:
    k: int


@dataclass
class IndexSearchParamBruteForce(IndexSearchParamBase):
    pass


@dataclass
class IndexSearchParamHnsw(IndexSearchParamBase):
    ef: int


@dataclass
class IndexSearchParamIvf(IndexSearchParamBase):
    nprobe: int
