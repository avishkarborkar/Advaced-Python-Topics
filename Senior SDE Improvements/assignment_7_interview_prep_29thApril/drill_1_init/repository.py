"""
Drill 1 — base class. DO NOT MODIFY.

Repository is a class with:
  - one positional arg (name)
  - two keyword-only args (max_size, readonly) — these can ONLY be passed by name
  - some setup logic in __init__ (creates an internal index dict)
  - a method that depends on the setup having run

This shape mirrors real production base classes: positional + keyword-only,
non-trivial __init__ work, and methods that read from that state.

Your subclasses must forward ALL parent args correctly. Drop one and the
parent is half-initialized — and you'll get cryptic AttributeErrors later.
"""


class Repository:
    def __init__(self, name: str, *, max_size: int = 100, readonly: bool = False):
        self.name = name
        self.max_size = max_size
        self.readonly = readonly
        self._items: dict = {}
        self._index: dict[str, list[int]] = {}  # built lazily by add()

    def add(self, key: str, value):
        if self.readonly:
            raise RuntimeError(f"{self.name} is readonly")
        if len(self._items) >= self.max_size:
            raise RuntimeError(f"{self.name} is full")
        self._items[key] = value
        self._index.setdefault(key[0], []).append(len(self._items))

    def get(self, key: str):
        return self._items.get(key)

    def size(self) -> int:
        return len(self._items)

    def describe(self) -> str:
        mode = "readonly" if self.readonly else "writable"
        return f"{self.name} ({mode}, {self.size()}/{self.max_size})"