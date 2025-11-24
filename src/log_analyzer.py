import pandas as pd

from src.analyzer_config import AnalyzerConfig


class LogAnalyzer:

    COLUMNS = ["ip", "timestamp_str", "method", "url", "status"]

    def __init__(self, config: AnalyzerConfig):
        self.cfg = config
        self.df = None

        self.cfg.output_dir.mkdir(parents=True, exist_ok=True)

    def load(self):
        print(f"Loading logs from {self.cfg.input_file}...")

        df_raw = pd.read_csv(
            self.cfg.input_file,
            sep="\0",
            header=None,
            names=["log_line"],
            engine="python",
        )

        extracted_data = df_raw["log_line"].str.extract(self.cfg.log_pattern)
        extracted_data.columns = self.COLUMNS

        self.df = extracted_data

        self.__optimize_types()
        self.__filter_spam()

        print(f"Data loaded. Rows: {len(self.df)}")
        return self

    def __optimize_types(self):
        self.df["status"] = pd.to_numeric(self.df["status"], errors="coerce")

        self.df["timestamp"] = pd.to_datetime(
            self.df["timestamp_str"],
            format=self.cfg.time_format,
            errors="coerce",
            utc=True,
        )

        if self.cfg.target_timezone:
            self.df["timestamp"] = self.df["timestamp"].dt.tz_convert(
                self.cfg.target_timezone
            )

        self.df["hour"] = self.df["timestamp"].dt.hour
        self.df["day_name"] = self.df["timestamp"].dt.day_name()

        self.df.drop(columns=["timestamp_str"], inplace=True)

    def __filter_spam(self):
        if self.cfg.ignore_patterns:
            mask = ~self.df["url"].str.contains(self.cfg.ignore_patterns, na=False)
            self.df = self.df[mask].copy()

    def export_report(self, filename: str, data: pd.Series | pd.DataFrame):
        """
        Універсальний метод збереження (DRY).
        Замінює купу блоків with open().
        """
        file_path = self.cfg.output_dir / filename
        # Pandas вміє писати одразу у файл, open() не потрібен
        data.to_csv(file_path)
        print(f"Saved: {filename}")

    def analyze_top_pages(self, limit=20):
        data = self.df.groupby("url")["url"].count().nlargest(limit)
        self.export_report("top_pages.csv", data)

    def analyze_top_ips(self, limit=30):
        data = self.df.groupby("ip")["ip"].count().nlargest(limit)
        self.export_report("top_ips.csv", data)

    def analyze_top_url_ip(self, limit=30):
        data = self.df.groupby(["url", "ip"])["ip"].count().nlargest(limit)
        self.export_report("top_url_ip.csv", data)

    def analyze_traffic_by_hour(self):
        data = self.df.groupby("hour")["hour"].count()
        self.export_report("traffic_by_hour.csv", data)

    def analyze_traffic_by_day(self):
        data = self.df.groupby("day_name")["day_name"].count()
        self.export_report("traffic_by_day.csv", data)

    def analyze_errors(self, limit=50):
        data = (
            self.df[self.df["status"] >= 400]
            .groupby(["url", "status"])["status"]
            .count()
            .nlargest(limit)
        )
        self.export_report("top_errors.csv", data)

    def analyze_unique_visitors(self, limit=50):
        data = self.df.groupby("url")["ip"].nunique().nlargest(limit)
        self.export_report("unique_visitors.csv", data)

    def analyze_bots_ratio(self, limit=20):
        stats = self.df.groupby("url").agg(
            Total_Hits=("url", "count"), Unique_IPs=("ip", "nunique")
        )

        stats["Frequency_Ratio"] = stats["Total_Hits"] / stats["Unique_IPs"]

        suspicious = stats.sort_values("Frequency_Ratio", ascending=False).head(limit)
        self.export_report("suspicious_bots.csv", suspicious)

    def run_all(self):
        """Facade method to run everything."""
        self.analyze_top_pages()
        self.analyze_top_ips()
        self.analyze_top_url_ip()
        self.analyze_traffic_by_hour()
        self.analyze_traffic_by_day()
        self.analyze_errors()
        self.analyze_unique_visitors()
        self.analyze_bots_ratio()
