from datetime import datetime
from pydantic import BaseModel, Field
class Telemetry(BaseModel):
    measurement_id:str; timestamp:datetime
    latency_ms:float|None=Field(None,ge=0); packet_loss_percent:float|None=Field(None,ge=0,le=100); jitter_ms:float|None=Field(None,ge=0)
    dns_latency_ms:float|None=None; http_latency_ms:float|None=None; gateway_latency_ms:float|None=None; internet_latency_ms:float|None=None
    download_mbps:float|None=None; upload_mbps:float|None=None; interface_name:str|None=None; interface_type:str|None=None; interface_is_up:bool|None=None
    bytes_sent:int|None=None; bytes_received:int|None=None; cpu_percent:float|None=None; memory_percent:float|None=None; test_status:str="OK"; error_code:str|None=None; error_message:str|None=None
