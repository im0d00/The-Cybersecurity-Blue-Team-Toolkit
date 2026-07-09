from pathlib import Path

SUPPORTED_LOGS = {
    "linux_auth": "/var/log/auth.log",
    "linux_syslog": "/var/log/syslog",
    "apache": "/var/log/apache2/access.log",
    "nginx": "/var/log/nginx/access.log",
}


def collect_logs(max_lines: int = 500) -> dict[str, list[str]]:
    output: dict[str, list[str]] = {}
    for key, path in SUPPORTED_LOGS.items():
        file_path = Path(path)
        if not file_path.exists():
            output[key] = []
            continue
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            lines = handle.readlines()[-max_lines:]
            output[key] = [line.rstrip("\n") for line in lines]
    return output
