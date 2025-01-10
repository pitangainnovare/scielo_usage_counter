import datetime
import unittest

from scielo_usage_counter.database import db


class TestDB(unittest.TestCase):
    def test_previous_and_next_dates(self):
        date = datetime.datetime.strptime('2021-01-01' , '%Y-%m-%d')
        obtained_pn_dates = db._get_previous_and_next_dates(date)
        expected_pn_dates = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in ['2021-01-01', '2020-12-31', '2021-01-02', '2020-12-30', '2021-01-03']]

        self.assertListEqual(obtained_pn_dates, expected_pn_dates)
