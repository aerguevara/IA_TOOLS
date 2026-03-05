import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Crew, Process
from agents.config_agents import ConfigAgents
from tasks.config_tasks import ConfigTasks

load_dotenv()

app = FastAPI(title="The Config Crew API", version="1.0.0")

class ConfigMergeRequest(BaseModel):
    ticket_id: str
    config_test_content: str
    config_pre_current: str
    config_pro_current: str

class ConfigMergeResponse(BaseModel):
    status: str
    config_pre_new: str
    config_pro_new: str
    reasoning: str

@app.post("/api/v1/config/merge", response_model=ConfigMergeResponse)
async def merge_config(request: ConfigMergeRequest):
    agents = ConfigAgents()
    tasks = ConfigTasks()

    # Initialize Agents
    analyzer = agents.senior_diff_analyzer()
    specialist = agents.environment_specialist()
    validator = agents.qa_validator()

    # Define Tasks
    t1 = tasks.analyze_diff_task(analyzer, request.config_test_content)
    t2 = tasks.merge_config_task(specialist, "See previous task output", request.config_pre_current, request.config_pro_current)
    t3 = tasks.validate_config_task(validator, "See output from t2 for pre", "See output from t2 for pro", request.config_pro_current)

    # Note: Sequential process is required
    crew = Crew(
        agents=[analyzer, specialist, validator],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    # Here we would normally parse the result from the validator agent
    # for simplicity in this initial implementation, we assume the result is a JSON string
    return {
        "status": "success",
        "config_pre_new": "...", # Extracted from result
        "config_pro_new": "...", # Extracted from result
        "reasoning": str(result)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
