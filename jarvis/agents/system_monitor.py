"""
System Monitor Agent
Runs every 60 seconds, logs CPU/RAM spikes.
"""
import platform


def monitor_system() -> str:
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        alerts = []
        if cpu > 85:
            alerts.append(f"HIGH CPU: {cpu}%")
        if mem > 90:
            alerts.append(f"HIGH RAM: {mem}%")
        if alerts:
            return "⚠️ " + " | ".join(alerts)
        return f"OK — CPU:{cpu}% RAM:{mem}%"
    except ImportError:
        return f"psutil not installed (pip install psutil) — OS: {platform.system()}"


AGENTS = [
    {
        "name": "system_monitor",
        "description": "Monitors CPU and RAM every 60 seconds and alerts on high usage.",
        "interval": 60,
        "enabled": True,
        "func": monitor_system,
    }
]
