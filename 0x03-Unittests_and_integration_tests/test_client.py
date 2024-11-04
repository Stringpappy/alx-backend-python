#!/usr/bin/env python3
""" Unit tests for the GithubOrgClient class and its methods. """

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """ Tests for the GithubOrgClient functionality. """

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch('client.get_json')
    def test_org_retrieval(self, org_name, mock):
        """ Verify that GithubOrgClient.org returns the correct organization URL. """
        client_instance = GithubOrgClient(org_name)
        client_instance.org()
        mock.assert_called_once_with(client_instance.ORG_URL.format(org=org_name))

    def test_public_repos_url_retrieval(self):
        """ Verify that the _public_repos_url method returns the correct URL based on the payload. """
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock:
            payload = {"repos_url": "Hello World"}
            mock.return_value = payload
            client_instance = GithubOrgClient('test')
            result = client_instance._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos_retrieval(self, mock_json):
        """ Unit test for the public_repos method of GithubOrgClient. 
            Verify that it returns the expected list of repositories. 
            Ensure the mocked property and get_json are called once. 
        """
        payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_json.return_value = payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public:
            mock_public.return_value = "hello world"
            client_instance = GithubOrgClient('test')
            result = client_instance.public_repos()

            expected = [item["name"] for item in payload]
            self.assertEqual(result, expected)

            mock_public.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_license_check(self, repo, license_key, expected):
        """ Unit test for checking if a repository has a specific license. """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration tests for the GithubOrgClient using predefined payloads. """
    
    @classmethod
    def setUpClass(cls):
        """ Method executed before any tests in the class run. """
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock = cls.get_patcher.start()

    def test_integration_public_repos(self):
        """ Integration test for verifying public repositories. """
        client_instance = GithubOrgClient("google")

        self.assertEqual(client_instance.org, self.org_payload)
        self.assertEqual(client_instance.repos_payload, self.repos_payload)
        self.assertEqual(client_instance.public_repos(), self.expected_repos)
        self.assertEqual(client_instance.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_integration_public_repos_with_license(self):
        """ Integration test for public repositories filtered by license. """
        client_instance = GithubOrgClient("google")

        self.assertEqual(client_instance.public_repos(), self.expected_repos)
        self.assertEqual(client_instance.public_repos("XLICENSE"), [])
        self.assertEqual(client_instance.public_repos("apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """ Method executed after all tests in the class have run. """
        cls.get_patcher.stop()

