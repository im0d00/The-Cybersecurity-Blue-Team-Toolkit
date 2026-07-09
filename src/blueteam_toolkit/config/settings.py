from pathlib import Path

from pydantic import BaseModel, Field


class ToolkitSettings(BaseModel):
    project_name: str = "Cybersecurity Blue Team Toolkit"
    rules_dir: Path = Path("rules")
    reports_dir: Path = Path("reports")
    logs_dir: Path = Path("logs")
    jwt_algorithm: str = "HS256"
    api_rate_limit_per_minute: int = 120
    allow_origins: list[str] = Field(default_factory=lambda: ["*"])


settings = ToolkitSettings()
