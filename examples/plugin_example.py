from blueteam_toolkit.plugins.sdk import ToolkitPlugin


class EchoPlugin(ToolkitPlugin):
    name = "echo"

    def run(self, payload: dict) -> dict:
        return {"plugin": self.name, "payload": payload}
