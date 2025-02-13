from dataclasses import dataclass

# ToDo comments

@dataclass(init=True)
class IndexBruteForceSearchParam:
    k : int = 0

@dataclass(init=True)
class IndexHnswSearchParam:
    k : int = 0
    ef: int = 0

@dataclass(init=True)
class IndexIvfSearchParam:
    k : int = 0
    nprobe: int = 0
