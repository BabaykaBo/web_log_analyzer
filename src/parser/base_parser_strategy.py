from abc import ABC, abstractmethod
from pathlib import Path


class BaseParserStrategy(ABC):
    @abstractmethod
    def parse(self, log_file: Path | str):
        pass
