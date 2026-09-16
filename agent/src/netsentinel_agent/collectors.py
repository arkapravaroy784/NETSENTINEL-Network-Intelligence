from __future__ import annotations
import platform, re, socket, subprocess, time, urllib.request
from statistics import mean
import psutil
def ping(host:str,timeout:float=2)->float|None:
    flag="-n" if platform.system()=="Windows" else "-c"; timeout_flag="-w" if platform.system()=="Windows" else "-W"
    try:
        out=subprocess.run(["ping",flag,"1",timeout_flag,str(int(timeout*1000) if platform.system()=="Windows" else int(timeout)),host],capture_output=True,text=True,timeout=timeout+2).stdout
        m=re.search(r"(?:time[=<]|Average = )(\d+(?:\.\d+)?)\s*ms",out,re.I); return float(m.group(1)) if m else None
    except (OSError,subprocess.TimeoutExpired): return None
def gateway()->str|None:
    try:
        if platform.system()=="Windows":
            out=subprocess.run(["route","print","0.0.0.0"],capture_output=True,text=True,timeout=3).stdout
            m=re.search(r"^\s*0\.0\.0\.0\s+0\.0\.0\.0\s+(\S+)",out,re.M);return m.group(1) if m else None
        out=subprocess.run(["ip","route","show","default"],capture_output=True,text=True,timeout=3).stdout;m=re.search(r"via\s+(\S+)",out);return m.group(1) if m else None
    except (OSError,subprocess.TimeoutExpired): return None
def interface():
    stats=psutil.net_if_stats(); counters=psutil.net_io_counters(); active=next(((n,s) for n,s in stats.items() if s.isup and not n.lower().startswith(("lo","loopback"))),None)
    if not active:return None,"Unknown",False,counters.bytes_sent,counters.bytes_recv
    name,s=active; low=name.lower(); kind="Wi-Fi" if any(x in low for x in ("wi-fi","wifi","wlan","wireless")) else "Ethernet" if any(x in low for x in ("eth","ethernet","en")) else "Unknown"
    return name,kind,s.isup,counters.bytes_sent,counters.bytes_recv
def system(): return psutil.cpu_percent(interval=None),psutil.virtual_memory().percent
def dns_latency(domain: str="example.com") -> float|None:
    """Measure system-resolver latency without collecting browsing content."""
    start=time.perf_counter()
    try: socket.getaddrinfo(domain,443); return round((time.perf_counter()-start)*1000,2)
    except socket.gaierror: return None
def http_latency(url: str="https://www.example.com/") -> float|None:
    """Perform a bounded, lightweight HEAD-style connectivity probe."""
    start=time.perf_counter()
    try:
        req=urllib.request.Request(url,method="HEAD",headers={"User-Agent":"NetSentinel/0.1"})
        with urllib.request.urlopen(req,timeout=5): pass
        return round((time.perf_counter()-start)*1000,2)
    except (OSError,ValueError): return None
def jitter(samples:list[float|None])->float|None:
    valid=[x for x in samples if x is not None]
    return mean(abs(b-a) for a,b in zip(valid,valid[1:])) if len(valid)>=2 else None
