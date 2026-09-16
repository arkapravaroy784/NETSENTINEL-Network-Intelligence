"""Seed the configured NetSentinel development database with synthetic data."""
import argparse
import os
import sys,uuid,random
from datetime import datetime,timezone,timedelta
from pathlib import Path
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--database-url",
    help="SQLAlchemy URL to seed. Defaults to DATABASE_URL or local SQLite.",
)
parser.add_argument("--records", type=int, default=80, help="Number of synthetic records to create.")
args = parser.parse_args()
if args.database_url:
    os.environ["DATABASE_URL"] = args.database_url

ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from app.db import Base,engine,Session,Device
from app.core import TelemetryIn,new_token
from app.main import ingest
Base.metadata.create_all(engine);s=Session();d=s.query(Device).first() or Device(id=str(uuid.uuid4()),name='Demo Wi-Fi device (synthetic)',platform='demo',token=new_token());s.add(d);s.commit()
for i in range(args.records):
 bad=i>args.records*0.75; t=TelemetryIn(measurement_id=str(uuid.uuid4()),timestamp=datetime.now(timezone.utc)-timedelta(minutes=args.records-i),latency_ms=random.uniform(25,45) if not bad else random.uniform(160,260),internet_latency_ms=random.uniform(25,45) if not bad else random.uniform(160,260),gateway_latency_ms=random.uniform(3,12),packet_loss_percent=random.uniform(0,2) if not bad else random.uniform(12,30),jitter_ms=random.uniform(1,7),dns_latency_ms=random.uniform(15,55),http_latency_ms=random.uniform(60,140),download_mbps=80,cpu_percent=25,memory_percent=48,interface_type='Wi-Fi')
 ingest(t,d,s)
s.commit();print(f'Seeded {args.records} synthetic telemetry records for {d.name}. Database: {engine.url.render_as_string(hide_password=True)}')
