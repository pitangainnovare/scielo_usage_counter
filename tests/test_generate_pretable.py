import argparse
import datetime
import os
import tempfile
import unittest
from unittest import mock

from scielo_usage_counter import values
from scielo_usage_counter.proc import generate_pretable


class TestPeriod(unittest.TestCase):
    def test_parse_single_date(self):
        date = datetime.date(2026, 8, 15)

        self.assertEqual((date, date), generate_pretable.parse_period('2026-08-15'))

    def test_parse_date_range(self):
        self.assertEqual(
            (datetime.date(2026, 8, 15), datetime.date(2026, 8, 20)),
            generate_pretable.parse_period('2026-08-15,2026-08-20'),
        )

    def test_reject_reversed_date_range(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            generate_pretable.parse_period('2026-08-20,2026-08-15')

    def test_reject_invalid_date(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            generate_pretable.parse_period('2026-08-32')

    def test_filter_dates_uses_inclusive_range(self):
        dates = [
            datetime.date(2026, 8, 14),
            datetime.date(2026, 8, 15),
            datetime.date(2026, 8, 20),
            datetime.date(2026, 8, 21),
        ]
        period = generate_pretable.parse_period('2026-08-15,2026-08-20')

        self.assertEqual(dates[1:3], generate_pretable.filter_dates(dates, period))


class TestGeneratePretables(unittest.TestCase):
    def test_writes_only_target_dates_from_neighboring_log_files(self):
        with tempfile.TemporaryDirectory() as directory:
            parsed_file = os.path.join(directory, 'processed.tsv')
            output_directory = os.path.join(directory, 'output')
            os.mkdir(output_directory)

            with open(parsed_file, 'w') as output:
                output.write('\t'.join(values.PRETABLE_FILE_HEADER) + '\n')
                output.write('2026-08-14 23:59:59\tCH\t1\t192.0.2.1\t1\t2\thttps://example.org/14\n')
                output.write('2026-08-15 00:00:00\tCH\t1\t192.0.2.2\t1\t2\thttps://example.org/15\n')
                output.write('2026-08-16 00:00:00\tCH\t1\t192.0.2.3\t1\t2\thttps://example.org/16\n')

            generate_pretable.generate_pretables(
                parsed_file,
                output_directory,
                target_dates={'2026-08-15'},
            )

            expected_path = os.path.join(output_directory, '2026-08-15.unsorted.tsv')
            with open(expected_path) as generated:
                lines = generated.readlines()

            self.assertEqual(2, len(lines))
            self.assertIn('2026-08-15 00:00:00', lines[1])
            self.assertFalse(os.path.exists(os.path.join(output_directory, '2026-08-14.unsorted.tsv')))
            self.assertFalse(os.path.exists(os.path.join(output_directory, '2026-08-16.unsorted.tsv')))

    def test_empty_target_dates_does_not_write_files(self):
        with tempfile.TemporaryDirectory() as directory:
            parsed_file = os.path.join(directory, 'processed.tsv')
            output_directory = os.path.join(directory, 'output')
            os.mkdir(output_directory)

            with open(parsed_file, 'w') as output:
                output.write('\t'.join(values.PRETABLE_FILE_HEADER) + '\n')
                output.write('2026-08-15 00:00:00\tCH\t1\t192.0.2.2\t1\t2\thttps://example.org/15\n')

            generate_pretable.generate_pretables(
                parsed_file,
                output_directory,
                target_dates=set(),
            )

            self.assertEqual([], os.listdir(output_directory))

    @mock.patch('scielo_usage_counter.proc.generate_pretable.file_utils.get_processed_files')
    @mock.patch('scielo_usage_counter.proc.generate_pretable.db.set_control_date_status')
    @mock.patch('scielo_usage_counter.proc.generate_pretable.db.get_non_pretable_dates')
    def test_database_generation_skips_existing_final_pretable(
        self,
        get_non_pretable_dates,
        set_control_date_status,
        get_processed_files,
    ):
        date = datetime.date(2026, 8, 15)
        get_non_pretable_dates.return_value = [date]

        with tempfile.TemporaryDirectory() as directory:
            unsorted_directory = os.path.join(directory, 'unsorted')
            pretables_directory = os.path.join(directory, 'pretables')
            os.mkdir(unsorted_directory)
            os.mkdir(pretables_directory)
            open(os.path.join(pretables_directory, '2026-08-15.tsv'), 'w').close()

            generate_pretable.generate_pretables_db(
                'mysql://example',
                'nbr',
                unsorted_directory,
                pretables_directory=pretables_directory,
                period=generate_pretable.parse_period('2026-08-15'),
            )

        get_processed_files.assert_not_called()
        set_control_date_status.assert_not_called()

    @mock.patch('scielo_usage_counter.proc.generate_pretable.subprocess.call')
    @mock.patch('scielo_usage_counter.proc.generate_pretable.db.set_control_date_status')
    @mock.patch('scielo_usage_counter.proc.generate_pretable.db.get_unsorted_pretables')
    def test_sort_does_not_overwrite_existing_pretable(
        self,
        get_unsorted_pretables,
        set_control_date_status,
        subprocess_call,
    ):
        date = datetime.date(2026, 8, 15)
        get_unsorted_pretables.return_value = [date]

        with tempfile.TemporaryDirectory() as directory:
            unsorted_directory = os.path.join(directory, 'unsorted')
            output_directory = os.path.join(directory, 'pretables')
            os.mkdir(unsorted_directory)
            os.mkdir(output_directory)

            open(os.path.join(unsorted_directory, '2026-08-15.unsorted.tsv'), 'w').close()
            open(os.path.join(output_directory, '2026-08-15.tsv'), 'w').close()

            generate_pretable.sort_pretables(
                'mysql://example',
                'nbr',
                output_directory,
                unsorted_pretables_directory=unsorted_directory,
            )

        subprocess_call.assert_not_called()
        set_control_date_status.assert_not_called()


if __name__ == '__main__':
    unittest.main()
