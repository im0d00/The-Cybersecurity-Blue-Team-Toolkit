rule SuspiciousPowerShellStrings {
    meta:
        author = "Blue Team"
        description = "Detects common encoded PowerShell techniques"
    strings:
        $s1 = "FromBase64String" nocase
        $s2 = "IEX(" nocase
        $s3 = "-enc" nocase
    condition:
        any of them
}
