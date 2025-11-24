input_file: str = "data/access.log"
output_dir: str = "dist"
log_pattern: str = (
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?\[(.*?)\]\s"(GET|POST|PUT|PATCH|HEAD|DELETE) (\S+).*?"\s(\d{3})'
)
time_format: str = "%d/%b/%Y:%H:%M:%S %z"
ignore_patterns: str = "admin/|li_op="
target_timezone: str = "Europe/Kyiv"
