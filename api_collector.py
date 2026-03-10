import requests
import time
from datetime import datetime, UTC
from pathlib import Path

# Log file location
LOG_FILE = "logs/api_logs.txt"

# Public APIs to monitor
APIS = [
    "https://api.github.com",
    "https://api.github.com/users/SurajArmugham",
]


def ensure_log_directory():
    """Ensure logs directory exists."""
    Path("logs").mkdir(exist_ok=True)


def call_api(url):
    """Call API and measure response time."""
    start_time = time.time()

    try:
        response = requests.get(url, timeout=5)
        latency_ms = int((time.time() - start_time) * 1000)
        return response.status_code, latency_ms

    except requests.exceptions.RequestException:
        latency_ms = int((time.time() - start_time) * 1000)
        return "ERROR", latency_ms


def write_log(method, endpoint, status, latency):
    """Write API call details to log file."""
    timestamp = datetime.now(UTC).isoformat()

    log_entry = f"{timestamp} {method} {endpoint} {status} {latency}\n"

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)


def main():
    ensure_log_directory()

    print("Starting API collection...\n")

    for api in APIS:
        status, latency = call_api(api)

        write_log("GET", api, status, latency)

        print(f"Endpoint: {api}")
        print(f"Status: {status}")
        print(f"Latency: {latency} ms\n")


if __name__ == "__main__":
    main()