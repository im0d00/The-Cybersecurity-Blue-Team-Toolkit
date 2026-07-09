# Cybersecurity Blue Team Toolkit

Enterprise-grade, open-source defensive security toolkit for SOC analysts, DFIR teams, and blue team engineers.

## Features

- Host telemetry collection (processes, users, startup, ports, firewall/task snapshots)
- Network telemetry collection and suspicious external connection detection
- IOC scanning for hashes, IPs, domains, URLs, and email artifacts
- Sigma rule loading and event matching
- YARA rule validation and lightweight content scanning
- MITRE ATT&CK mapping for selected detections
- Incident report generation in JSON/Markdown/CSV/HTML
- FastAPI service with JWT auth and rate limiting
- Cross-platform CLI for operational workflows
- Plugin SDK and plugin loader
- Advanced malware analysis pipeline (static, strings, behavioral, IOC, MITRE, reporting)

## Repository Layout

- `src/blueteam_toolkit/` - Python modules (API, CLI, collectors, detections, reporting)
- `rules/` - Sigma, YARA, and IOC content
- `scripts/` - Bash and PowerShell operational scripts
- `docker/` - Container image resources
- `.github/workflows/` - CI automation
- `tests/` - Unit and API tests

## Quickstart

```bash
python -m pip install -e .[dev]
ruff check .
pytest
```

Run CLI:

```bash
btk host
btk ioc-scan-text "powershell -enc aQBlAHgA"
btk malware-analyze sample_data/report_input.json
```

Run API:

```bash
uvicorn blueteam_toolkit.api.main:app --reload
```

Generate JWT for development:

```python
from jose import jwt
print(jwt.encode({"sub":"soc"}, "development-secret-change-me", algorithm="HS256"))
```

## API Security

- Use an `Authorization` header with a valid bearer JWT for `/api/v1/*` routes.
- `/health` remains unauthenticated for liveness probes.

## Docker

```bash
docker compose up --build
```

## Documentation

- [Architecture](docs/architecture.md)
- [API Guide](docs/api.md)
- [CLI Guide](docs/cli.md)
- [Threat Hunting Guide](docs/threat-hunting.md)
- [Plugin Guide](docs/plugins.md)
- [Malware Analysis Guide](docs/malware-analysis-guide.md)
