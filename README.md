# NetSentinel

Cloud-Based Network Intelligence & Anomaly Detection Platform. NetSentinel collects privacy-conscious network metadata, derives a deterministic **NetSentinel Health Score**, detects deviations from a per-device baseline, and creates explainable, probabilistic incidents. It never attributes a fault to an ISP with certainty.

## Quick start (PowerShell)

```powershell
cd network-intelligence-platform
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt -r agent/requirements.txt
python scripts/seed_demo_data.py
uvicorn backend.app.main:app --reload
# In another shell: cd frontend; npm install; npm run dev
```

Open `http://localhost:8000/docs` or the dashboard at `http://localhost:5173`. The frontend defaults to `http://localhost:8000/api/v1`; copy `frontend/.env.example` to `frontend/.env` and set `VITE_API_URL` when the API runs elsewhere. See [agent/README.md](agent/README.md) for Windows agent registration and execution.

## Docker

`docker compose up --build` starts PostgreSQL, the API, and the dashboard. The API is at port 8000; dashboard at port 5173.

To seed the same PostgreSQL database used by the Docker API, run:

```powershell
docker compose --profile demo run --rm seed
```

Alternatively, from the host, pass the published PostgreSQL URL explicitly:

```powershell
python scripts/seed_demo_data.py --database-url "postgresql+psycopg://netsentinel:netsentinel_dev@localhost:5432/netsentinel"
```

The seed command prints a password-redacted database URL. Do not seed Docker using the default local SQLite configuration.

## Demo, tests, ML

```powershell
python scripts/run_demo_scenario.py --scenario packet_loss
python -m pytest backend/tests agent/tests ml/tests
python -m ml.src.train
```

The ML trainer uses labeled synthetic data only; its reported metrics are generated at execution time and are not claims about production performance. See `docs/` for security, privacy, architecture, cloud cost guidance, and known limitations.
<img width="1228" height="848" alt="image" src="https://github.com/user-attachments/assets/7e75d438-e44f-474f-82ca-a211cf198853" />
