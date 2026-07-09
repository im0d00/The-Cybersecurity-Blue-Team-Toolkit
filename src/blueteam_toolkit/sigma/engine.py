from pathlib import Path

import yaml


class SigmaRuleError(ValueError):
    pass


def load_sigma_rule(path: str | Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SigmaRuleError("Sigma file must be a mapping")
    required = {"title", "logsource", "detection"}
    missing = sorted(required - data.keys())
    if missing:
        raise SigmaRuleError(f"Missing required keys: {', '.join(missing)}")
    return data


def detect_matches(rule: dict, event: dict) -> bool:
    detection = rule.get("detection", {})
    selection = detection.get("selection", {})
    if not isinstance(selection, dict):
        return False
    return all(str(event.get(key)) == str(value) for key, value in selection.items())


def run_rules(rule_paths: list[str | Path], event: dict) -> list[dict]:
    matches = []
    for path in rule_paths:
        rule = load_sigma_rule(path)
        if detect_matches(rule, event):
            matches.append(
                {
                    "title": rule.get("title"),
                    "level": rule.get("level", "medium"),
                    "id": rule.get("id", "unknown"),
                }
            )
    return matches
