from pathlib import Path

from blueteam_toolkit.ioc.scanner import scan_file_for_iocs, scan_text_for_iocs


def test_scan_text_for_iocs_extracts_expected_values():
    text = "connect https://example.com from 8.8.8.8 and mail to team@example.com"
    result = scan_text_for_iocs(text)
    assert "https://example.com" in result["url"]
    assert "8.8.8.8" in result["ip"]
    assert "team@example.com" in result["email"]


def test_scan_file_for_iocs_includes_file_hashes(tmp_path: Path):
    target = tmp_path / "artifact.txt"
    target.write_text("IOC domain test.example", encoding="utf-8")
    result = scan_file_for_iocs(target)
    assert any(entry.startswith("sha256:") for entry in result["file_hashes"])
