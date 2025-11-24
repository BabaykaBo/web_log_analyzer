import re

LOG_PATTERN = re.compile(
    r"(?P<ip>\S+)\s+"
    r"\S+\s+"
    r"\S+\s+"
    r"\[(?P<time>[^\]]+)\]\s+"
    r'"(?P<request>[^"]+)"\s+'
    r"(?P<status>\d+)\s+"
    r"(?P<size>\S+)\s+"
    r'"(?P<referrer>[^"]*)"\s+'
    r'"(?P<user_agent>[^"]*)"'
)
