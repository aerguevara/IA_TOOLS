import os
import yaml
from crewai import Agent

class ConfigAgents:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "../config/agents.yaml")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def senior_diff_analyzer(self) -> Agent:
        return Agent(
            config=self.config['senior_diff_analyzer'],
            allow_delegation=False,
            verbose=True
        )

    def environment_specialist(self) -> Agent:
        return Agent(
            config=self.config['environment_specialist'],
            allow_delegation=False,
            verbose=True
        )

    def qa_validator(self) -> Agent:
        return Agent(
            config=self.config['qa_validator'],
            allow_delegation=False,
            verbose=True
        )
