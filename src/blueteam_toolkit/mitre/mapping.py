from dataclasses import dataclass


@dataclass(frozen=True)
class TechniqueMapping:
    technique_id: str
    technique_name: str
    tactic: str


_DETECTION_TO_MITRE = {
    "encoded_powershell": TechniqueMapping("T1059.001", "PowerShell", "Execution"),
    "credential_dumping": TechniqueMapping("T1003", "OS Credential Dumping", "Credential Access"),
    "scheduled_task_persistence": TechniqueMapping("T1053", "Scheduled Task/Job", "Persistence"),
    "smb_lateral_movement": TechniqueMapping(
        "T1021.002",
        "SMB/Windows Admin Shares",
        "Lateral Movement",
    ),
}


def map_detection_to_mitre(detection_name: str) -> dict | None:
    mapping = _DETECTION_TO_MITRE.get(detection_name)
    if not mapping:
        return None
    return {
        "technique_id": mapping.technique_id,
        "technique_name": mapping.technique_name,
        "tactic": mapping.tactic,
    }
