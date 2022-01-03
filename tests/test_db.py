import datetime
import unittest

from app import values
from app.lib import db


class TestDB(unittest.TestCase):
    def test_previous_and_next_dates(self):
        date = datetime.datetime.strptime('2021-01-01' , '%Y-%m-%d')
        obtained_pn_dates = db._get_previous_and_next_dates(date)
        expected_pn_dates = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in ['2021-01-01', '2020-12-31', '2021-01-02', '2020-12-30', '2021-01-03']]

        self.assertListEqual(obtained_pn_dates, expected_pn_dates)

    def test_dates_able_to_pretable(self):
        date_status = {
            datetime.datetime.strptime('2021-01-01', '%Y-%m-%d'): values.DATE_STATUS_LOADED,
            datetime.datetime.strptime('2021-01-02', '%Y-%m-%d'): values.DATE_STATUS_LOADED,
            datetime.datetime.strptime('2021-01-03', '%Y-%m-%d'): values.DATE_STATUS_LOADED,
            datetime.datetime.strptime('2021-01-04', '%Y-%m-%d'): values.DATE_STATUS_LOADED,
            datetime.datetime.strptime('2021-01-05', '%Y-%m-%d'): values.DATE_STATUS_LOADED,
            datetime.datetime.strptime('2021-01-06', '%Y-%m-%d'): values.DATE_STATUS_LOADED,
        }
        expected_dates_able_to_extract = [
            datetime.datetime.strptime('2021-01-03', '%Y-%m-%d'), 
            datetime.datetime.strptime('2021-01-04', '%Y-%m-%d')
        ]
        obtained_dates_able_to_extract = db._get_enabled_dates_by_status_value(date_status, values.DATE_STATUS_LOADED)

        self.assertListEqual(expected_dates_able_to_extract, obtained_dates_able_to_extract)
