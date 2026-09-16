from fastapi.testclient import TestClient


def test_register_and_ingest(client: TestClient) -> None:
    response = client.post("/api/v1/devices/register", json={"name": "test", "platform": "windows"})
    assert response.status_code == 201
    token = response.json()["device_token"]
    data = {"measurement_id": "test-measurement-0001", "timestamp": "2026-01-01T00:00:00Z", "latency_ms": 40, "packet_loss_percent": 0}
    assert client.post("/api/v1/telemetry", headers={"X-Device-Token": token}, json=data).status_code == 201
    assert client.post("/api/v1/telemetry", headers={"X-Device-Token": token}, json=data).json()["accepted"] is False


def test_rejects_invalid_telemetry(client: TestClient) -> None:
    response = client.post("/api/v1/devices/register", json={"name": "bad", "platform": "x"})
    assert response.status_code == 201
    invalid = {"measurement_id": "x" * 8, "timestamp": "2026-01-01T00:00:00Z", "packet_loss_percent": 101}
    assert client.post("/api/v1/telemetry", headers={"X-Device-Token": response.json()["device_token"]}, json=invalid).status_code == 422
