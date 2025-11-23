from ping3 import ping
import datetime
import json

def ping_host(host, count):
    host_info = {"host": host, "count": count}
    host_info["timestamp"] = datetime.datetime.now().isoformat()
    latencies_ms = []


    for _ in range(count):
        retries = 2
        latency = None
        for attempt in range(retries):
            latency = ping(host, timeout=2)
            if latency is not None:
                break  # success
        if latency is not None:
            latencies_ms.append(int(latency * 1000))
    if latencies_ms:
        host_info["Online"] = True
        host_info["avg_ms"] = sum(latencies_ms) // len(latencies_ms)
        host_info["min_ms"] = min(latencies_ms)
        host_info["max_ms"] = max(latencies_ms)
    else:
        host_info["Online"] = False
        host_info["avg_ms"] = None
        host_info["min_ms"] = None
        host_info["max_ms"] = None

    return host_info 