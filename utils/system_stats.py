import psutil
import pandas as pd
from datetime import datetime

def get_system_stats():
    stats = {
        "timestamp": datetime.now(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "net_sent": psutil.net_io_counters().bytes_sent / (1024 * 1024),  # in MB
        "net_recv": psutil.net_io_counters().bytes_recv / (1024 * 1024)
    }
    return pd.DataFrame([stats])
