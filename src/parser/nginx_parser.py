from pathlib import Path
from typing import Iterator
import pandas as pd
from .base_parser_strategy import BaseParserStrategy
from ..config import general as cfg
from ..config import nginx as cfn


class NginxParserStrategy(BaseParserStrategy):
    def __init__(self):
        self._log_pattern = cfn.LOG_PATTERN
        self._max_chunk_size = cfg.MAX_CHUNK_SIZE

    def parse(self, log_file: Path | str) -> Iterator[pd.DataFrame]:
        """Parse log file and return iterator"""
        log_file = Path(log_file)
        batch = []

        with log_file.open("r", encoding="utf-8") as f:
            for line in f:
                match = self._log_pattern.match(line)
                if match:
                    batch.append(match.groupdict())

                if len(batch) >= self._max_chunk_size:
                    yield self._process_batch(batch)
                    batch = []

            if batch:
                yield self._process_batch(batch)

    def _process_batch(self, data: list[dict]) -> pd.DataFrame:
        """Helper method for optimization DataFrame"""
        df = pd.DataFrame(data)

        if "status" in df.columns:
            df["status"] = (
                pd.to_numeric(df["status"], errors="coerce").fillna(0).astype(int)
            )
        if "size" in df.columns:
            df["size"] = (
                pd.to_numeric(df["size"], errors="coerce").fillna(0).astype(int)
            )

        if "time" in df.columns:
            df["time"] = pd.to_datetime(
                df["time"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce"
            )

        return df
