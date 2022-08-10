"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Enum, Counter
import requests


class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, app_url, app_secret, app_port=80, polling_interval_seconds=5):
        self.app_url = app_url
        self.app_secret = app_secret
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus' metrics to collect
        self.redis_event_handle_worker_1 = Gauge("redis_event_handle_worker_1", "Redis Event worker 1")
        self.redis_event_handle_worker_2 = Gauge("redis_event_handle_worker_2", "Redis Event worker 2")
        self.total_event_process_error = Gauge("total_event_process_error", "Total event logs process error")
        # self.total_uptime = Gauge("app_uptime", "Uptime")
        # self.health = Enum("app_health", "Health", states=["healthy", "unhealthy"])

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Fetch raw status data from the application
        resp = requests.get(url=f"{self.app_url}:{self.app_port}/status?api_key={self.app_secret}")
        status_data = resp.json()

        # Update Prometheus metrics with application metrics
        self.redis_event_handle_worker_1.set(status_data["redis_event_handle_worker_1"])
        self.redis_event_handle_worker_2.set(status_data["redis_event_handle_worker_2"])
        self.total_event_process_error.set(status_data["total_event_process_error"])
        # self.total_uptime.set(status_data["total_uptime"])
        # self.health.state(status_data["health"])


def main():
    """Main entry point"""
    try:
        polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
        app_port = int(os.getenv("APP_PORT", "5000"))
        exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))
        app_url = os.getenv("APP_URL", "http://localhost")
        app_secret = os.getenv("APP_SECRET", "yoursecretkey")
        app_metrics = AppMetrics(
            app_url=app_url,
            app_secret=app_secret,
            app_port=app_port,
            polling_interval_seconds=polling_interval_seconds
        )
        start_http_server(exporter_port)
        app_metrics.run_metrics_loop()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
