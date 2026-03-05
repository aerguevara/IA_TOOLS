from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.release_entities import JiraTicket, ReleaseProject

class IJiraService(ABC):
    @abstractmethod
    def get_release_tickets(self, status: str) -> List[ReleaseProject]:
        pass

    @abstractmethod
    def get_completed_child_tickets(self, parent_key: str) -> List[JiraTicket]:
        pass

class IGitHubService(ABC):
    @abstractmethod
    def find_repository_for_ticket(self, ticket_id: str) -> Optional[str]:
        pass

    @abstractmethod
    def create_pull_request(self, repo: str, head: str, base: str, title: str, body: str) -> str:
        pass

    @abstractmethod
    def trigger_workflow(self, repo: str, workflow_id: str, ref: str, inputs: dict):
        pass

class IGitHandler(ABC):
    @abstractmethod
    def clone_and_checkout(self, repo_url: str, branch: str):
        pass

    @abstractmethod
    def cherry_pick(self, commit_hash: str) -> bool:
        pass

    @abstractmethod
    def push(self, branch: str):
        pass

class INotificationService(ABC):
    @abstractmethod
    def send_release_report(self, recipients: List[str], report_data: dict):
        pass
