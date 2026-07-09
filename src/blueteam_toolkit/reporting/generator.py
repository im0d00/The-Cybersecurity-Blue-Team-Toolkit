import csv
import json
from datetime import UTC, datetime
from pathlib import Path


def generate_report(
    data: dict,
    output_dir: str | Path,
    base_name: str = "report",
) -> dict[str, str]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    json_path = output / f"{base_name}_{timestamp}.json"
    md_path = output / f"{base_name}_{timestamp}.md"
    csv_path = output / f"{base_name}_{timestamp}.csv"
    html_path = output / f"{base_name}_{timestamp}.html"

    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    md_content = [
        f"# {base_name.title()} Report",
        "",
        f"Generated: {timestamp}",
        "",
        "## Findings",
        "",
    ]
    for key, value in data.items():
        md_content.append(f"- **{key}**: `{value}`")
    md_path.write_text("\n".join(md_content), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["field", "value"])
        for key, value in data.items():
            writer.writerow([key, json.dumps(value)])

    html_rows = "".join(
        (
            f"<tr><td>{key}</td>"
            f"<td><pre>{json.dumps(value, indent=2)}</pre></td></tr>"
        )
        for key, value in data.items()
    )
    html_path.write_text(
        (
            "<html><head><title>Blue Team Report</title></head><body>"
            f"<h1>{base_name.title()} Report</h1>"
            f"<table border='1'>{html_rows}</table></body></html>"
        ),
        encoding="utf-8",
    )

    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "csv": str(csv_path),
        "html": str(html_path),
    }
