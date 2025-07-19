#!/usr/bin/env python3

import utils
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