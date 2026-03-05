import unittest
from unittest.mock import patch, MagicMock
from infra.external.jira_adapter import JiraAdapter
from domain.entities.release_entities import JiraTicket, ReleaseProject

class TestJiraAdapter(unittest.TestCase):
    @patch('infra.external.jira_adapter.JIRA')
    def setUp(self, mock_jira_class):
        self.mock_jira_instance = mock_jira_class.return_value
        with patch.dict('os.environ', {
            'JIRA_URL': 'https://test.atlassian.net',
            'JIRA_EMAIL': 'test@example.com',
            'JIRA_API_TOKEN': 'token'
        }):
            self.adapter = JiraAdapter()

    def test_get_release_tickets_success(self):
        mock_issue = MagicMock()
        mock_issue.key = "REL-1"
        mock_issue.fields.status.name = "Ready for PRE"
        mock_issue.fields.customfield_10001 = "1.0.0"
        self.mock_jira_instance.search_issues.return_value = [mock_issue]

        result = self.adapter.get_release_tickets("Ready for PRE")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].key, "REL-1")
        self.assertEqual(result[0].version, "1.0.0")
        self.mock_jira_instance.search_issues.assert_called_once_with('type = "Release" AND status = "Ready for PRE"')

    def test_get_completed_child_tickets(self):
        mock_child = MagicMock()
        mock_child.key = "PROJ-123"
        mock_child.fields.status.name = "Done"
        mock_child.fields.summary = "Fix bug"
        self.mock_jira_instance.search_issues.return_value = [mock_child]

        result = self.adapter.get_completed_child_tickets("REL-1")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].key, "PROJ-123")
        self.mock_jira_instance.search_issues.assert_called_with('parent = "REL-1" AND status IN ("Done", "Closed", "Completed")')

    def test_jira_api_error_handling(self):
        self.mock_jira_instance.search_issues.side_effect = Exception("Jira API Down")
        with self.assertRaises(Exception):
            self.adapter.get_release_tickets("Status")
