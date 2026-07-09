from pathlib import Path

from blueteam_toolkit.sigma.engine import run_rules


def test_sigma_rule_match(tmp_path: Path):
    rule = tmp_path / "rule.yml"
    rule.write_text(
        """
title: Test Rule
logsource:
  product: windows
detection:
  selection:
    Image: powershell.exe
    CommandLine: powershell.exe -enc
""",
        encoding="utf-8",
    )
    event = {"Image": "powershell.exe", "CommandLine": "powershell.exe -enc"}
    result = run_rules([rule], event)
    assert result and result[0]["title"] == "Test Rule"
