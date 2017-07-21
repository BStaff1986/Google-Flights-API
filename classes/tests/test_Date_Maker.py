####
import sys
path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\' +
        'Stats Canada\\Travel\\TDD\\Google')
if path not in sys.path:
    sys.path.append(path)
####
import os
import datetime
import unittest
from unittest.mock import patch
from classes.date_maker.Date_Maker import Date_Maker


class Test_Basket_Proffer(unittest.TestCase):

    def setUp(self):
        self.dm = Date_Maker()
        self.test_dates = {'date': '2017-10-07',
                      'time': '14:42:53',
                      'four_weeks': {
                                     'depart': '2017-11-04',
                                     'intl_return': '2017-11-18',
                                     'dom_return': '2017-11-11',
                                    },
                      'eight_weeks': {
                                     'depart': '2017-12-02',
                                     'intl_return': '2017-12-16',
                                     'dom_return': '2017-12-09',
                                     },
                      }

    # @unittest.skip('Skip')
    def test_check_dict_is_returned_from_get_dates(self):
        dates = self.dm.get_dates()
        self.assertIsInstance(dates, dict)
        self.assertListEqual(list(dates.keys()), ['date', 'four_weeks',
                                                  'eight_weeks', 'time'])
        

    # @unittest.skip('Skip')
    def test_check_if_fill_dates_output_matches_expected_dates(self):
        self.dm.today = datetime.datetime(2017,10,7,14,42,53,915626)
        self.dm.fill_dates()
        self.assertDictEqual(self.dm.dates, self.test_dates)

if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
             '\\Travel\\TDD\\Google')
    unittest.main()
