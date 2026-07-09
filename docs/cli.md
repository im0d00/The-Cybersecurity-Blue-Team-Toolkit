# CLI Guide

Commands:

- `btk host --output reports/host.json`
- `btk network`
- `btk logs --max-lines 200`
- `btk ioc-scan-text "<text>"`
- `btk ioc-scan-file ./sample_data/sample.log`
- `btk ioc-add domain evil.tld`
- `btk yara-validate rules/yara/suspicious_strings.yar`
- `btk sigma-detect --rule rules/sigma/suspicious_powershell.yml --event-json '{"Image":"powershell.exe","CommandLine":"powershell.exe -enc"}'`
- `btk report sample_data/report_input.json`
