#!/usr/bin/env python3
""" Unittests and integration tests for GithubOrgClient """

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """ Test suite for the GithubOrgClient class """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org_returns_correct_value(self, org_name, mock_get_json):
        """ 
        Verify that the org method returns the correct URL 
        for the given organization name.
        """
        test_class = GithubOrgClient(org_name)
        test_class.org()
        mock_get_json.assert_called_once_with(test_class.ORG_URL.format(org=org_name))

    def test_public_repos_url_returns_correct_value(self):
        """ 
        Ensure that the _public_repos_url property returns 
        the expected repos_url from the org payload.
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            payload = {"repos_url": "Hello World"}
            mock_org.return_value = payload
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos_returns_expected_list(self, mock_get_json):
        """ 
        Test that the public_repos method returns the 
        correct list of repository names based on the payload.
        """
        payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_get_json.return_value = payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "hello world"
            test_class = GithubOrgClient('test')
            result = test_class.public_repos()

            expected = [item["name"] for item in payload]
            self.assertEqual(result, expected)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license_checks_correctly(self, repo, license_key, expected):
        """ 
        Verify that the has_license method correctly determines 
        if a repository has the specified license.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test suite for GithubOrgClient using fixtures """

    @classmethod
    def setUpClass(cls):
        """ 
        Set up the mock for requests.get before running tests 
        in this class. This will simulate responses from 
        the GitHub API.
        """
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock = cls.get_patcher.start()

    def test_integration_public_repos(self):
        """ 
        Integration test to verify public repositories 
        match the expected payload for a given organization.
        """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_integration_public_repos_with_license(self):
        """ 
        Integration test to verify public repositories 
        with a specific license match the expected payload.
        """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """ Stop the patcher after tests in this class have run. """
        cls.get_patcher.stop()
