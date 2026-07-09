from blueteam_toolkit.mitre.mapping import map_detection_to_mitre

DETECTION_PATTERNS = {
    "encoded_powershell": ["-enc", "FromBase64String"],
    "credential_dumping": ["sekurlsa", "lsass"],
    "scheduled_task_persistence": ["schtasks", "create"],
    "smb_lateral_movement": ["\\\\", "ADMIN$"],
}


def hunt_text(text: str) -> list[dict]:
    findings = []
    lower = text.lower()
    for name, indicators in DETECTION_PATTERNS.items():
        if all(indicator.lower() in lower for indicator in indicators):
            finding = {"detection": name, "mitre": map_detection_to_mitre(name)}
            findings.append(finding)
    return findings
