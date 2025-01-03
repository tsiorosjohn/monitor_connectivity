import os
import time
import datetime
import subprocess
import platform
import argparse


def ping_host(host):
    """
    Pings a host and returns the latency in milliseconds and packet loss percentage.
    If ping fails, returns None for both latency and packet loss.
    """
    try:
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", host]
        else:  # macOS and Linux
            cmd = ["ping", "-c", "1", host]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout
            if platform.system().lower() == "windows":
                latency = output.split("Average = ")[-1].split("ms")[0].strip()
                packet_loss = 0  # No packet loss if ping is successful on Windows
            else:
                latency = output.split("time=")[-1].split(" ms")[0].strip()
                packet_loss = output.split("packet loss")[0].split(",")[-2].strip().split()[0]  # Get packet loss percentage
            return float(latency), float(packet_loss)  # Return both latency and packet loss
        else:
            return None, None  # Return None for both if ping fails
    except Exception:
        return None, None


def log_status(log_file, timestamp, host, status, latency=None, packet_loss=None):
    """
    Logs the connectivity status with latency, packet loss, and timestamp.
    """
    latency_info = f"Latency: {latency} ms" if latency is not None else "Latency: N/A"
    packet_loss_info = f"Packet Loss: {packet_loss}%" if packet_loss is not None else "Packet Loss: N/A"
    with open(log_file, "a") as log_file:
        log_file.write(f"{timestamp} - {host} - {'Online' if status else 'Offline'} - {latency_info} - {packet_loss_info}\n")


def monitor_connectivity(log_file, hosts, interval, duration):
    """
    Monitors internet connectivity for the specified hosts and logs results.
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        for host in hosts:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            latency, packet_loss = ping_host(host)
            status = latency is not None
            log_status(log_file, timestamp, host, status, latency, packet_loss)
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Internet Connectivity Monitor")
    parser.add_argument("--hosts", nargs="+", default=["8.8.8.8", "1.1.1.1"], help="List of hosts to monitor (default: Google and Cloudflare DNS)")
    parser.add_argument("--interval", type=int, default=10, help="Interval between checks in seconds (default: 10)")
    parser.add_argument("--duration", type=int, default=3600, help="Monitoring duration in seconds (default: 1 hour)")
    parser.add_argument("--log-file", type=str, default="internet_connectivity_log.txt", help="Path to the log file (default: internet_connectivity_log.txt)")

    args = parser.parse_args()
    if os.path.exists(args.log_file):
        os.remove(args.log_file)  # Clear previous log if it exists

    print(f"Starting monitoring for hosts: {', '.join(args.hosts)}")
    monitor_connectivity(args.log_file, args.hosts, args.interval, args.duration)
    print(f"Monitoring completed. Log saved to {args.log_file}.")
