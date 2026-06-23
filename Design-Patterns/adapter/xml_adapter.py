from typing import Any
from bs4 import BeautifulSoup

class XMLConfig:

    def __init__(self, bs: BeautifulSoup) -> None:
        self.bs = bs

    def get(self, key: str ,default: Any = None) -> Any | None:
        # Implementation to retrieve value from XML structure
        value = self.bs.find(key)
        if not value:
            return default
        return value.text
        