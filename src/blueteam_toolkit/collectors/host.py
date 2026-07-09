import os
import platform
import socket
import subprocess
from pathlib import Path

import psutil


def _safe_command(command: list[str]) -> list[str]:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return []
        return [line for line in result.stdout.splitlines() if line.strip()]
    except (FileNotFoundError, subprocess.SubprocessError, TimeoutError):
        return []


def collect_host_information() -> dict:
    users = [u.name for u in psutil.users()]
    network_interfaces = {
        iface: [addr.address for addr in addresses]
        for iface, addresses in psutil.net_if_addrs().items()
    }

    services = []
    for proc in psutil.process_iter(["pid", "name", "username"]):
        info = proc.info
        if info.get("name"):
            services.append(info)
        if len(services) >= 200:
            break

    running_processes = [
        p.info for p in psutil.process_iter(["pid", "name", "username"])
    ][:250]
    open_ports = sorted(
        {
            conn.laddr.port
            for conn in psutil.net_connections(kind="inet")
            if conn.laddr
        },
    )

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_release": platform.release(),
        "kernel": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "environment_variables": dict(list(os.environ.items())[:100]),
        "logged_in_users": users,
        "network_interfaces": network_interfaces,
        "running_processes": running_processes,
        "services_snapshot": services,
        "open_ports": open_ports,
        "firewall_status": {
            "linux_ufw": _safe_command(["ufw", "status"]),
            "windows_netsh": _safe_command(["netsh", "advfirewall", "show", "allprofiles"]),
        },
        "scheduled_tasks": {
            "linux": _safe_command(["crontab", "-l"]),
            "windows": _safe_command(["schtasks", "/query", "/fo", "LIST"]),
        },
        "startup_programs": {
            "linux_systemd": _safe_command(["systemctl", "list-unit-files", "--type=service"]),
            "windows_startup": _safe_command(["wmic", "startup", "get", "caption,command"]),
        },
        "recent_files": _safe_command(["ls", "-lt", str(Path.home())])[:50],
    }
