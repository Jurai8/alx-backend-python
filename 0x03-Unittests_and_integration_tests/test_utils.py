#!/usr/bin/env python3

import utils
from utils import memoize
from unittest.mock import patch, Mock, MagicMock
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
    
    @parameterized.expand([
        (("http://example.com"), {"payload": True}),
        (("http://holberton.io"), {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):

        mock_response = MagicMock()
        mock_response.json.return_value = test_payload

        mock_get.return_value = mock_response

        result = utils.get_json(test_url)

        mock_get.assert_called_once_with(test_url)

        self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    
    def test_memoize(self):
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        instance = TestClass()

        with patch.object(instance, 'a_method') as mock_a_method:
            result1 = instance.a_property()
            result2 = instance.a_property()
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()


