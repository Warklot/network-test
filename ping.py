import subprocess;
import json;
import datetime


def ping(host,count):
    try:
        output = subprocess.check_output(["ping", "-n", str(count), host], text=True)
        host_info = {"host": host}
        host_info["online"] = True  
        host_info["count"] = count
        for line in output.splitlines():
            if "Average =" in line:
                avg_part = line.split("Average =")[-1].replace("ms","").strip()
                host_info["avg_part"] = avg_part
            if "Minimum =" in line:
                min_part = line.split("Minimum =")[-1].split(",")[0].split()[0].replace("ms","")
                host_info["min_part"] = min_part
            if "Maximum =" in line:
                max_part = line.split("Maximum =")[-1].split(",")[0].split()[0].replace("ms","")
                host_info["max_part"] = max_part
        host_info["timestamp"] = datetime.datetime.now().isoformat()
        return host_info
    except:
        host_info = {"host": host}
        host_info["Online"] = False
        host_info["avg_part"] = None
        host_info["min_part"] = None 
        host_info["max_part"] = None  
        host_info["timestamp"] = datetime.datetime.now().isoformat()
        return host_info
        
