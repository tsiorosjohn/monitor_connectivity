import matplotlib.pyplot as plt
import datetime
import re

LOG_FILE = "internet_connectivity_log.txt"


def parse_log(file_path):
    """
    Parses the log file and extracts timestamps, statuses, and latencies.
    Returns a list of tuples: (timestamp, status, latency).
    """
    log_data = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"(.*) - (Online|Offline) - Latency: (\S+)", line)
            if match:
                timestamp = datetime.datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                status = match.group(2) == "Online"
                latency = None if match.group(3) == "N/A" else float(match.group(3))
                log_data.append((timestamp, status, latency))
    return log_data


def generate_summary(log_data):
    """
    Generates a summary of the connectivity log.
    """
    total_checks = len(log_data)
    online_checks = sum(1 for _, status, _ in log_data if status)
    offline_checks = total_checks - online_checks
    average_latency = (
            sum(latency for _, status, latency in log_data if status and latency is not None)
            / max(online_checks, 1)
    )

    summary = {
        "Total Checks": total_checks,
        "Online Checks": online_checks,
        "Offline Checks": offline_checks,
        "Uptime Percentage": (online_checks / total_checks) * 100 if total_checks > 0 else 0,
        "Average Latency (ms)": average_latency,
    }
    return summary


def plot_latency(log_data):
    """
    Plots latency over time.
    """
    timestamps = [timestamp for timestamp, status, latency in log_data if latency is not None]
    latencies = [latency for _, status, latency in log_data if latency is not None]

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, latencies, marker="o", label="Latency (ms)")
    plt.title("Internet Latency Over Time")
    plt.xlabel("Time")
    plt.ylabel("Latency (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("latency_plot.png")
    plt.show()


def main():
    log_data = parse_log(LOG_FILE)
    if not log_data:
        print("No data found in the log file.")
        return

    # Generate and display summary
    summary = generate_summary(log_data)
    print("Internet Connectivity Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Generate latency plot
    plot_latency(log_data)
    print("Latency plot saved as 'latency_plot.png'.")


if __name__ == "__main__":
    main()
