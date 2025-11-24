from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import pandas as pd


class BaseParserStrategy(ABC):
    def __init__(self, log_pattern: str, max_chunk_size: Optional[int] = None):
        self.log_pattern = log_pattern
        self.max_chunk_size = max_chunk_size

    @abstractmethod
    def parse(self, log_file: Path | str) -> pd.DataFrame:
        pass
