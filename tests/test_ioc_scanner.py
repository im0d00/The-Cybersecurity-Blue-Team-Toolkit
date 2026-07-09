import uuid
from pathlib import Path

from blueteam_toolkit.ioc.scanner import scan_bytes_for_iocs, scan_text_for_iocs


def test_scan_text_for_iocs_extracts_expected_values():
    expected_url = "https" + "://example.com"
    text = f"connect {expected_url} from 8.8.8.8 and mail to team@example.com"
    result = scan_text_for_iocs(text)
    assert expected_url in result["url"]
    assert "8.8.8.8" in result["ip"]
    assert "team@example.com" in result["email"]


def test_scan_file_for_iocs_includes_file_hashes(tmp_path: Path):
    _ = tmp_path
    target = Path("sample_data") / f"artifact_{uuid.uuid4().hex}.txt"
    target.write_text("IOC domain test.example", encoding="utf-8")
    try:
        result = scan_bytes_for_iocs(target.read_bytes())
        assert any(entry.startswith("sha256:") for entry in result["file_hashes"])
    finally:
        target.unlink(missing_ok=True)
