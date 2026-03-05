import unittest
import os
import yaml
from unittest.mock import MagicMock
from agents.config_agents import ConfigAgents
from tasks.config_tasks import ConfigTasks

from crewai import Agent
from unittest.mock import MagicMock

class TestConfigLoading(unittest.TestCase):
    def test_agents_yaml_loading(self):
        agents = ConfigAgents()
        self.assertIn('senior_diff_analyzer', agents.config)
        self.assertIn('environment_specialist', agents.config)
        self.assertIn('qa_validator', agents.config)

    def test_tasks_yaml_loading(self):
        tasks = ConfigTasks()
        self.assertIn('analyze_diff_task', tasks.config)
        self.assertIn('merge_config_task', tasks.config)
        self.assertIn('validate_config_task', tasks.config)

    def test_agent_creation_from_yaml(self):
        agents = ConfigAgents()
        analyzer = agents.senior_diff_analyzer()
        self.assertEqual(analyzer.role.strip(), "Senior Diff Analyzer")
        self.assertFalse(analyzer.allow_delegation)

    def test_task_formatting_logic(self):
        tasks = ConfigTasks()
        # Use a real Agent instead of MagicMock to avoid Pydantic validation errors
        agent = Agent(role="Test", goal="Test", backstory="Test")
        task = tasks.analyze_diff_task(agent, "SAMPLE_TEST_CONTENT")
        self.assertIn("SAMPLE_TEST_CONTENT", task.description)
