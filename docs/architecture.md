# Architecture

The toolkit uses a modular architecture with separate packages for collectors, detections, enrichment, reporting, automation, and extensibility.

## Layers

1. Collection layer: host, network, and log collectors.
2. Detection layer: IOC, Sigma, YARA, and hunting logic.
3. Enrichment layer: MITRE ATT&CK mapping.
4. Exposure layer: CLI and FastAPI.
5. Output layer: report generation and artifacts.
6. Extensibility layer: plugin SDK and dynamic loader.
