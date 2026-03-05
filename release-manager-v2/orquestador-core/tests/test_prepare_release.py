import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from unittest.mock import Mock, patch
from domain.use_cases.prepare_release import PrepareReleaseUseCase
from domain.entities.release_entities import ReleaseProject, JiraTicket

class TestPrepareReleaseUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_jira = Mock()
        self.mock_github = Mock()
        self.mock_git = Mock()
        self.mock_notifier = Mock()
        self.use_case = PrepareReleaseUseCase(
            self.mock_jira, self.mock_github, self.mock_git, self.mock_notifier
        )

    def test_execute_with_no_releases(self):
        self.mock_jira.get_release_tickets.return_value = []
        
        self.use_case.execute("Ready for PRE")
        
        self.mock_jira.get_release_tickets.assert_called_once_with("Ready for PRE")
        self.mock_github.find_repository_for_ticket.assert_not_called()

    def test_execute_with_one_release_and_tickets(self):
        # Setup
        release = ReleaseProject(key="REL-1", version="1.0.0", status="Ready for PRE")
        self.mock_jira.get_release_tickets.return_value = [release]
        
        ticket = JiraTicket(key="PROJ-123", status="Done", summary="Feature A")
        self.mock_jira.get_completed_child_tickets.return_value = [ticket]
        
        self.mock_github.find_repository_for_ticket.return_value = "user/repo"
        
        # Execute
        self.use_case.execute("Ready for PRE")
        
        # Assert
        self.mock_jira.get_release_tickets.assert_called_once()
        self.mock_jira.get_completed_child_tickets.assert_called_with("REL-1")
        self.mock_github.find_repository_for_ticket.assert_called_with("PROJ-123")

if __name__ == "__main__":
    unittest.main()
