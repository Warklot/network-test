from ping3 import ping
import datetime


class HostPinger:
    def __init__(self, host: str, count: int):
        self.host = host
        self.count = count
        self.timestamp = None
        self.latencies_ms = []
        self.online = False
        self.avg_ms = None
        self.min_ms = None
        self.max_ms = None

    def ping(self):
        self.timestamp = datetime.datetime.now().isoformat()
        self.latencies_ms = []
        for _ in range(self.count): 
            retries = 2
            latency = None
            for _ in range (retries): 
                latency = ping(self.host, timeout=2)
                if latency:
                    break
            if latency:
                self.latencies_ms.append(int(latency*1000))

        if self.latencies_ms:
            self.online = True
            self.avg_ms = sum(self.latencies_ms)// len(self.latencies_ms)
            self.min_ms = min(self.latencies_ms)
            self.max_ms = max(self.latencies_ms)
        else:
            self.online = False
            self.avg_ms = None
            self.min_ms = None
            self.max_ms = None
    

    def get_info(self):
        return{
            "host": self.host,
            "count": self.count,
            "timestamp": self.timestamp,
            "Online": self.online,
            "avg_ms": self.avg_ms,
            "min_ms": self.min_ms,
            "max_ms": self.max_ms
        }

