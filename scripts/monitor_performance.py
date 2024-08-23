import os
import psutil
import time
import argparse
from datetime import datetime

def log_performance_metrics(output_file):
    """
    Logs system performance metrics to a specified file.
    """
    with open(output_file, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()

        log_entry = (
            f"{timestamp}, "
            f"CPU: {cpu_usage}%, "
            f"Memory: {memory_info.percent}%, "
            f"Disk: {disk_usage.percent}%, "
            f"Net Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB, "
            f"Net Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB\n"
        )

        f.write(log_entry)
        print(log_entry.strip())

def check_thresholds(cpu_threshold, memory_threshold, disk_threshold, alert_callback=None):
    """
    Checks if system performance metrics exceed specified thresholds and triggers an alert if they do.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    if cpu_usage > cpu_threshold:
        message = f"ALERT: CPU usage is {cpu_usage}% which exceeds the threshold of {cpu_threshold}%"
        print(message)
        if alert_callback:
            alert_callback(message)
    
    if memory_usage > memory_threshold:
        message = f"ALERT: Memory usage is {memory_usage}% which exceeds the threshold of {memory_threshold}%"
        print(message)
        if alert_callback:
            alert_callback(message)

    if disk_usage > disk_threshold:
        message = f"ALERT: Disk usage is {disk_usage}% which exceeds the threshold of {disk_threshold}%"
        print(message)
        if alert_callback:
            alert_callback(message)

def alert(message):
    """
    Placeholder function for sending alerts (e.g., email, SMS, logging to an external system).
    """
    print(f"ALERT: {message}")

def monitor_system(interval, output_file, cpu_threshold, memory_threshold, disk_threshold, alert_on_threshold):
    """
    Continuously monitors system performance metrics at specified intervals.
    """
    while True:
        log_performance_metrics(output_file)
        
        if alert_on_threshold:
            check_thresholds(cpu_threshold, memory_threshold, disk_threshold, alert_callback=alert)
        
        time.sleep(interval)

def main(interval, output_file, cpu_threshold, memory_threshold, disk_threshold, alert_on_threshold):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Start monitoring system performance
    monitor_system(interval, output_file, cpu_threshold, memory_threshold, disk_threshold, alert_on_threshold)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor system performance metrics.")
    parser.add_argument('--interval', type=int, default=5, help="Interval (in seconds) between each performance check.")
    parser.add_argument('--output_file', type=str, required=True, help="File to log the performance metrics.")
    parser.add_argument('--cpu_threshold', type=float, default=80.0, help="CPU usage threshold for alerts (in percent).")
    parser.add_argument('--memory_threshold', type=float, default=80.0, help="Memory usage threshold for alerts (in percent).")
    parser.add_argument('--disk_threshold', type=float, default=90.0, help="Disk usage threshold for alerts (in percent).")
    parser.add_argument('--alert_on_threshold', action='store_true', help="Enable alerts when thresholds are exceeded.")
    
    args = parser.parse_args()
    main(args.interval, args.output_file, args.cpu_threshold, args.memory_threshold, args.disk_threshold, args.alert_on_threshold)
