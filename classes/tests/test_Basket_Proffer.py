####
import sys
path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\' +
        'Stats Canada\\Travel\\TDD\\Google')
if path not in sys.path:
    sys.path.append(path)
####
import os
import tempfile
import unittest
import datetime
from unittest.mock import patch
import pandas as pd
from pandas.util.testing import assert_frame_equal
from classes.basket_proffer.Basket_Proffer import Basket_Proffer


class Test_Basket_Proffer(unittest.TestCase):

    def setUp(self):
        dates = {
                 'date': '2017-07-19',
                 'eight_weeks': {
                                 'depart': '2017-09-13',
                                 'dom_return': '2017-09-20',
                                 'intl_return': '2017-09-27'
                                 },
                 'four_weeks': {
                                 'depart': '2017-08-16',
                                 'dom_return': '2017-08-23',
                                 'intl_return': '2017-08-30'},
                 'time': '09:16:18'
                }

        self.test_df_good = pd.DataFrame(
                columns=['Area', 'Orig', 'Dest', 'Return'],
                data=[
                        ['Domestic', 'Ottawa', 'Toronto', 7],
                        ['Domestic', 'Vancouver', 'Winnipeg', 7],
                        ['Domestic', 'Fredricton', 'Beijing', 14],
                        ])
        self.test_df_NAs = pd.DataFrame(
                columns=['Area', 'Orig', 'Dest', 'Return'],
                data=[
                        ['Domestic', 'Ottawa', 'Toronto', 7],
                        ['Asia', 'Ottawa', 'Incheon', 14],  # NA
                        ['Domestic', 'Vancouver', 'Winnipeg', 7],
                        ['Trans-Atlantic', 'Toronto', 'Potemkin', 14],  # NA
                        ['Asia', 'Fredricton', 'Beijing', 14],
                        ])

        self.expected_df = pd.DataFrame(columns=['Orig', 'Dest', 'Return'],
                                        data=[['YOW', 'YYZ', 7],
                                              ['YVR', 'YWG', 7],
                                              ['YFC', 'PEK', 14]])
    
        self.bp = Basket_Proffer(dates)

    #@unittest.skip('Skip')
    def test_read_in_flight_basket_excel_file(self):
        result = self.bp.read_in_excel()
        self.assertIsInstance(result, pd.DataFrame)

    #@unittest.skip('Skip')
    def test_if_error_raised_when_file_is_missing(self):
        self.bp.read_in_excel()
        self.assertRaises(FileNotFoundError)

    #@unittest.skip('Skip')
    def test_if_all_cities_get_converted_properly(self):
        test_df = self.test_df_good
        test_df.drop('Area', axis=1, inplace=True)
        self.bp.convert_to_iata_code(test_df)
        assert_frame_equal(test_df, self.expected_df)

    #@unittest.skip('Skip')
    def test_if_unknown_cities_are_dropped_and_all_others_converted(self):
        test_df = self.test_df_NAs
        test_df.drop('Area', axis=1, inplace=True)
        self.bp.convert_to_iata_code(test_df)
        test_df.reset_index(inplace=True, drop=True)
        assert_frame_equal(test_df, self.expected_df)

    #@unittest.skip('Skip')
    def test_city_conversion_error_logged(self):
        self.bp.path = tempfile.mkdtemp()
        os.mkdir(self.bp.path + '\\error_logs\\')
        self.bp._write_to_error_log(2)
        file_name = (datetime.datetime.now().strftime('%Y-%m-%d') +
                     '_dropped_flights.txt')
        self.assertIn(file_name, os.listdir(self.bp.path + '\\error_logs'))

    #@unittest.skip('Skip')
    def test_converted_basket_written_to_file(self):
        self.bp.path = tempfile.mkdtemp()
        os.mkdir(self.bp.path + '\\flight_basket\\')
        to_export = self.expected_df
        self.bp.to_csv(to_export)
        self.assertIn('basket.csv',
                      os.listdir(self.bp.path + '\\flight_basket'))

if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
    '\\Travel\\TDD\\Google')
    unittest.main()
