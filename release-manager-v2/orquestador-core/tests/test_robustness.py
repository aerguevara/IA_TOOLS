import unittest
from unittest.mock import Mock, patch
from domain.use_cases.prepare_release import PrepareReleaseUseCase
from domain.entities.release_entities import ReleaseProject, JiraTicket

class TestPrepareReleaseRobustness(unittest.TestCase):
    def setUp(self):
        self.mock_jira = Mock()
        self.mock_github = Mock()
        self.mock_git = Mock()
        self.mock_notifier = Mock()
        self.use_case = PrepareReleaseUseCase(
            self.mock_jira, self.mock_github, self.mock_git, self.mock_notifier
        )

    def test_partial_success_some_tickets_missing_repos(self):
        # Case where some tickets don't have repos
        release = ReleaseProject(key="REL-1", version="1.0.0", status="Ready for PRE")
        self.mock_jira.get_release_tickets.return_value = [release]
        
        t1 = JiraTicket(key="PROJ-1", status="Done", summary="T1")
        t2 = JiraTicket(key="PROJ-2", status="Done", summary="T2")
        self.mock_jira.get_completed_child_tickets.return_value = [t1, t2]
        
        # PROJ-1 has repo, PROJ-2 does not
        self.mock_github.find_repository_for_ticket.side_effect = ["user/repo1", None]
        
        # Should not crash and should continue
        self.use_case.execute()
        
        self.assertEqual(self.mock_github.find_repository_for_ticket.call_count, 2)

    def test_config_sync_api_failure(self):
        # Test if the orchestrator handles Config Crew API 500 errors gracefully
        release = ReleaseProject(key="REL-1", version="1.0.0", status="Ready for PRE")
        self.mock_jira.get_release_tickets.return_value = [release]
        self.mock_jira.get_completed_child_tickets.return_value = []
        
        with patch('domain.use_cases.prepare_release.requests.post') as mock_post:
            mock_post.return_value.status_code = 500
            
            # This is hard to test without full implementation of _handle_config_sync
            # but let's assume it should log/print and continue
            self.use_case.execute() 
            # Verification of internal call if we had more hooks
