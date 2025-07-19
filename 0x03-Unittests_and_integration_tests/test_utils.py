#!/usr/bin/env python3

import utils
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
import unittest

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        # input(nested map), path, result
        ({"a": 1}, ("a",), (1)),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ]) 
    def test_access_nested_map(self, nested_map, path, result):
        self.assertEqual(utils.access_nested_map(nested_map, path), result)


    @parameterized.expand([
        ({}, ("a"), (KeyError)),
        ({"a": 1}, ("a", "b"), (KeyError)),
    ])
    def test_access_nested_map_exception(self, nested_map, path, exception):
            with self.assertRaises(exception):
                utils.access_nested_map(nested_map, path) 



    class TestGetJson(unittest.TestCase):
        @unittest.mock.patch('utils.requests.get')
        @parameterized.expand([
        (("http://example.com"), {"payload": True}),
        (("http://holberton.io"), {"payload": True})
    ])
        
        def test_get_json(self, test_url, test_payload, mock_get):
            mock_response = Mock()

            mock_response.json.return_value = test_payload

            mock_get.return_value = mock_response

            result = utils.get_json(test_url)

            mock_get.assert_called_once_with(test_url)

            self.assertEqual(result, test_payload)