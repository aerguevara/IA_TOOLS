import os
from jira import JIRA
from domain.interfaces.services import IJiraService
from domain.entities.release_entities import ReleaseProject, JiraTicket
from typing import List

class JiraAdapter(IJiraService):
    def __init__(self):
        self.url = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.token = os.getenv("JIRA_API_TOKEN")
        self.client = JIRA(server=self.url, basic_auth=(self.email, self.token))

    def get_release_tickets(self, status: str) -> List[ReleaseProject]:
        query = f'type = "Release" AND status = "{status}"'
        issues = self.client.search_issues(query)
        return [
            ReleaseProject(
                key=issue.key,
                version=getattr(issue.fields, 'customfield_10001', 'unknown'), # Example field
                status=issue.fields.status.name
            ) for issue in issues
        ]

    def get_completed_child_tickets(self, release_key: str) -> List[JiraTicket]:
        query = f'parent = "{release_key}" AND status IN ("Done", "Closed", "Completed")'
        issues = self.client.search_issues(query)
        return [
            JiraTicket(
                key=issue.key,
                status=issue.fields.status.name,
                summary=issue.fields.summary
            ) for issue in issues
        ]
