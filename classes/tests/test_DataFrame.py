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
from classes.dataframe.DataFrame import DataFrame


class Test_DataFrame(unittest.TestCase):

    def setUp(self):
        self.df = DataFrame()

if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
             '\\Travel\\TDD\\Google')
    unittest.main()
