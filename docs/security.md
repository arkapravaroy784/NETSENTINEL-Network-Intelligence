# Security and privacy

Device tokens are separate secrets from dashboard authentication and are sent using `X-Device-Token`; do not log or commit them. FastAPI/Pydantic validates input and SQLAlchemy parameterizes database access. Production deployments should terminate HTTPS at the load balancer, use a secret manager, configure restrictive CORS, rate-limit ingress, and add user/device ownership before exposing multi-user access.

Data minimization: NetSentinel collects timing and aggregate interface/system counters only. It intentionally excludes packet payloads, passwords, cookies, messages, and browsing content/history.
