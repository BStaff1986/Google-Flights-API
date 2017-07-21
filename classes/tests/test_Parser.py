####
import sys
path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\' +
        'Stats Canada\\Travel\\TDD\\Google')
if path not in sys.path:
    sys.path.append(path)
####
import os
import json
import types
import tempfile
import unittest
import datetime
from unittest.mock import patch
import pandas as pd
from pandas.util.testing import assert_frame_equal
from classes.parser.Parser import Parser


class Test_Basket_Proffer(unittest.TestCase):

    def setUp(self):
        file_path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada\\'
                 'Travel\\TDD\\Google\\files\\json\\2017-07-18'
                 '\\2017-07-18-YYZ-PEK_(4 weeks).JSON')
        with open(file_path, 'r') as f:
            self.json_ = json.load(f)
            
        self.parser = Parser(self.json_)
   
    # @unittest.skip('Skip')
    def test_generator_creation(self):
        generator = self.parser.get_generator(self.json_)
        self.assertIsInstance(generator,
                              types.GeneratorType)
        

if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
    '\\Travel\\TDD\\Google')
    unittest.main()
