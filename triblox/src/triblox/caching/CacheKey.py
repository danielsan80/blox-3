import sys

sys.path.append("../../src/")

import hashlib
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CacheKey:
    parts: Tuple[str, ...] = ()

    def add(self, part: str | Tuple[str]) -> "Cache":
        if isinstance(part, tuple):
            return CacheKey(self.parts + part)
        elif isinstance(part, str):
            return CacheKey(self.parts + (part,))
        else:
            raise TypeError("Part must be a string or a tuple of strings")

    def __str__(self) -> str:
        return "_".join(self.parts)

    def hash(self) -> str:
        return hashlib.sha256(str(self).encode()).hexdigest()
