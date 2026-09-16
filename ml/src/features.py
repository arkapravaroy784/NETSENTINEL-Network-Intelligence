FEATURES=["latency_ms","packet_loss_percent","jitter_ms","download_mbps","upload_mbps","dns_latency_ms","http_latency_ms","gateway_latency_ms","internet_latency_ms","cpu_percent","memory_percent"]
def rows_to_matrix(rows):
 import numpy as np
 return np.array([[float(r.get(f) or 0) for f in FEATURES] for r in rows])
