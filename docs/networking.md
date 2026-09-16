# Networking and diagnosis

ICMP latency is round-trip time; loss is failed probes divided by probes; jitter is the mean absolute difference between consecutive successful latency samples. Gateway probes help distinguish local-path symptoms from remote-path symptoms. DNS checks measure resolver response time; HTTP checks should be lightweight and infrequent; throughput tests belong on a much longer interval.

Diagnosis is evidence-based and probabilistic. High gateway and internet latency suggests a possible LAN/router or Wi-Fi issue. Normal gateway with degraded internet suggests possible upstream degradation. Slow DNS with normal ping suggests DNS degradation. These rules cannot verify ISP responsibility. ICMP and traceroute may be blocked or deprioritized.
