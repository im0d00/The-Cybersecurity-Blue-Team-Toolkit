import ipaddress
import socket
from collections import Counter
from datetime import UTC, datetime

import psutil


def _is_private(ip: str) -> bool:
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False


def collect_network_snapshot() -> dict:
    connections = []
    remote_ips = Counter()

    for conn in psutil.net_connections(kind="inet"):
        remote = conn.raddr.ip if conn.raddr else None
        local = conn.laddr.ip if conn.laddr else None
        entry = {
            "status": conn.status,
            "pid": conn.pid,
            "local_ip": local,
            "local_port": conn.laddr.port if conn.laddr else None,
            "remote_ip": remote,
            "remote_port": conn.raddr.port if conn.raddr else None,
            "suspicious": bool(remote and not _is_private(remote)),
        }
        connections.append(entry)
        if remote:
            remote_ips[remote] += 1

    top_remote = [{"ip": ip, "count": count} for ip, count in remote_ips.most_common(20)]

    return {
        "captured_at": datetime.now(UTC).isoformat(),
        "host": socket.gethostname(),
        "interfaces": psutil.net_if_stats(),
        "connections": connections,
        "top_remote_ips": top_remote,
        "suspicious_connections": [c for c in connections if c["suspicious"]],
        "io_counters": psutil.net_io_counters()._asdict(),
    }
