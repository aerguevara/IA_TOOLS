from typing import List
from domain.interfaces.services import IJiraService, IGitHubService, IGitHandler, INotificationService
from domain.entities.release_entities import ReleaseProject, ReleaseReport, JiraTicket
import requests
import os

class PrepareReleaseUseCase:
    def __init__(
        self,
        jira: IJiraService,
        github: IGitHubService,
        git: IGitHandler,
        notifier: INotificationService
    ):
        self.jira = jira
        self.github = github
        self.git = git
        self.notifier = notifier
        self.config_crew_url = os.getenv("CONFIG_CREW_SOURCE_URL")

    def execute(self, release_status: str = "Ready for PRE"):
        releases = self.jira.get_release_tickets(release_status)
        
        for release in releases:
            print(f">>> Processing Release: {release.key}")
            tickets = self.jira.get_completed_child_tickets(release.key)
            
            successful_prs = []
            
            for ticket in tickets:
                print(f"  > Handling Ticket: {ticket.key}")
                repo_full_name = self.github.find_repository_for_ticket(ticket.key)
                
                if not repo_full_name:
                    print(f"    ! Repository not found for ticket {ticket.key}")
                    continue

                # Code Release Branching & Cherry-picking
                # Logic to find commits and cherry-pick would be more involved in a real scenario
                # Here we assume branch per ticket naming convention or similar.

            # Config Management Integration
            # For each release, if there are config changes...
            # This is where we call "The Config Crew"
            # self._handle_config_sync(release)

            # Notifier
            # self.notifier.send_release_report(...)

    def _handle_config_sync(self, release: ReleaseProject):
        # Simplified: Fetch files and call API
        payload = {
            "ticket_id": release.key,
            "config_test_content": "...", # Load from git
            "config_pre_current": "...", # Load from git
            "config_pro_current": "..."  # Load from git
        }
        response = requests.post(self.config_crew_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            # Commit result back to config repo
