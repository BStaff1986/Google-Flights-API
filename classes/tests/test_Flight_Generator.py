####
import sys
path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\' +
        'Stats Canada\\Travel\\TDD\\Google')
if path not in sys.path:
    sys.path.append(path)
####
import os
import types
import tempfile
import unittest
from unittest.mock import patch
import pandas as pd
from pandas.util.testing import assert_frame_equal
from classes.flight_generator.Flight_Generator import Flight_Generator
from classes.date_maker.Date_Maker import Date_Maker


class Test_Basket_Proffer(unittest.TestCase):

    def setUp(self):
        dates = Date_Maker().get_dates()
        self.fg = Flight_Generator(dates)

    # @unittest.skip('Skip')
    def test_read_in_csv_and_create_iterrows_generator(self):
        generator = self.fg.read_csv_to_iterrows()
        self.assertIsInstance(generator,
                              types.GeneratorType)

    # @unittest.skip('Skip')
    def test_missing_basket_file_raises_error(self):
        with self.assertRaises(OSError):
            self.fg.path = tempfile.mkdtemp()
            os.mkdir(self.fg.path + '\\flight_basket\\')
            os.mkdir(self.fg.path + '\\error_logs\\')
            self.fg.read_csv_to_iterrows()

    # @unittest.skip('Skip')
    def test_dates_are_properly_extracted(self):
        x = 0
        return_days = 14
        dates = {'date': 'pass',
                 'eight_weeks': {'depart': '2017-09-14',
                                 'dom_return': '2017-09-21',
                                 'intl_return': '2017-09-28'},
                 'four_weeks':  {'depart': 'pass',
                                 'dom_return': 'fail',
                                 'intl_return': 'pass'},
                 'time': '12:42:58'}
        test_dict = self.fg.extract_dates(x, dates, return_days)

        expected_dict = {'today': 'pass',
                         'dep_date': 'pass',
                         'ret_date': 'pass',
                         'booking': 'four_weeks',
                         }

        self.assertDictEqual(test_dict, expected_dict)
        
    # @unittest.skip('Skip')
    def test_set_dictionaries_returns_all_wanted_values(self):
        city_pair = ([[0, pd.Series(['YOW', 'YVR', 7], index=['Orig', 
                                                              'Dest', 
                                                              'Return'])]])
        city_pair_generator = (city for city in city_pair)

        dates = {'date': 'pass',
                 'eight_weeks': {'depart': 'pass_1',
                                 'dom_return': 'pass_1',
                                 'intl_return': 'fail_1'},
                 'four_weeks':  {'depart': 'pass_0',
                                 'dom_return': 'pass_0',
                                 'intl_return': 'fail_0'},
                 'time': '12:42:58'}
                 
        test_dict_list = self.fg.set_dictionaries(city_pair_generator, dates)
        
        expected_dict_1 = { 'Dest': 'YVR',
                            'Orig': 'YOW',
                            'booking': 'four_weeks',
                            'dep_date': 'pass_0',
                            'ret_date': 'pass_0',
                            'today': 'pass'}
        
        expected_dict_2 = { 'Dest': 'YVR',
                            'Orig': 'YOW',
                            'booking': 'eight_weeks',
                            'dep_date': 'pass_1',
                            'ret_date': 'pass_1',
                            'today': 'pass'}
        expected_dict_list = [expected_dict_1, expected_dict_2]
                 
        self.assertDictEqual(test_dict_list[0], expected_dict_list[0])
        self.assertDictEqual(test_dict_list[1], expected_dict_list[1])
        
    # @unittest.skip('Skip')
    def test_generator_is_created_by_get_generator(self):
        expected_dict_1 = { 'Dest': 'YVR',
                            'Orig': 'YOW',
                            'booking': 'four_weeks',
                            'dep_date': 'pass_0',
                            'ret_date': 'pass_0',
                            'today': 'pass'}
        
        expected_dict_2 = { 'Dest': 'YVR',
                            'Orig': 'YOW',
                            'booking': 'eight_weeks',
                            'dep_date': 'pass_1',
                            'ret_date': 'pass_1',
                            'today': 'pass'}
        expected_dict_list = [expected_dict_1, expected_dict_2]
        
        generator = self.fg.get_generator(expected_dict_list)
        self.assertIsInstance(generator,
                              types.GeneratorType)

if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
             '\\Travel\\TDD\\Google')
    unittest.main()
