from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(capacity)]
        self.load_factor = 0.66

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: Any) -> bool:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for k, _ in bucket:
            if k == key:
                return True

        return False

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self) -> list:
        return [k for bucket in self.table for k, _ in bucket]

    def values(self) -> list:
        return [v for bucket in self.table for _, v in bucket]

    def items(self) -> list:
        return [(k, v) for bucket in self.table for k, v in bucket]

    def clear(self) -> None:
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for k, v in bucket:
                self[k] = v
