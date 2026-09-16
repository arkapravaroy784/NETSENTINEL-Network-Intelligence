from __future__ import annotations
import argparse, asyncio, json, platform, uuid
from datetime import datetime, timezone
import httpx
from .collectors import dns_latency,gateway,http_latency,interface,jitter,ping,system
from .config import Config
from .models import Telemetry
from .storage import Store
def collect(targets: tuple[str, ...] = ("1.1.1.1", "8.8.8.8")):
    """Collect one privacy-preserving host-network measurement."""
    g=gateway(); gl=ping(g) if g else None; samples=[ping(x) for x in targets]; valid=[x for x in samples if x is not None]; name,kind,up,sent,received=interface();cpu,mem=system()
    return Telemetry(measurement_id=str(uuid.uuid4()),timestamp=datetime.now(timezone.utc),latency_ms=sum(valid)/len(valid) if valid else None,internet_latency_ms=sum(valid)/len(valid) if valid else None,gateway_latency_ms=gl,packet_loss_percent=100*(len(samples)-len(valid))/len(samples),jitter_ms=jitter(samples),dns_latency_ms=dns_latency(),http_latency_ms=http_latency(),interface_name=name,interface_type=kind,interface_is_up=up,bytes_sent=sent,bytes_received=received,cpu_percent=cpu,memory_percent=mem)
async def upload(store,cfg):
    rows=store.pending()
    if not rows or not cfg.device_token:return
    try:
      async with httpx.AsyncClient(timeout=8) as c:
       r=await c.post(cfg.api_base_url.rstrip("/")+"/api/v1/telemetry/batch",json=[__import__('json').loads(x[1]) for x in rows],headers={"X-Device-Token":cfg.device_token});r.raise_for_status()
       for id,_ in rows:store.sent(id)
    except httpx.HTTPError:
      for id,_ in rows:store.failed(id)
def main():
 p=argparse.ArgumentParser();p.add_argument("--once",action="store_true");p.add_argument("--register",action="store_true",help="Register this host and print JSON device credentials.");p.add_argument("--name",help="Device name used with --register.");args=p.parse_args();cfg=Config()
 if args.register:
  name=args.name or platform.node()
  with httpx.Client(timeout=8) as client:
   response=client.post(cfg.api_base_url.rstrip("/")+"/api/v1/devices/register",json={"name":name,"platform":platform.system().lower()})
   response.raise_for_status()
  print(json.dumps(response.json()))
  return
 store=Store()
 while True:
  store.add(collect(cfg.targets).model_dump());asyncio.run(upload(store,cfg))
  if args.once:return
  import time;time.sleep(cfg.interval_seconds)
if __name__=="__main__":main()
