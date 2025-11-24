from dataclasses import dataclass
from pathlib import Path


@dataclass
class AnalyzerConfig:
    input_file: Path
    output_dir: Path
    log_pattern: str
    time_format: str
    ignore_patterns: str
    target_timezone: str = "UTC"
