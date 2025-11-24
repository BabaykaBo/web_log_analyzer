from pathlib import Path

from src.analyzer_config import AnalyzerConfig
from src.log_analyzer import LogAnalyzer
import config


config = AnalyzerConfig(
    input_file=Path(config.input_file),
    output_dir=Path(config.output_dir),
    log_pattern=config.log_pattern,
    time_format=config.time_format,
    ignore_patterns=config.ignore_patterns,
)

# Виконання
analyzer = LogAnalyzer(config)
analyzer.load().run_all()
