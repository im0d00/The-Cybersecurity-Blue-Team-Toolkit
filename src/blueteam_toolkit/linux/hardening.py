def linux_hardening_recommendations() -> list[str]:
    return [
        "Disable root SSH login and enforce multi-factor authentication.",
        "Use nftables/iptables default-deny firewall policy with explicit allow rules.",
        "Enable auditd and persistent journald retention for forensic quality logs.",
        "Apply least privilege file permissions and remove world-writable service paths.",
        "Enable kernel hardening sysctl settings and keep packages patched.",
    ]
