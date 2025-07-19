
import utils
from parameterized import parameterized, parameterized_class
import unittest

class TestAccessNestedMap:

    @parameterized.expand 
    def test_access_nested_map(self):
        nested_map = {"a": {"b": {"c": 1}}}
        self.assertEqual(utils.access_nested_map(nested_map), 1 )