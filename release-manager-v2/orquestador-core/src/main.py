import typer
from dotenv import load_dotenv
from domain.use_cases.prepare_release import PrepareReleaseUseCase
from infra.external.jira_adapter import JiraAdapter
from infra.external.github_adapter import GitHubAdapter
from infra.external.git_adapter import GitAdapter
from infra.external.notification_adapter import EmailNotificationAdapter

load_dotenv()

app = typer.Typer()

@app.command()
def run_release(status: str = "Ready for PRE"):
    """
    Run the release orchestration process.
    """
    # Dependency Injection
    jira = JiraAdapter()
    github = GitHubAdapter()
    git = GitAdapter()
    notifier = EmailNotificationAdapter()
    
    use_case = PrepareReleaseUseCase(jira, github, git, notifier)
    use_case.execute(status)

if __name__ == "__main__":
    app()
