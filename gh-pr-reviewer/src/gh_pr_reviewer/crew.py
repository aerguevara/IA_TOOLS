import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_ollama import ChatOllama

# Usar el modelo local Ollama
os.environ["OPENAI_API_KEY"] = "NA"

@CrewBase
class GhPrReviewerCrew():
    """GhPrReviewer crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # Se usa el formato de string con prefijo para asegurar compatibilidad con LiteLLM interno de CrewAI
        self.llm = "ollama/deepseek-coder-v2:16b"

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reviewer'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def review_and_merge_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_and_merge_task'],
            agent=self.code_reviewer()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GhPrReviewer crew"""
        return Crew(
            agents=self.agents, # Automáticamente proveído por @agent
            tasks=self.tasks, # Automáticamente proveído por @task
            process=Process.sequential,
            verbose=True,
        )
