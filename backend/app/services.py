from __future__ import annotations
from statistics import median
from sqlalchemy import select
from .db import Telemetry, Anomaly, Incident
def health(t):
    penalties = [(t.latency_ms or 0)/3, (t.packet_loss_percent or 0)*2, (t.jitter_ms or 0), (t.dns_latency_ms or 0)/8, (t.http_latency_ms or 0)/12]
    if t.download_mbps is not None and t.download_mbps < 5: penalties.append((5-t.download_mbps)*3)
    return round(max(0,min(100,100-sum(penalties))),1)
def diagnose(t):
    if (t.packet_loss_percent or 0)>=70: return "INTERNET_OUTAGE", .82, ["Severe packet loss was measured."]
    if (t.dns_latency_ms or 0)>250 and (t.latency_ms or 0)<100: return "DNS_DEGRADATION", .74, ["DNS was slow while endpoint latency was normal."]
    if (t.gateway_latency_ms or 0)>80 and (t.internet_latency_ms or 0)>120: return "LAN_OR_ROUTER", .70, ["Gateway and internet latency rose together."]
    if (t.gateway_latency_ms or 0)<40 and (t.internet_latency_ms or 0)>150: return "UPSTREAM_DEGRADATION", .67, ["Gateway was normal while internet latency increased."]
    if (t.cpu_percent or 0)>85 and (t.download_mbps or 0)>30: return "BANDWIDTH_SATURATION", .61, ["Local CPU and throughput were high."]
    return "UNKNOWN", .35, ["No deterministic rule matched this measurement."]
def process(session,t):
    recent=session.scalars(select(Telemetry).where(Telemetry.device_id==t.device_id).order_by(Telemetry.timestamp.desc()).limit(30)).all()
    vals=[x.latency_ms for x in recent if x.latency_ms is not None]
    baseline=median(vals) if len(vals)>=5 else None
    anomalous=(t.packet_loss_percent or 0)>=10 or (baseline is not None and (t.latency_ms or 0)>max(100,baseline*2)) or (t.dns_latency_ms or 0)>300
    if not anomalous: return None
    kind, confidence, evidence=diagnose(t); evidence.append("This is a heuristic assessment, not proof of external responsibility.")
    a=Anomaly(device_id=t.device_id,telemetry_id=t.id,score=round(min(1,(t.packet_loss_percent or 0)/100+(t.latency_ms or 0)/1000),3),reason=kind); session.add(a)
    open_incident=session.scalar(select(Incident).where(Incident.device_id==t.device_id,Incident.status=="OPEN"))
    if not open_incident: session.add(Incident(device_id=t.device_id,classification=kind,confidence=confidence,evidence=" ".join(evidence)))
    return a
