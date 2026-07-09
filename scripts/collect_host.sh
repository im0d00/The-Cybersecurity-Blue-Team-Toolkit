#!/usr/bin/env bash
set -euo pipefail
python -m blueteam_toolkit.cli.main host --output reports/host_snapshot.json
