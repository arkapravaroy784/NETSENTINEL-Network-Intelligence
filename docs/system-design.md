# System design

Functional requirements are periodic collection, durable upload, validation, analytics, anomalies, explainable incidents, and a dashboard. Non-functional priorities are graceful offline operation, bounded queues, UTC timestamps, input safety, indexed device/time reads, and privacy. Raw retention is intentionally disabled in development; production retention should run as a reviewed scheduled job with a configured period. Long-range queries should be served from hourly/daily summaries when volume warrants it.

Tradeoff: this is a modular monolith with synchronous ingestion processing. It is easy to develop and demo. At higher volume, move aggregation/anomaly jobs to a worker and use PostgreSQL migrations (an Alembic migration directory can be added once deployment schema governance is enabled).
