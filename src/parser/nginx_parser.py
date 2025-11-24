from pathlib import Path
from base_parser_strategy import BaseParserStrategy
import pandas as pd


class NginxParserStrategy(BaseParserStrategy):
    def parse(self, log_file: Path | str) -> pd.DataFrame:
        pass
