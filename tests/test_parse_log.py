import unittest
from unittest import mock

from scielo_usage_counter import values
from scielo_usage_counter.proc import parse_log


class TestParseLog(unittest.TestCase):
    @mock.patch('scielo_usage_counter.proc.parse_log.file_utils.generate_filepath')
    @mock.patch('scielo_usage_counter.proc.parse_log.log.LogParser')
    @mock.patch('scielo_usage_counter.proc.parse_log.validator.pipeline_validate')
    def test_no_validate_skips_validator(
        self,
        pipeline_validate,
        log_parser,
        generate_filepath,
    ):
        generate_filepath.return_value = '/tmp/processed.tsv'
        parser = log_parser.return_value
        parser.parse.return_value = []
        parser.total_time = 0

        result = parse_log.parse_file(
            '/tmp/access.log',
            '/tmp',
            '/tmp/map.mmdb',
            '/tmp/robots.txt',
            validate=False,
        )

        pipeline_validate.assert_not_called()
        parser.save.assert_called_once_with([])
        self.assertEqual(values.LOGFILE_STATUS_LOADED, result)

    @mock.patch('scielo_usage_counter.proc.parse_log.log.LogParser')
    @mock.patch('scielo_usage_counter.proc.parse_log.validator.pipeline_validate')
    def test_invalid_file_is_not_parsed(self, pipeline_validate, log_parser):
        pipeline_validate.return_value = {'is_valid': {'all': False}}

        result = parse_log.parse_file(
            '/tmp/access.log',
            '/tmp',
            '/tmp/map.mmdb',
            '/tmp/robots.txt',
        )

        pipeline_validate.assert_called_once_with(
            path='/tmp/access.log',
            sample_size=0.05,
        )
        log_parser.assert_not_called()
        self.assertEqual(values.LOGFILE_STATUS_INVALIDATED, result)


if __name__ == '__main__':
    unittest.main()
