from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator
import pandas as pd


class BaseParserStrategy(ABC):
    @abstractmethod
    def parse(self, log_file: Path | str) -> Iterator[pd.DataFrame]:
        """
        Get iterator of DataFrames.
        """
        pass
