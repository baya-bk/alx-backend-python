#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org calls get_json with the correct URL.
        """
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"payload": True})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct repos_url.
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value={"repos_url":
                          "https://api.github.com/orgs/google/repos"},
        ):
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch("client.get_json", return_value=[{"name": "repo1"},
                                            {"name": "repo2"}])
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns a list of repo names.
        """
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/google/repos",
        ):
            client = GithubOrgClient("google")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license correctly checks repo licenses.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


# ---- Integration Tests ----

def extract_repo_names(repos):
    """
    Extract all repository names from the given payload.
    """
    return [repo["name"] for repo in repos]


def extract_apache2_repos(repos):
    """
    Extract all repositories licensed under apache-2.0.
    """
    return [
        repo["name"]
        for repo in repos
        if repo.get("license") and repo["license"].get("key") == "apache-2.0"
    ]


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": extract_repo_names(TEST_PAYLOAD[0][1]),
        "apache2_repos": extract_apache2_repos(TEST_PAYLOAD[0][1]),
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient using fixtures.
    """

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks for integration tests."""

        def mock_get_json(url):
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return cls.org_payload

        cls.get_patcher = patch("client.get_json", side_effect=mock_get_json)
        cls.get_patcher.start()


    @classmethod
    def tearDownClass(cls):
        """
        Stop the requests.get patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos returns expected repo list.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos filtering by license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )
