from __future__ import annotations
import os, secrets
from datetime import datetime, timezone
from typing import Annotated
from fastapi import Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

def utcnow() -> datetime: return datetime.now(timezone.utc)

class Settings:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./netsentinel.db")
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
settings = Settings()

class TelemetryIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    measurement_id: str = Field(min_length=8, max_length=100)
    timestamp: datetime
    latency_ms: float | None = Field(default=None, ge=0, le=120000)
    packet_loss_percent: float | None = Field(default=None, ge=0, le=100)
    jitter_ms: float | None = Field(default=None, ge=0, le=120000)
    download_mbps: float | None = Field(default=None, ge=0, le=100000)
    upload_mbps: float | None = Field(default=None, ge=0, le=100000)
    dns_latency_ms: float | None = Field(default=None, ge=0, le=120000)
    http_latency_ms: float | None = Field(default=None, ge=0, le=120000)
    gateway_latency_ms: float | None = Field(default=None, ge=0, le=120000)
    internet_latency_ms: float | None = Field(default=None, ge=0, le=120000)
    interface_name: str | None = Field(default=None, max_length=128)
    interface_type: str | None = Field(default=None, max_length=32)
    interface_is_up: bool | None = None
    bytes_sent: int | None = Field(default=None, ge=0)
    bytes_received: int | None = Field(default=None, ge=0)
    cpu_percent: float | None = Field(default=None, ge=0, le=100)
    memory_percent: float | None = Field(default=None, ge=0, le=100)
    test_status: str = Field(default="OK", max_length=24)
    error_code: str | None = Field(default=None, max_length=80)
    error_message: str | None = Field(default=None, max_length=500)
    @field_validator("timestamp")
    @classmethod
    def aware(cls, value):
        if value.tzinfo is None: raise ValueError("timestamp must be timezone-aware UTC")
        return value.astimezone(timezone.utc)

class RegisterIn(BaseModel):
    name: str = Field(min_length=1,max_length=120)
    platform: str = Field(default="unknown", max_length=50)

def new_token() -> str: return secrets.token_urlsafe(32)
