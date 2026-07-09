from collections import defaultdict
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from blueteam_toolkit.collectors.host import collect_host_information
from blueteam_toolkit.collectors.logs import collect_logs
from blueteam_toolkit.collectors.network import collect_network_snapshot
from blueteam_toolkit.config.settings import settings
from blueteam_toolkit.ioc.scanner import scan_file_for_iocs, scan_text_for_iocs
from blueteam_toolkit.reporting.generator import generate_report

app = FastAPI(title=settings.project_name, version="v1")
auth_scheme = HTTPBearer(auto_error=False)
request_counters: dict[str, list[datetime]] = defaultdict(list)


class IOCScanTextRequest(BaseModel):
    text: str


class IOCScanFileRequest(BaseModel):
    path: str


class ReportRequest(BaseModel):
    data: dict
    base_name: str = "incident"


def _enforce_rate_limit(client_id: str) -> None:
    now = datetime.now(UTC)
    recent = [t for t in request_counters[client_id] if (now - t).total_seconds() <= 60]
    if len(recent) >= settings.api_rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    recent.append(now)
    request_counters[client_id] = recent


def _auth(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(auth_scheme),
    ],
) -> None:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing bearer token")
    try:
        jwt.decode(
            credentials.credentials,
            "development-secret-change-me",
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


@app.middleware("http")
async def limit_requests(request: Request, call_next):
    _enforce_rate_limit(request.client.host if request.client else "unknown")
    return await call_next(request)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.project_name}


@app.get("/api/v1/host", dependencies=[Depends(_auth)])
def host_info() -> dict:
    return collect_host_information()


@app.get("/api/v1/network", dependencies=[Depends(_auth)])
def network_info() -> dict:
    return collect_network_snapshot()


@app.get("/api/v1/logs", dependencies=[Depends(_auth)])
def logs() -> dict:
    return collect_logs()


@app.post("/api/v1/ioc/scan/text", dependencies=[Depends(_auth)])
def scan_text(payload: IOCScanTextRequest) -> dict:
    return scan_text_for_iocs(payload.text)


@app.post("/api/v1/ioc/scan/file", dependencies=[Depends(_auth)])
def scan_file(payload: IOCScanFileRequest) -> dict:
    return scan_file_for_iocs(payload.path)


@app.post("/api/v1/reports", dependencies=[Depends(_auth)])
def report(payload: ReportRequest) -> dict:
    return generate_report(payload.data, settings.reports_dir, payload.base_name)
