
SHARD_MAX_KEYS = 10**9

class Shard(dict):
    def __init__(self) -> None:
        pass

    def is_full(self) -> bool:
        return len(self) == SHARD_MAX_KEYS