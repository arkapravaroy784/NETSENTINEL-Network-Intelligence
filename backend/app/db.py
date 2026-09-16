from __future__ import annotations
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from .core import settings, utcnow
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {})
Session = sessionmaker(bind=engine, expire_on_commit=False)
class Base(DeclarativeBase): pass
class Device(Base):
    __tablename__="devices"
    id: Mapped[str]=mapped_column(String(48),primary_key=True)
    name: Mapped[str]=mapped_column(String(120)); platform: Mapped[str]=mapped_column(String(50)); token: Mapped[str]=mapped_column(String(128),unique=True)
    created_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow)
class User(Base):
    __tablename__="users"; id: Mapped[int]=mapped_column(primary_key=True); email: Mapped[str]=mapped_column(String(254),unique=True); created_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow)
class DeviceToken(Base):
    __tablename__="device_tokens"; id: Mapped[int]=mapped_column(primary_key=True); device_id: Mapped[str]=mapped_column(ForeignKey("devices.id"),index=True); token_hint: Mapped[str]=mapped_column(String(12)); created_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow)
class Telemetry(Base):
    __tablename__="telemetry"; __table_args__=(Index("ix_telemetry_device_timestamp","device_id","timestamp"),)
    id: Mapped[int]=mapped_column(primary_key=True); measurement_id: Mapped[str]=mapped_column(String(100),unique=True)
    device_id: Mapped[str]=mapped_column(ForeignKey("devices.id"),index=True); timestamp: Mapped[object]=mapped_column(DateTime(timezone=True),index=True)
    latency_ms: Mapped[float|None]=mapped_column(Float); packet_loss_percent: Mapped[float|None]=mapped_column(Float); jitter_ms: Mapped[float|None]=mapped_column(Float)
    download_mbps: Mapped[float|None]=mapped_column(Float); upload_mbps: Mapped[float|None]=mapped_column(Float); dns_latency_ms: Mapped[float|None]=mapped_column(Float); http_latency_ms: Mapped[float|None]=mapped_column(Float); gateway_latency_ms: Mapped[float|None]=mapped_column(Float); internet_latency_ms: Mapped[float|None]=mapped_column(Float)
    interface_name: Mapped[str|None]=mapped_column(String(128)); interface_type: Mapped[str|None]=mapped_column(String(32)); interface_is_up: Mapped[bool|None]=mapped_column(Boolean)
    bytes_sent: Mapped[int|None]=mapped_column(Integer); bytes_received: Mapped[int|None]=mapped_column(Integer); cpu_percent: Mapped[float|None]=mapped_column(Float); memory_percent: Mapped[float|None]=mapped_column(Float); test_status: Mapped[str]=mapped_column(String(24)); error_code: Mapped[str|None]=mapped_column(String(80)); error_message: Mapped[str|None]=mapped_column(String(500))
class Anomaly(Base):
    __tablename__="anomalies"; id: Mapped[int]=mapped_column(primary_key=True); device_id: Mapped[str]=mapped_column(index=True); telemetry_id: Mapped[int]=mapped_column(); score: Mapped[float]=mapped_column(Float); reason: Mapped[str]=mapped_column(Text); created_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow,index=True)
class Incident(Base):
    __tablename__="incidents"; id: Mapped[int]=mapped_column(primary_key=True); device_id: Mapped[str]=mapped_column(index=True); status: Mapped[str]=mapped_column(String(20),default="OPEN",index=True); classification: Mapped[str]=mapped_column(String(64)); confidence: Mapped[float]=mapped_column(Float); evidence: Mapped[str]=mapped_column(Text); opened_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow); resolved_at: Mapped[object|None]=mapped_column(DateTime(timezone=True),nullable=True)
class Prediction(Base):
    __tablename__="predictions"; id: Mapped[int]=mapped_column(primary_key=True); telemetry_id: Mapped[int]=mapped_column(index=True); label: Mapped[str]=mapped_column(String(64)); confidence: Mapped[float]=mapped_column(Float); created_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow)
class Alert(Base):
    __tablename__="alerts"; id: Mapped[int]=mapped_column(primary_key=True); incident_id: Mapped[int]=mapped_column(index=True); status: Mapped[str]=mapped_column(String(20),default="PENDING"); channel: Mapped[str]=mapped_column(String(32),default="webhook"); created_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow)
class ModelVersion(Base):
    __tablename__="model_versions"; id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(100)); version: Mapped[str]=mapped_column(String(64)); metadata_json: Mapped[str]=mapped_column(Text); created_at: Mapped[object]=mapped_column(DateTime(timezone=True),default=utcnow)
