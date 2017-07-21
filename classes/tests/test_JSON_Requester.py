####
import sys
path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\' +
        'Stats Canada\\Travel\\TDD\\Google')
if path not in sys.path:
    sys.path.append(path)
####
import os
import unittest
import json
import pandas as pd
import tempfile
from unittest import mock
from unittest.mock import patch
from classes.json_requester.JSON_Requester import JSON_Requester

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def json(self):
            return self.json_data
    '''
    Assign Google API web address and file path where properly downloaded JSON
    files are located.
    '''
    uri = 'https://www.googleapis.com/qpxExpress/v1/trips/search'
    api_key = '?key=' + 'AIzaSyBGmAqPd3KNGuvyG-8UF7mW80jeENnanWg'
    url = uri + api_key
    path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada\\'
            'Travel\\TDD\\Google\\files\\test_files\\')

    '''
    Below, we will extract the origin, destination, depart_date, and
    return date from the payload JSON. The payload JSON was sent to this mock
    function as KWARGS
    '''
    request_params = []
    params = ['origin', 'destination', 'date', 'date']
    for x in range(4):
        if x != 3:
            request_param = kwargs['json']['request']['slice'][0][params[x]]
            request_params.append(request_param)
        else:
            request_param = kwargs['json']['request']['slice'][1][params[x]]
            request_params.append(request_param)

    '''
    The tuples below contain a list of the desired request parameter data, and
    a file path to the associated JSON file (that will act as a mock response)
    '''
    yyz_pek_june27_return = (['YYZ', 'PEK', '2017-06-27', '2017-07-10'],
                             '2017627-YYZ-PEK.JSON')
    yyz_pek_error = (['YYZ', 'PEK', '2015-06-27', '2015-07-10'], '')
    yul_cia_empty = (['YUL', 'CIA', '2017-08-04', '2017-08-08'],
                     '20170714-YUL-CIA.JSON')

    trip_json = [
                 yyz_pek_june27_return,
                 yyz_pek_error,
                 yul_cia_empty,
                 ]
    # Iterate through the test trips to find a match.
    file_name = ''
    for trip in trip_json:
        if request_params == trip[0][:4]:
            file_name = trip[1]
            break

    if file_name != '':
        with open(path + file_name, 'r') as f:
            return_json = f.read()
            good_request = True
    else:
        good_request = False

    if args[0] == url and good_request is True:
        return MockResponse(return_json, 200)
    return MockResponse("Error 404", 404)


