import unittest
from unittest.mock import patch, MagicMock
from git import GitCommandError
from infra.external.git_adapter import GitAdapter

class TestGitAdapter(unittest.TestCase):
    @patch('infra.external.git_adapter.Repo')
    @patch('os.makedirs')
    @patch('os.path.exists')
    def setUp(self, mock_exists, mock_makedirs, mock_repo_class):
        self.mock_repo = mock_repo_class.return_value
        mock_exists.return_value = True
        self.adapter = GitAdapter(workspace_path="/tmp/tests")
        self.adapter.current_repo = self.mock_repo

    def test_cherry_pick_success(self):
        result = self.adapter.cherry_pick("hash123")
        self.assertTrue(result)
        self.mock_repo.git.cherry_pick.assert_called_with("hash123")

    def test_cherry_pick_conflict(self):
        # First call fails, second call (abort) succeeds
        self.mock_repo.git.cherry_pick.side_effect = [GitCommandError("cherry-pick", 1), None]
        
        result = self.adapter.cherry_pick("hash-conflict")
        
        self.assertFalse(result)
        self.assertEqual(self.mock_repo.git.cherry_pick.call_count, 2)
        self.mock_repo.git.cherry_pick.assert_any_call("--abort")

    def test_create_branch(self):
        self.adapter.create_branch("release/v1", base="main")
        self.mock_repo.git.checkout.assert_called_with("main")
        self.mock_repo.create_head.assert_called_with("release/v1")
