# API Guide

## Endpoints

- `GET /health`
- `GET /api/v1/host`
- `GET /api/v1/network`
- `GET /api/v1/logs`
- `POST /api/v1/ioc/scan/text`
- `POST /api/v1/ioc/scan/file` (expects JSON with `content_base64`)
- `POST /api/v1/reports`

All `/api/v1/*` endpoints require bearer JWT.
