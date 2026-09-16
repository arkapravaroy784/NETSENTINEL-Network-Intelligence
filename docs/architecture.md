# Architecture

`Agent → local SQLite queue → HTTPS FastAPI API → PostgreSQL/SQLite → rules + baseline anomaly processing → incidents → React dashboard`.

The agent sends metadata only: timing, loss, interface state, counters, and local CPU/RAM. It does not inspect packet payloads, credentials, cookies, messages, or browsing history. Failed uploads remain durable in the local queue and are retried with a bounded retry count.

The **NetSentinel Health Score** is a deterministic, project-specific 0–100 heuristic: `100 - latency/3 - loss×2 - jitter - DNS/8 - HTTP/12`, with an extra low-bandwidth penalty. Values are clamped to 0–100. It is not an industry standard.
