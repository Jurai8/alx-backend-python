#!/usr/bin/env python3

"""
This module contains unit tests for the utils module.

It tests functionality including nested map access, JSON retrieval,
and memoization decorators using unittest and mocking.
"""
import utils
from utils import memoize
from unittest.mock import patch, Mock, MagicMock
from parameterized import parameterized, parameterized_class
import unittest


class TestAccessNestedMap(unittest.TestCase):

    """Test class for testing the access_nested_map function."""

    @parameterized.expand([
        # input(nested map), path, result
        ({"a": 1}, ("a",), (1)),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, result):
        """
        Test the nested map and the corresponding paths
        to see if they yeild the correct result
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ({}, ("a"), (KeyError)),
        ({"a": 1}, ("a", "b"), (KeyError)),
    ])
    def test_access_nested_map_exception(self, nested_map, path, exception):
        """
        Test if access nested map will raise an error when trying to access
        a non existent path
        """
        with self.assertRaises(exception):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    This class is used to test the get_json function.
    paramaterized is used for the arguments. patch and
    mock are used instead of calling the actual function
    """

    @parameterized.expand([
        (("http://example.com"), {"payload": True}),
        (("http://holberton.io"), {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test whether the get function returns a json corresponding to the url
        use mock to avoid creating an actual request by mimicking the
        get function
        """
        mock_response = MagicMock()
        mock_response.json.return_value = test_payload

        mock_get.return_value = mock_response

        result = utils.get_json(test_url)

        mock_get.assert_called_once_with(test_url)

        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    This class is used to test memoize, by mocking an object
    and testing it's functionality
    """

    def test_memoize(self):
        """
        Test that the memoize decorator properly caches function results.
        Verifies that a decorated method is only called once even when
        accessed multiple times, demonstrating proper memoization behavior.
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        instance = TestClass()

        with patch.object(instance, 'a_method',
                          return_value=42) as mock_a_method:
            result1 = instance.a_property
            result2 = instance.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()
