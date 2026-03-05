import unittest
from unittest.mock import patch, MagicMock
import subprocess
import json
from infra.external.github_adapter import GitHubAdapter

class TestGitHubAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = GitHubAdapter()

    @patch('subprocess.run')
    def test_find_repository_for_ticket_found(self, mock_run):
        # Mock gh repo list
        mock_repo_list = [
            {"nameWithOwner": "owner/repo-a"},
            {"nameWithOwner": "owner/repo-b"}
        ]
        mock_run.side_effect = [
            MagicMock(stdout=json.dumps(mock_repo_list)), # repo list call
            MagicMock(stdout="feature/PROJ-123\n")        # branch check in repo-a
        ]

        result = self.adapter.find_repository_for_ticket("PROJ-123")
        
        self.assertEqual(result, "owner/repo-a")
        self.assertEqual(mock_run.call_count, 2)

    @patch('subprocess.run')
    def test_find_repository_for_ticket_not_found(self, mock_run):
        mock_run.return_value = MagicMock(stdout="[]") # No repos or no branches
        result = self.adapter.find_repository_for_ticket("ABSENT-1")
        self.assertIsNone(result)

    @patch('subprocess.run')
    def test_create_pull_request(self, mock_run):
        mock_run.return_value = MagicMock(stdout="https://github.com/owner/repo/pull/1")
        
        result = self.adapter.create_pull_request(
            "owner/repo", "head", "main", "Title", "Body"
        )
        
        self.assertEqual(result, "https://github.com/owner/repo/pull/1")
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        self.assertIn("pr", args[0])
        self.assertIn("create", args[0])
