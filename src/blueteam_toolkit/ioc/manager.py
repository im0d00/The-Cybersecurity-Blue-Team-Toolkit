import json
from pathlib import Path


class IOCRepository:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def load(self) -> list[dict]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def add(self, ioc_type: str, value: str, source: str = "manual") -> dict:
        records = self.load()
        item = {"type": ioc_type, "value": value, "source": source}
        if item not in records:
            records.append(item)
            self.path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        return item

    def find(self, value: str) -> list[dict]:
        return [record for record in self.load() if record["value"] == value]
