from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.bigq_agent import bigq_agent
from .sub_agents.vsearch_agent import vsearch_agent

MODEL = "gemini-2.5-pro-preview-05-06"


academic_coordinator = LlmAgent(
    name="academic_coordinator",
    model=MODEL,
    description=prompt.MODEL_DESCRIPTION,
    instruction=prompt.COORDINATOR_PROMPT,
    
    tools=[
        AgentTool(agent=vsearch_agent),
        AgentTool(agent=bigq_agent),
    ],
)

root_agent = academic_coordinator