# NetSentinel Windows agent

The agent is a host process, not a Docker container. It sends telemetry to the API URL in `API_BASE_URL` and uses a device token in `DEVICE_TOKEN`. Register once, keep the returned token private, then set the variables in the process that runs the agent.

```powershell
cd network-intelligence-platform
.\.venv\Scripts\Activate.ps1
pip install -e .\agent
$env:API_BASE_URL = "http://localhost:8000"
$registration = python -m netsentinel_agent.main --register --name $env:COMPUTERNAME | ConvertFrom-Json
$env:DEVICE_ID = $registration.device_id
$env:DEVICE_TOKEN = $registration.device_token
python -m netsentinel_agent.main --once
```

Omit `--once` for continuous collection; use `Ctrl+C` to stop. The queue database is `netsentinel-agent.db` in the current directory. It preserves `PENDING`, `FAILED`, and `UPLOADED` records; failed batch uploads are retried on subsequent collection cycles up to five times. The current collector uses `INTERVAL_SECONDS` (default `10`) and `INTERNET_TARGETS` (default `1.1.1.1,8.8.8.8`).
