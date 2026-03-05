import os
from git import Repo, GitCommandError
from domain.interfaces.services import IGitHandler

class GitAdapter(IGitHandler):
    def __init__(self, workspace_path="/tmp/release_manager_repos"):
        self.workspace = workspace_path
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)
        self.current_repo = None

    def clone_and_checkout(self, repo_url: str, branch: str):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(self.workspace, repo_name)
        
        if os.path.exists(repo_path):
            self.current_repo = Repo(repo_path)
            self.current_repo.remotes.origin.pull()
        else:
            self.current_repo = Repo.clone_from(repo_url, repo_path)
        
        self.current_repo.git.checkout(branch)

    def cherry_pick(self, commit_hash: str) -> bool:
        if not self.current_repo:
            return False
        try:
            self.current_repo.git.cherry_pick(commit_hash)
            return True
        except GitCommandError:
            self.current_repo.git.cherry_pick("--abort")
            return False

    def push(self, branch: str):
        if self.current_repo:
            self.current_repo.remotes.origin.push(branch)
            
    def create_branch(self, branch_name: str, base: str = "main"):
        self.current_repo.git.checkout(base)
        new_branch = self.current_repo.create_head(branch_name)
        new_branch.checkout()
