import hashlib
import ipaddress
import re
from pathlib import Path

IOC_PATTERNS = {
    "md5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "sha1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "sha256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "domain": re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"),
    "url": re.compile(r"https?://[^\s\"'<>]+"),
}


def hash_file(file_path: Path) -> dict[str, str]:
    data = file_path.read_bytes()
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _extract_ips(text: str) -> list[str]:
    ips = []
    for token in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text):
        try:
            ipaddress.ip_address(token)
            ips.append(token)
        except ValueError:
            continue
    return ips


def scan_text_for_iocs(text: str) -> dict[str, list[str]]:
    results = {kind: sorted(set(pattern.findall(text))) for kind, pattern in IOC_PATTERNS.items()}
    results["ip"] = sorted(set(_extract_ips(text)))
    return results


def scan_file_for_iocs(file_path: str | Path) -> dict[str, list[str]]:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    iocs = scan_text_for_iocs(text)
    hashes = hash_file(path)
    iocs["file_hashes"] = [f"{algo}:{value}" for algo, value in hashes.items()]
    return iocs
