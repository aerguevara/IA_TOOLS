import os
from git import Repo, GitCommandError

class GitHandler:
    def __init__(self, workspace_path="/tmp/release_manager_repos"):
        self.workspace = workspace_path
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)

    def clone_or_pull(self, repo_url, repo_name):
        repo_path = os.path.join(self.workspace, repo_name)
        if os.path.exists(repo_path):
            repo = Repo(repo_path)
            repo.remotes.origin.pull()
        else:
            repo = Repo.clone_from(repo_url, repo_path)
        return repo

    def prepare_release_branch(self, repo, release_id, base_branch="main"):
        new_branch_name = f"release/v{release_id}"
        repo.git.checkout(base_branch)
        
        # Create and checkout new branch
        if new_branch_name in repo.branches:
            repo.git.branch("-D", new_branch_name)
        
        new_branch = repo.create_head(new_branch_name)
        new_branch.checkout()
        return new_branch_name

    def cherry_pick_commits(self, repo, jira_id):
        """
        Find commits containing the Jira ID in their message and cherry-pick them.
        Assumes we are already on the release branch.
        """
        # Search for commits in 'development' or other branches that are not yet in main
        # For simplicity, we search in all branches or a specific one like 'develop'
        try:
            commits = list(repo.iter_commits('develop', grep=jira_id))
            if not commits:
                return False, f"No commits found for {jira_id}"
            
            # Cherry-pick in reverse order (oldest first)
            for commit in reversed(commits):
                repo.git.cherry_pick(commit.hexsha)
            
            return True, f"Successfully cherry-picked {len(commits)} commits for {jira_id}"
        except GitCommandError as e:
            # Conflict handling
            repo.git.cherry_pick("--abort")
            return False, str(e)

    def push_branch(self, repo, branch_name):
        repo.remotes.origin.push(branch_name)
