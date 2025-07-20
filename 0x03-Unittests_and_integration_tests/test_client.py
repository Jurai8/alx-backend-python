#!/usr/bin/env python3

import utils
from utils import memoize
from unittest.mock import patch, Mock, MagicMock
from parameterized import parameterized, parameterized_class
import unittest
import client 
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""
    @parameterized.expand([
        (("Google"),),
        (("abc"), )
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""

        expected_org_data = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_org_data

        client = GithubOrgClient(org_name)

        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Assert the result is what we expect
        self.assertEqual(result, expected_org_data)
