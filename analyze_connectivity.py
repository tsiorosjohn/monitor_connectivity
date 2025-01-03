import matplotlib.pyplot as plt
import datetime
import argparse
import os


def analyze_log(log_file):
    """
    Analyzes the log file and extracts latency, packet loss, and offline status.
    """
    times = []
    latencies = []
    packet_losses = []
    offline_times = []

    with open(log_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(" - ")
            if len(parts) >= 5:
                timestamp = parts[0].strip()
                host = parts[1].strip()
                status = parts[2].strip()
                latency_info = parts[3].strip()
                packet_loss_info = parts[4].strip()

                # Parse timestamp
                time_entry = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

                # Parse latency
                latency = None
                if "Latency" in latency_info:
                    try:
                        latency = float(latency_info.split(":")[1].split("ms")[0].strip())
                    except ValueError:
                        latency = None

                # Parse packet loss
                packet_loss = None
                if "Packet Loss" in packet_loss_info:
                    try:
                        packet_loss = float(packet_loss_info.split(":")[1].strip().replace("%", ""))
                    except ValueError:
                        packet_loss = None

                # Append to lists
                times.append(time_entry)
                latencies.append(latency)
                packet_losses.append(packet_loss)

                # Record offline times
                if status == "Offline":
                    offline_times.append(time_entry)

    return times, latencies, packet_losses, offline_times


def plot_latency(times, latencies, packet_losses, offline_times):
    """
    Plots latency and packet loss, with offline periods highlighted.
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot latency on the primary y-axis
    ax1.plot(times, latencies, 'bo-', label="Latency (ms)")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Latency (ms)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Highlight offline periods
    offline_label_added = False  # Ensure "Offline" is labeled only once
    for offline_time in offline_times:
        if not offline_label_added:
            ax1.axvline(x=offline_time, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label="Offline")
            offline_label_added = True
        else:
            ax1.axvline(x=offline_time, color='red', linestyle='--', linewidth=1.5, alpha=0.8)

    # Plot packet loss on the secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(times, packet_losses, 'go-', label="Packet Loss (%)")
    ax2.set_ylabel("Packet Loss (%)", color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Combine legends from both axes
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

    # Add title and layout adjustments
    plt.title("Network Latency and Packet Loss Over Time")
    fig.tight_layout()

    # Save and show the plot
    plt.savefig("latency_and_packet_loss_plot.png")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Analyze Internet Connectivity Log")
    parser.add_argument("--log-file", type=str, default="internet_connectivity_log.txt", help="Path to the log file (default: internet_connectivity_log.txt)")
    args = parser.parse_args()

    if not os.path.exists(args.log_file):
        print(f"Log file {args.log_file} does not exist.")
        return

    times, latencies, packet_losses, offline_times = analyze_log(args.log_file)

    # Display summary
    print(f"Log Analysis Summary for {args.log_file}:")
    print(f"Total entries: {len(times)}")
    print(f"Offline periods: {len(offline_times)}")
    # Filter out None values for latency and packet loss
    filtered_latencies = [lat for lat in latencies if lat is not None]
    filtered_packet_losses = [loss for loss in packet_losses if loss is not None]

    # Calculate and display max values
    print(f"Max latency: {max(filtered_latencies) if filtered_latencies else 'N/A'} ms")
    print(f"Max packet loss: {max(filtered_packet_losses) if filtered_packet_losses else 'N/A'}%")

    # Plot data
    plot_latency(times, latencies, packet_losses, offline_times)
    print("Latency and packet loss plot saved as 'latency_and_packet_loss_plot.png'.")


if __name__ == "__main__":
    main()
