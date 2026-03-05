import os
import yaml
from crewai import Task

class ConfigTasks:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "../config/tasks.yaml")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def analyze_diff_task(self, agent, config_test_content) -> Task:
        task_config = self.config['analyze_diff_task'].copy()
        task_config['description'] = task_config['description'].format(config_test_content=config_test_content)
        return Task(
            config=task_config,
            agent=agent
        )

    def merge_config_task(self, agent, diff_report, config_pre_current, config_pro_current) -> Task:
        task_config = self.config['merge_config_task'].copy()
        task_config['description'] = task_config['description'].format(
            diff_report=diff_report,
            config_pre_current=config_pre_current,
            config_pro_current=config_pro_current
        )
        return Task(
            config=task_config,
            agent=agent
        )

    def validate_config_task(self, agent, config_pre_new, config_pro_new, config_pro_original) -> Task:
        task_config = self.config['validate_config_task'].copy()
        task_config['description'] = task_config['description'].format(
            config_pre_new=config_pre_new,
            config_pro_new=config_pro_new,
            config_pro_original=config_pro_original
        )
        return Task(
            config=task_config,
            agent=agent
        )
