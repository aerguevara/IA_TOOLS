from dataclasses import dataclass
from typing import List, Optional

@dataclass
class JiraTicket:
    key: str
    status: str
    summary: str

@dataclass
class ReleaseProject:
    key: str
    version: str
    status: str
    child_tickets: List[JiraTicket] = None

@dataclass
class GitCommit:
    hash: str
    message: str
    author: str

@dataclass
class ReleaseReport:
    release_id: str
    successful_tickets: List[str]
    failed_tickets: List[dict]
    pr_links: List[str]
