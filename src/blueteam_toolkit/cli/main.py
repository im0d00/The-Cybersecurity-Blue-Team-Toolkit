import json
from pathlib import Path
from typing import Annotated

import typer
from rich import print

from blueteam_toolkit.collectors.host import collect_host_information
from blueteam_toolkit.collectors.logs import collect_logs
from blueteam_toolkit.collectors.network import collect_network_snapshot
from blueteam_toolkit.ioc.manager import IOCRepository
from blueteam_toolkit.ioc.scanner import scan_bytes_for_iocs, scan_text_for_iocs
from blueteam_toolkit.reporting.generator import generate_report
from blueteam_toolkit.sigma.engine import run_rules
from blueteam_toolkit.yara.engine import lightweight_scan, validate_rule_file

app = typer.Typer(add_completion=False, help="Cybersecurity Blue Team Toolkit CLI")


@app.command()
def host(output: str | None = None) -> None:
    data = collect_host_information()
    if output:
        Path(output).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(data)


@app.command()
def network(output: str | None = None) -> None:
    data = collect_network_snapshot()
    if output:
        Path(output).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(data)


@app.command()
def logs(max_lines: int = 200) -> None:
    print(collect_logs(max_lines=max_lines))


@app.command()
def ioc_scan_text(text: str) -> None:
    print(scan_text_for_iocs(text))


@app.command()
def ioc_scan_file(path: str) -> None:
    print(scan_bytes_for_iocs(Path(path).read_bytes()))


@app.command()
def ioc_add(
    ioc_type: str,
    value: str,
    source: str = "manual",
    db: str = "rules/ioc/iocs.json",
) -> None:
    repository = IOCRepository(db)
    print(repository.add(ioc_type, value, source))


@app.command()
def yara_validate(rule_path: str) -> None:
    print(validate_rule_file(rule_path))


@app.command()
def yara_scan(
    path: str,
    indicator: Annotated[list[str] | None, typer.Option("--indicator")] = None,
) -> None:
    print(lightweight_scan(path, indicator or []))


@app.command()
def sigma_detect(rule: list[str], event_json: str) -> None:
    event = json.loads(event_json)
    print(run_rules(rule, event))


@app.command()
def report(input_json: str, base_name: str = "incident") -> None:
    data = json.loads(Path(input_json).read_text(encoding="utf-8"))
    outputs = generate_report(data, base_name)
    print(outputs)
