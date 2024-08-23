import os
import time
import argparse
import re
from datetime import datetime

def tail_file(filename, lines=20):
    """
    Return the last `lines` lines from the file.
    """
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        buffer_size = 1024
        buffer = bytearray(buffer_size)
        lines_found = []
        position = file_size

        while position >= 0 and len(lines_found) < lines:
            position -= buffer_size
            if position < 0:
                position = 0
            f.seek(position)
            read_bytes = f.readinto(buffer)
            lines_found = buffer[:read_bytes].splitlines()
        
        return [line.decode() for line in lines_found[-lines:]]

def monitor_logs(file_path, patterns, alert_callback=None, poll_interval=1.0):
    """
    Monitor the log file for specific patterns.
    
    file_path: str
        Path to the log file to be monitored.
    patterns: list of str
        List of regex patterns to search for in the log file.
    alert_callback: callable
        A function to call when a pattern is matched.
    poll_interval: float
        How often to check the log file (in seconds).
    """
    last_position = 0

    while True:
        with open(file_path, 'r') as f:
            f.seek(last_position)
            lines = f.readlines()
            last_position = f.tell()

        for line in lines:
            for pattern in patterns:
                if re.search(pattern, line):
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    message = f"[{timestamp}] Pattern '{pattern}' matched: {line.strip()}"
                    print(message)
                    if alert_callback:
                        alert_callback(message)

        time.sleep(poll_interval)

def alert(message):
    """
    Placeholder for an alert system (e.g., send an email or log to a monitoring system).
    """
    print(f"ALERT: {message}")

def main(log_file, patterns, poll_interval, alert_on_match):
    if not os.path.exists(log_file):
        raise FileNotFoundError(f"Log file not found: {log_file}")

    if alert_on_match:
        alert_callback = alert
    else:
        alert_callback = None

    monitor_logs(log_file, patterns, alert_callback, poll_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor log files for specific patterns.")
    parser.add_argument('--log_file', type=str, required=True, help="Path to the log file to monitor.")
    parser.add_argument('--patterns', type=str, nargs='+', required=True, help="List of patterns to search for in the log file.")
    parser.add_argument('--poll_interval', type=float, default=1.0, help="Interval (in seconds) between checks.")
    parser.add_argument('--alert_on_match', action='store_true', help="Trigger an alert when a pattern is matched.")
    
    args = parser.parse_args()
    main(args.log_file, args.patterns, args.poll_interval, args.alert_on_match)
