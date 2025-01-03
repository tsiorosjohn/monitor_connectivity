import matplotlib.pyplot as plt
import datetime
import re
import argparse


def parse_log(file_path):
    """
    Parses the log file and extracts timestamps, hosts, statuses, latencies, and packet losses.
    Returns a dictionary keyed by host, each containing a list of (timestamp, status, latency, packet_loss) tuples.
    """
    log_data = {}
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"(.*) - (.*) - (Online|Offline) - Latency: (\S+) ms - Packet Loss: (\S+)%", line)
            if match:
                timestamp = datetime.datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                host = match.group(2)
                status = match.group(3) == "Online"
                latency = None if match.group(4) == "N/A" else float(match.group(4))
                packet_loss = None if match.group(5) == "N/A" else float(match.group(5))

                if host not in log_data:
                    log_data[host] = []
                log_data[host].append((timestamp, status, latency, packet_loss))
    return log_data


def plot_latency_and_packet_loss(log_data):
    """
    Plots latency and packet loss for all monitored hosts.
    """
    plt.figure(figsize=(12, 8))

    for host, data in log_data.items():
        timestamps = [entry[0] for entry in data if entry[2] is not None]
        latencies = [entry[2] for entry in data if entry[2] is not None]
        packet_losses = [entry[3] for entry in data if entry[3] is not None]
        offline_timestamps = [entry[0] for entry in data if not entry[1]]

        # Plot latency
        plt.plot(timestamps, latencies, label=f"{host} (Latency)", marker="o", color="blue", linewidth=1)

        # Plot packet loss as a secondary axis
        plt.scatter(timestamps, packet_losses, label=f"{host} (Packet Loss)", color="green", marker="x", zorder=5)

        # Plot offline periods
        plt.scatter(offline_timestamps, [0] * len(offline_timestamps), label=f"{host} (Offline)", color="red", marker="x")

    plt.title("Internet Latency, Packet Loss, and Offline Periods")
    plt.xlabel("Time")
    plt.ylabel("Latency (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("latency_and_packet_loss_plot.png")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Internet Connectivity Log Analyzer")
    parser.add_argument("--log-file", type=str, default="internet_connectivity_log.txt", help="Path to the log file (default: internet_connectivity_log.txt)")

    args = parser.parse_args()

    log_data = parse_log(args.log_file)
    if not log_data:
        print("No data found in the log file.")
    else:
        plot_latency_and_packet_loss(log_data)
        print("Latency and packet loss plot saved as 'latency_and_packet_loss_plot.png'.")
