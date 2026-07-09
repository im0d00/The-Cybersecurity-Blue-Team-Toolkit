def windows_hardening_recommendations() -> list[str]:
    return [
        "Enable Microsoft Defender real-time protection and cloud-delivered protection.",
        "Enforce Windows Firewall on domain, private, and public profiles.",
        "Require Credential Guard and LSASS protection where hardware supports it.",
        "Disable SMBv1 and restrict remote administration interfaces.",
        "Constrain PowerShell with script block logging and constrained language mode.",
    ]
