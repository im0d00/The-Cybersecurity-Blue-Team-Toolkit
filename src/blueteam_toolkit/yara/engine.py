from pathlib import Path


def validate_rule(rule_text: str) -> bool:
    return all(keyword in rule_text for keyword in ("rule", "strings", "condition"))


def validate_rule_file(path: str | Path) -> dict:
    rule_path = Path(path)
    text = rule_path.read_text(encoding="utf-8", errors="ignore")
    return {
        "file": str(rule_path),
        "valid": validate_rule(text),
    }


def lightweight_scan(path: str | Path, indicators: list[str]) -> dict:
    target = Path(path)
    content = target.read_text(encoding="utf-8", errors="ignore")
    matches = [indicator for indicator in indicators if indicator in content]
    return {
        "target": str(target),
        "match_count": len(matches),
        "matches": matches,
    }
