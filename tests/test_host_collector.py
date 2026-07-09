from blueteam_toolkit.collectors.host import collect_host_information


def test_collect_host_information_contains_core_fields():
    result = collect_host_information()
    for key in ("hostname", "os", "architecture", "running_processes", "open_ports"):
        assert key in result
