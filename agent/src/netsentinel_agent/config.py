from dataclasses import dataclass
import os
@dataclass
class Config:
    api_base_url:str=os.getenv("API_BASE_URL","http://localhost:8000")
    device_id:str=os.getenv("DEVICE_ID","")
    device_token:str=os.getenv("DEVICE_TOKEN","")
    interval_seconds:int=int(os.getenv("INTERVAL_SECONDS","10"))
    targets:tuple[str,...]=tuple(os.getenv("INTERNET_TARGETS","1.1.1.1,8.8.8.8").split(","))
