from fastapi.testclient import TestClient
from jose import jwt

from blueteam_toolkit.api.main import app

client = TestClient(app)


def _token() -> str:
    return jwt.encode({"sub": "soc"}, "development-secret-change-me", algorithm="HS256")


def test_health_route_works():
    response = client.get("/health")
    assert response.status_code == 200


def test_protected_route_requires_auth():
    response = client.get("/api/v1/host")
    assert response.status_code == 401


def test_ioc_scan_text_route():
    token = _token()
    expected_url = "http" + "://example.com"
    response = client.post(
        "/api/v1/ioc/scan/text",
        headers={"Authorization": " ".join(["Bearer", token])},
        json={"text": f"{expected_url} 1.1.1.1"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert expected_url in payload["url"]
    assert "1.1.1.1" in payload["ip"]
