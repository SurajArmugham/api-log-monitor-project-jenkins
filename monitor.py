from collections import defaultdict

LOG_FILE = "logs/api_logs.txt"


def parse_logs():
    """Read log file and extract monitoring data."""
    total_requests = 0
    endpoint_counts = defaultdict(int)
    error_count = 0
    latencies = []

    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                parts = line.strip().split()

                if len(parts) != 5:
                    continue

                timestamp, method, endpoint, status, latency = parts

                total_requests += 1
                endpoint_counts[endpoint] += 1

                # Track errors
                if status != "ERROR":
                    status_code = int(status)

                    if status_code >= 400:
                        error_count += 1

                else:
                    error_count += 1

                # Track latency
                try:
                    latencies.append(int(latency))
                except ValueError:
                    pass

    except FileNotFoundError:
        print("Log file not found.")
        return None

    return total_requests, endpoint_counts, error_count, latencies


def generate_report():
    data = parse_logs()

    if not data:
        return

    total_requests, endpoint_counts, error_count, latencies = data

    if total_requests == 0:
        print("No log data available.")
        return

    error_rate = (error_count / total_requests) * 100

    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)

    print("\nAPI Monitoring Report")
    print("----------------------")

    print(f"\nTotal Requests: {total_requests}")

    print("\nEndpoint Usage:")
    for endpoint, count in endpoint_counts.items():
        print(f"{endpoint} : {count}")

    print(f"\nError Rate: {error_rate:.2f}%")

    print(f"\nAverage Latency: {avg_latency:.2f} ms")
    print(f"Max Latency: {max_latency} ms")

    check_alerts(error_rate, avg_latency)


def check_alerts(error_rate, avg_latency):
    """Basic alert logic."""

    print("\nAlerts:")

    if error_rate > 5:
        print("WARNING: High API error rate detected")

    if avg_latency > 500:
        print("WARNING: High API latency detected")

    if error_rate <= 5 and avg_latency <= 500:
        print("No alerts triggered")


if __name__ == "__main__":
    generate_report()