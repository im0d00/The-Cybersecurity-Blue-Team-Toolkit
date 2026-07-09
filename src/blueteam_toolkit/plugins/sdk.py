from abc import ABC, abstractmethod


class ToolkitPlugin(ABC):
    name: str

    @abstractmethod
    def run(self, payload: dict) -> dict:
        raise NotImplementedError
