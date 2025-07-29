#!/usr/bin/env python3
"""
Unit and integration tests for client.py module.
Covers GithubOrgClient class methods and integration with fixtures.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls get_json with the correct URL."""
        test_client = GithubOrgClient(org_name)
        test_client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns correct value from org payload."""
        mock_org.return_value = {"repos_url": "http://some_url.com/repos"}
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "http://some_url.com/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://some_url.com/repos"
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean for license key."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": ["episodes.dart"],
        "apache2_repos": ["episodes.dart"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up class by mocking requests.get."""
        patcher = patch("client.get_json", side_effect=cls.mock_get_json)
        cls.get_patcher = patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    @classmethod
    def mock_get_json(cls, url):
        """Mock get_json to return appropriate payload based on URL."""
        if url == GithubOrgClient.ORG_URL.format(org="google"):
            return cls.org_payload
        elif url == cls.org_payload["repos_url"]:
            return cls.repos_payload
        return None

    def test_public_repos(self):
        """Test that public_repos returns expected repo list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtering by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )
