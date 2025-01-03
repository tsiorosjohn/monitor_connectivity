import os
import time
import datetime
import subprocess
import platform

# Configuration
CHECK_INTERVAL = 1  # Time in seconds between checks
MONITOR_DURATION = 3600  # Monitoring duration in seconds (1 hour)
LOG_FILE = "internet_connectivity_log.txt"
PING_HOST = "8.8.8.8"  # Host to ping (Google DNS)


def ping_host(host=PING_HOST):
    """
    Pings a host and returns the latency in milliseconds.
    If ping fails, returns None.
    """
    try:
        # Platform-specific ping command
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", host]
        else:  # macOS and Linux
            cmd = ["ping", "-c", "1", host]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Extract latency from the ping output
            output = result.stdout
            if platform.system().lower() == "windows":
                latency = output.split("Average = ")[-1].split("ms")[0].strip()
            else:
                latency = output.split("time=")[-1].split(" ms")[0].strip()
            return float(latency)
        else:
            return None
    except Exception as e:
        return None


def log_status(status, latency=None):
    """
    Logs the connectivity status with latency and timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latency_info = f"Latency: {latency} ms" if latency is not None else "Latency: N/A"
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} - {'Online' if status else 'Offline'} - {latency_info}\n")
    print(f"{timestamp} - {'Online' if status else 'Offline'} - {latency_info}")


def monitor_connectivity():
    """
    Monitors internet connectivity and logs latency for a specified duration.
    """
    start_time = time.time()
    while time.time() - start_time < MONITOR_DURATION:
        latency = ping_host()
        status = latency is not None
        log_status(status, latency)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)  # Clear previous log if it exists
    print("Starting internet connectivity monitor...")
    monitor_connectivity()
    print(f"Monitoring completed. Log saved to {LOG_FILE}.")
