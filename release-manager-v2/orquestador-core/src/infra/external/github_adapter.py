import subprocess
import json
import os
from domain.interfaces.services import IGitHubService
from typing import Optional

class GitHubAdapter(IGitHubService):
    def find_repository_for_ticket(self, ticket_id: str) -> Optional[str]:
        """
        Search through accessible repos to find if a branch named after the ticket_id exists.
        Returns repo_name_with_owner if found, else None.
        """
        try:
            # Get all repos (limit 100 for performance, ideally narrower)
            result = subprocess.run(
                ["gh", "repo", "list", "--json", "nameWithOwner", "--limit", "100"],
                capture_output=True, text=True, check=True
            )
            repos = json.loads(result.stdout)
            
            for repo in repos:
                full_name = repo['nameWithOwner']
                # Check for branch containing ticket_id
                cmd = ["gh", "api", f"repos/{full_name}/branches", "--jq", f'.[] | select(.name | contains("{ticket_id}")) | .name']
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.stdout.strip():
                    return full_name
        except Exception as e:
            print(f"Error searching GitHub: {e}")
        return None

    def create_pull_request(self, repo: str, head: str, base: str, title: str, body: str) -> str:
        cmd = [
            "gh", "pr", "create",
            "--repo", repo,
            "--head", head,
            "--base", base,
            "--title", title,
            "--body", body
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def trigger_workflow(self, repo: str, workflow_id: str, ref: str, inputs: dict):
        # inputs must be a string for gh cli
        inputs_json = json.dumps(inputs)
        cmd = [
            "gh", "workflow", "run", workflow_id,
            "--repo", repo,
            "--ref", ref,
            "-f", f"json_inputs={inputs_json}" # Example of sending inputs
        ]
        subprocess.run(cmd, check=True)
