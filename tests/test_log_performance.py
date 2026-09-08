import unittest
from unittest import mock

from scielo_usage_counter import log


class ParsedDevice:
    UNKNOWN = 'UNK'

    def client_short_name(self):
        return 'FF'

    def client_name(self):
        return 'Firefox'

    def client_version(self):
        return '111.0'


class RobotPattern:
    def __init__(self):
        self.calls = 0

    def search(self, user_agent):
        self.calls += 1
        return 'bot' in user_agent.lower()


class TestLogPerformance(unittest.TestCase):
    def setUp(self):
        log._CLIENT_CACHE.clear()

    def make_parser(self, robots=None):
        parser = log.LogParser.__new__(log.LogParser)
        parser._LogParser__robots = robots or []
        parser._LogParser__robot_cache = log.OrderedDict()
        parser._LogParser__ip_type_cache = log.OrderedDict()
        return parser

    @mock.patch('scielo_usage_counter.log.DeviceDetector')
    def test_reuses_client_detection_and_skips_physical_device(self, detector):
        detector.return_value.parse.return_value = ParsedDevice()
        parser = self.make_parser()

        first = parser._detect_client('Mozilla/5.0 Test Agent')
        second = parser._detect_client('Mozilla/5.0 Test Agent')

        self.assertEqual(('FF', '111.0'), first)
        self.assertEqual(first, second)
        detector.assert_called_once_with(
            'Mozilla/5.0 Test Agent',
            skip_device_detection=True,
        )

    @mock.patch('scielo_usage_counter.log.DeviceDetector')
    def test_client_cache_evicts_least_recently_used_entry(self, detector):
        detector.return_value.parse.return_value = ParsedDevice()
        parser = self.make_parser()

        with mock.patch.object(log, 'USER_AGENT_CACHE_MAX_SIZE', 2):
            parser._detect_client('Agent A')
            parser._detect_client('Agent B')
            parser._detect_client('Agent A')
            parser._detect_client('Agent C')
            parser._detect_client('Agent B')

        self.assertEqual(4, detector.call_count)

    def test_reuses_robot_classification(self):
        robot_pattern = RobotPattern()
        parser = self.make_parser([robot_pattern])

        self.assertTrue(parser.user_agent_is_bot('ExampleBot/1.0'))
        self.assertTrue(parser.user_agent_is_bot('ExampleBot/1.0'))
        self.assertEqual(1, robot_pattern.calls)

    @mock.patch('scielo_usage_counter.log.ipaddress.ip_address')
    def test_reuses_ip_classification(self, ip_address):
        address = mock.Mock()
        address.is_global = True
        ip_address.return_value = address
        parser = self.make_parser()

        self.assertEqual('remote', parser.get_ip_type('192.0.2.1'))
        self.assertEqual('remote', parser.get_ip_type('192.0.2.1'))
        ip_address.assert_called_once_with('192.0.2.1')


if __name__ == '__main__':
    unittest.main()