class Test_JSON_Requester(unittest.TestCase):

    def setUp(self):
        # Create a global class variable for the Google API endpoint URL
        uri = 'https://www.googleapis.com/qpxExpress/v1/trips/search'
        api_key = '?key=' + 'AIzaSyBGmAqPd3KNGuvyG-8UF7mW80jeENnanWg'
        self.url = uri + api_key

        # File path
        path = ('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada\\'
                'Travel\\TDD\\Google\\files\\test_files\\')
        self.yyz_pek_june27_ret = json.load(open(
                            path + '/2017627-YYZ-PEK.JSON', 'r'))
        self.yul_cia_empty = json.load(open(
                            path + '/20170714-YUL-CIA.JSON', 'r'))

        
        sample_data = {'Dest': 'PEK',
                       'Orig': 'YYZ',
                       'booking': 'four_weeks',
                       'dep_date': '2017-08-17',
                       'ret_date': '2017-08-31',
                       'today': '2017-07-20'}
        
        self.j_req = JSON_Requester(sample_data)

    # @unittest.skip('Skip')
    def test_payload_construction(self):
        expected_payload = {
                        "request": {
                                "passengers": {
                                        "adultCount": "1"
                                                },
                                        "slice": [
                                                  { # Depart
                                                    "origin": 'YYZ',
                                                    "destination": 'PEK',
                                                    "date": '2017-08-17',
                                                    "permittedCarrier": ['AC',
                                                                         'WS']
                                                  },
                                                  { # Return
                                                    "origin": 'PEK',
                                                    "destination": 'YYZ',
                                                    "date": '2017-08-31',
                                                    "permittedCarrier": ['AC',
                                                                         'WS']
                                                  }
                                                  ],
                                        "solutions": "10",
                                    }
                            }

        test_payload = self.j_req.set_payload()
        self.assertDictEqual(test_payload, expected_payload)

    # @unittest.skip('Skip')
    def test_read_API_key_from_file_with_url_returned(self):
        test_url = self.j_req.get_url_with_api_key()
        expected_url = ('https://www.googleapis.com/qpxExpress/v1/trips/search'
                        '?key=AIzaSyBGmAqPd3KNGuvyG-8UF7mW80jeENnanWg')
        self.assertEqual(test_url, expected_url)

    # @unittest.skip('Skip')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_200_response_from_Google_API(self, mock_patch):
        self.j_req.dep_date = '2017-06-27'
        self.j_req.ret_date = '2017-07-10'
        payload = self.j_req.set_payload()
        url = self.j_req.get_url_with_api_key()
        json_ = self.j_req.send_request(url, payload)
        self.assertDictEqual(json_, self.yyz_pek_june27_ret)

    # @unittest.skip('Skip')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_read_API_key_from_file_fail__missing__(self, mock_patch):
        self.j_req.dep_date = '2015-06-27'  # Dates are wrong
        self.j_req.ret_date = '2015-07-10'
        payload = self.j_req.set_payload()
        url = self.j_req.get_url_with_api_key()
        json_ = self.j_req.send_request(url, payload)
        self.assertIsNone(json_)

    # @unittest.skip('Skip')
    def test_error_log_file_is_written(self):
        class MockRequest():
            def __init__(self, status_code):
                self.status_code = status_code

        r = MockRequest(404)
        self.j_req.today = ''
        file_name = '_response_error_code.txt'
        self.j_req.path = tempfile.mkdtemp()
        os.mkdir(self.j_req.path + '\\error_logs\\')
        self.j_req.write_error_log(r)
        self.assertIn(file_name, os.listdir(self.j_req.path + '\\error_logs'))

    # @unittest.skip('Skip')
    def test_JSON_file_written_to_JSON_folder(self):
        self.j_req.path = tempfile.mkdtemp()

        class MockRequest():
            def __init__(self, status_code, text):
                self.status_code = status_code
                self.text = text
        text = json.dumps(self.yyz_pek_june27_ret)
        r = MockRequest(200, text)
        self.j_req.save_and_return_response(r)
        path = self.j_req.path + '\\json\\' + self.j_req.today
        self.assertEqual(len(os.listdir(path)), 1)

    # @unittest.skip('Skip')
    def test_empty_JSON_error_gets_logged_correctly_from_write_error_log(self):
        self.j_req.path = tempfile.mkdtemp()

        class MockRequest():
            def __init__(self, status_code, text):
                self.status_code = status_code
                self.text = text
        text = json.dumps(self.yul_cia_empty)
        r = MockRequest(200, text)
        self.j_req.write_error_log(r, status_code_error=False)
        path = self.j_req.path + '\\error_logs\\'
        self.assertEqual(len(os.listdir(path)), 1)

    # @unittest.skip('Skip')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_empty_JSON_error_gets_logged_correctly_from_send_request(self, m):
        self.j_req.orig = 'YUL'
        self.j_req.dest = 'CIA'
        self.j_req.dep_date = '2017-08-04'
        self.j_req.ret_date = '2017-08-08'
        self.j_req.path = tempfile.mkdtemp()

        payload = self.j_req.set_payload()
        self.j_req.send_request(self.url, payload)
        path = self.j_req.path + '\\error_logs\\'
        self.assertEqual(len(os.listdir(path)), 1)

if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
             '\\Travel\\TDD\\Google')
    unittest.main()
