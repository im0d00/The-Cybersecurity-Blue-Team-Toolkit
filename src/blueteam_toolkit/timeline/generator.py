from datetime import UTC, datetime


def generate_timeline(events: list[dict]) -> list[dict]:
    normalized = []
    for event in events:
        timestamp = event.get("timestamp") or datetime.now(UTC).isoformat()
        normalized.append({"timestamp": timestamp, "event": event})
    return sorted(normalized, key=lambda item: item["timestamp"])
