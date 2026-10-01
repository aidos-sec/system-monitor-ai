"""Сбор системных метрик через psutil."""
import time
import psutil
import asyncio

def collect_metrics() -> dict:
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    return {
        "timestamp": time.time(),
        "cpu": cpu,
        "mem": mem.percent,
        "disk": disk.percent,
        "net_sent": net.bytes_sent,
        "net_recv": net.bytes_recv,
    }

async def metrics_stream(interval: float = 1.0):
    while True:
        yield collect_metrics()
        await asyncio.sleep(interval)
