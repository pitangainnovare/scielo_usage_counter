from scielo_usage_counter import log_handler


MMDB_PATH = 'tests/fixtures/map.mmdb'


def setup_function():
    log_handler._CLIENT_CACHE.clear()


class CountingRobotPattern:
    def __init__(self):
        self.calls = 0

    def search(self, user_agent):
        self.calls += 1
        return 'bot' in user_agent.lower()


class ParsedDevice:
    def client_name(self):
        return 'Firefox'

    def client_version(self):
        return '111.0'


def test_reuses_robot_classification_for_repeated_user_agents(monkeypatch):
    pattern = CountingRobotPattern()
    monkeypatch.setattr(
        log_handler.resource_utils,
        'load_robots',
        lambda **kwargs: [pattern],
    )
    parser = log_handler.LogParser(mmdb_path=MMDB_PATH, robots_list=['ignored'])

    assert parser.user_agent_is_bot('Mozilla/5.0') is False
    assert parser.user_agent_is_bot('Mozilla/5.0') is False
    assert parser.user_agent_is_bot('ExampleBot/1.0') is True
    assert parser.user_agent_is_bot('ExampleBot/1.0') is True
    assert pattern.calls == 2


def test_reuses_device_detection_without_changing_parsed_lines(monkeypatch):
    detector_calls = []

    class CountingDeviceDetector:
        def __init__(self, user_agent):
            detector_calls.append(user_agent)

        def parse(self):
            return ParsedDevice()

    monkeypatch.setattr(log_handler, 'DeviceDetector', CountingDeviceDetector)
    parser = log_handler.LogParser(
        mmdb_path=MMDB_PATH,
        robots_list=[],
        output_mode='dict',
    )
    line = (
        'MISS|200|1755473648|1435|4339610|185.29.10.0|-|'
        'http://www.scielo.br/scielo.php?script=sci_arttext|SE|'
        'Mozilla/5.0 Test Agent|d0b6cb231fafac81cf42c524d05e0882|SE'
    )

    first_result = parser.parse_line(line)
    second_result = parser.parse_line(line)

    assert first_result == second_result
    assert first_result['client_name'] == 'Firefox'
    assert first_result['client_version'] == '111.0'
    assert detector_calls == ['Mozilla/5.0 Test Agent']
    assert parser.stats.lines_parsed == 2
    assert parser.stats.total_imported_lines == 2


def test_reuses_device_detection_between_parsers(monkeypatch):
    detector_calls = []

    class CountingDeviceDetector:
        def __init__(self, user_agent):
            detector_calls.append(user_agent)

        def parse(self):
            return ParsedDevice()

    monkeypatch.setattr(log_handler, 'DeviceDetector', CountingDeviceDetector)
    first_parser = log_handler.LogParser(mmdb_path=MMDB_PATH, robots_list=[])
    second_parser = log_handler.LogParser(mmdb_path=MMDB_PATH, robots_list=[])

    assert first_parser._detect_client('Shared Agent') == ('Firefox', '111.0')
    assert second_parser._detect_client('Shared Agent') == ('Firefox', '111.0')
    assert detector_calls == ['Shared Agent']


def test_rejects_static_resource_before_robot_and_client_detection(monkeypatch):
    pattern = CountingRobotPattern()
    detector_calls = []

    class CountingDeviceDetector:
        def __init__(self, user_agent):
            detector_calls.append(user_agent)

        def parse(self):
            return ParsedDevice()

    monkeypatch.setattr(log_handler, 'DeviceDetector', CountingDeviceDetector)
    monkeypatch.setattr(
        log_handler.resource_utils,
        'load_robots',
        lambda **kwargs: [pattern],
    )
    parser = log_handler.LogParser(
        mmdb_path=MMDB_PATH,
        robots_list=['ignored'],
    )
    line = (
        'MISS|200|1755473648|1435|4339610|185.29.10.0|-|'
        'https://www.scielo.br/static/app.css|SE|'
        'ExampleBot/1.0|d0b6cb231fafac81cf42c524d05e0882|SE'
    )

    assert parser.parse_line(line) is None
    assert parser.stats.ignored_lines_static_resources == 1
    assert parser.stats.ignored_lines_bot == 0
    assert pattern.calls == 0
    assert detector_calls == []


def test_reuses_ip_origin_classification(monkeypatch):
    real_ip_address = log_handler.ipaddress.ip_address
    calls = []

    def counting_ip_address(ip):
        calls.append(ip)
        return real_ip_address(ip)

    monkeypatch.setattr(log_handler.ipaddress, 'ip_address', counting_ip_address)
    parser = log_handler.LogParser(mmdb_path=MMDB_PATH, robots_list=[])

    assert parser.get_ip_origin_type('185.29.10.0') == log_handler.IP_ORIGIN_REMOTE
    assert parser.get_ip_origin_type('185.29.10.0') == log_handler.IP_ORIGIN_REMOTE
    assert calls == ['185.29.10.0']


def test_user_agent_cache_evicts_least_recently_used_entry(monkeypatch):
    pattern = CountingRobotPattern()
    monkeypatch.setattr(log_handler, 'USER_AGENT_CACHE_MAX_SIZE', 2)
    monkeypatch.setattr(
        log_handler.resource_utils,
        'load_robots',
        lambda **kwargs: [pattern],
    )
    parser = log_handler.LogParser(mmdb_path=MMDB_PATH, robots_list=['ignored'])

    parser.user_agent_is_bot('Agent A')
    parser.user_agent_is_bot('Agent B')
    parser.user_agent_is_bot('Agent A')
    parser.user_agent_is_bot('Agent C')
    parser.user_agent_is_bot('Agent B')

    assert pattern.calls == 4
