#!/usr/bin/env python3

import utils
from utils import memoize
from unittest.mock import patch, Mock, MagicMock, PropertyMock
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

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Unit test for GithubOrgClient._public_repos_url"""

        expected_repo_url = f"https://api.github.com/orgs/{org_name}"

        mock_org.return_value = {
            "repos_url": expected_repo_url,
            "name": "test-org",
        }

        client = GithubOrgClient("test-org")

        result = client._public_repos_url

        self.assertEqual(result, expected_repo_url)

        mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """test public repos"""

        # define the return value
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]

        mock_get_json.return_value = test_payload

        test_url = 'https://api.github.com/orgs/test/repos'
        with patch.object(
            GithubOrgClient, '_public_repos_url',
            new_callable=PropertyMock,
            return_value=test_url
        ) as mock_repos_url:

            # Create instance of GithubOrgClient
            client = GithubOrgClient("test-org")

            # Call the method we're testing
            result = client.public_repos()

            # Expected result should be list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]

            # Test that the result matches expected
            self.assertEqual(result, expected_repos)

            mock_repos_url.assert_called_once()

            # Test that get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/test/repos'
            )
