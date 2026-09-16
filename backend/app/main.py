from __future__ import annotations
from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from .core import RegisterIn, TelemetryIn, new_token, settings
from .db import Base, Device, Incident, Session, Telemetry, Anomaly, engine
from .services import health, process


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize the configured production database when the API starts."""
    Base.metadata.create_all(engine)
    yield


app=FastAPI(title="NetSentinel API",version="0.1.0",lifespan=lifespan); app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_methods=["*"],allow_headers=["*"])
def db():
    s=Session()
    try: yield s
    finally: s.close()
def device_auth(x_device_token: str=Header(), s=Depends(db)):
    d=s.scalar(select(Device).where(Device.token==x_device_token))
    if not d: raise HTTPException(401,"invalid device token")
    return d
@app.get("/api/v1/health")
def app_health(): return {"status":"healthy"}
@app.get("/api/v1/ready")
def ready():
    with engine.connect() as c: c.execute(select(1))
    return {"status":"ready"}
@app.post("/api/v1/devices/register",status_code=201)
def register(body:RegisterIn,s=Depends(db)):
    d=Device(id=str(uuid4()),name=body.name,platform=body.platform,token=new_token()); s.add(d);s.commit();return {"device_id":d.id,"device_token":d.token}
def ingest(record,device,s):
    if s.scalar(select(Telemetry).where(Telemetry.measurement_id==record.measurement_id)): return False
    t=Telemetry(device_id=device.id,**record.model_dump()); s.add(t);s.flush();process(s,t);return True
@app.post("/api/v1/telemetry",status_code=201)
def telemetry(body:TelemetryIn,device=Depends(device_auth),s=Depends(db)):
    created=ingest(body,device,s);s.commit();return {"accepted":created}
@app.post("/api/v1/telemetry/batch",status_code=201)
def batch(records:list[TelemetryIn],device=Depends(device_auth),s=Depends(db)):
    if len(records)>500: raise HTTPException(422,"batch exceeds 500 records")
    accepted=sum(ingest(x,device,s) for x in records);s.commit();return {"accepted":accepted,"duplicates":len(records)-accepted}
@app.get("/api/v1/devices")
def devices(s=Depends(db)): return [{"id":d.id,"name":d.name,"platform":d.platform,"created_at":d.created_at} for d in s.scalars(select(Device)).all()]
@app.get("/api/v1/devices/{device_id}")
def device(device_id:str,s=Depends(db)):
    d=s.get(Device,device_id)
    if not d: raise HTTPException(404,"device not found")
    return {"id":d.id,"name":d.name,"platform":d.platform,"created_at":d.created_at}
@app.get("/api/v1/devices/{device_id}/metrics")
def metrics(device_id:str,limit:int=120,s=Depends(db)):
    rows=s.scalars(select(Telemetry).where(Telemetry.device_id==device_id).order_by(Telemetry.timestamp.desc()).limit(min(limit,1000))).all();return [{"timestamp":x.timestamp,"latency_ms":x.latency_ms,"packet_loss_percent":x.packet_loss_percent,"jitter_ms":x.jitter_ms,"dns_latency_ms":x.dns_latency_ms,"health_score":health(x)} for x in reversed(rows)]
@app.get("/api/v1/devices/{device_id}/health")
def device_health(device_id:str,s=Depends(db)):
    t=s.scalar(select(Telemetry).where(Telemetry.device_id==device_id).order_by(Telemetry.timestamp.desc()))
    if not t: raise HTTPException(404,"no telemetry")
    return {"device_id":device_id,"score":health(t),"timestamp":t.timestamp,"label":"NetSentinel Health Score"}
@app.get("/api/v1/anomalies")
def anomalies(s=Depends(db)): return [{"id":a.id,"device_id":a.device_id,"score":a.score,"reason":a.reason,"created_at":a.created_at} for a in s.scalars(select(Anomaly).order_by(Anomaly.created_at.desc()).limit(100)).all()]
@app.get("/api/v1/incidents")
def incidents(s=Depends(db)): return [{"id":i.id,"device_id":i.device_id,"status":i.status,"classification":i.classification,"confidence":i.confidence,"evidence":i.evidence,"opened_at":i.opened_at} for i in s.scalars(select(Incident).order_by(Incident.opened_at.desc())).all()]
@app.get("/api/v1/incidents/{incident_id}")
def incident(incident_id:int,s=Depends(db)):
    i=s.get(Incident,incident_id)
    if not i: raise HTTPException(404,"incident not found")
    return {"id":i.id,"status":i.status,"classification":i.classification,"confidence":i.confidence,"evidence":i.evidence}
