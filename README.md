# Internet Connectivity Monitor and Analyzer

This project includes two scripts to monitor and analyze internet connectivity:

1. **Monitoring Script (`monitor_connectivity.py`)**: Monitors internet connectivity, logs status, latency, and packet loss for multiple hosts.
2. **Analysis Script (`analyze_connectivity.py`)**: Analyzes the connectivity log, generates a latency and packet loss plot, and highlights offline periods.

---

## Features
- Monitor multiple hosts (e.g., `8.8.8.8`, `1.1.1.1`) simultaneously.
- Customizable monitoring interval and duration.
- Logs connectivity status (online/offline), latency, and packet loss.
- Generates latency and packet loss plots with offline periods visually marked.

---

## Requirements
- Python 3.x
- Required libraries:
  - `matplotlib`

Install dependencies using:
```bash
pip install -r requirements.txt
```

## CLI Execution Examples
### Monitoring Connectivity
- Monitor default hosts (8.8.8.8 and 1.1.1.1) for 1 hour:
  ```bash
    python monitor_connectivity.py
    ```
  This will monitor the connectivity of 8.8.8.8 and 1.1.1.1 for 1 hour (3600 seconds) and log results to the default log file internet_connectivity_log.txt.

- Monitor a custom host (1.1.1.1) every 5 seconds for 2 minutes, saving to custom_log.txt:
  ```bash
  python monitor_connectivity.py --hosts 1.1.1.1 --interval 5 --duration 120 --log-file custom_log.txt
  ```
  This will monitor 1.1.1.1 every 5 seconds for 2 minutes and save the output to custom_log.txt.

- Monitor multiple hosts (8.8.8.8, 1.1.1.1, and google.com) every 10 seconds for 5 minutes:
  ```bash
  python monitor_connectivity.py --hosts 8.8.8.8 1.1.1.1 google.com --interval 10 --duration 300
  ```
  This monitors 8.8.8.8, 1.1.1.1, and google.com every 10 seconds for 5 minutes.

## Analyzing Connectivity Logs
- Analyze the default log file (internet_connectivity_log.txt):
  ```bash
  python analyze_connectivity.py
  ```
  This will analyze the internet_connectivity_log.txt file, and display a summary along with a latency and packet loss plot (latency_and_packet_loss_plot.png).

- Analyze a custom log file (custom_log.txt):
  ```bash
  python analyze_connectivity.py --log-file custom_log.txt
  ```
  This will analyze the custom_log.txt log file and generate a plot based on the recorded latency and packet loss.

### Example Log Output
The log file (internet_connectivity_log.txt) will include:
  ```bash
  2025-01-04 10:00:00 - 8.8.8.8 - Online - Latency: 20.3 ms - Packet Loss: 0%
  2025-01-04 10:00:00 - 1.1.1.1 - Offline - Latency: N/A - Packet Loss: N/A
  ```

### Example Latency and Packet Loss Plot
The generated plot (latency_and_packet_loss_plot.png) will show:

Blue markers: Latency over time.
Green line: Packet loss percentage over time.
Red "x" markers: Offline periods.
This plot helps visualize both latency fluctuations and packet loss events, alongside the offline periods.