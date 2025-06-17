from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

#MODEL = "gemini-2.5-pro-preview-05-06"
MODEL = "gemini-2.0-flash-001"

bigq_agent = Agent(
    model=MODEL,
    name="bigq_agent",
    description= prompt.MODEL_DESCRIPTION,
    instruction=prompt.BIGQ_PROMPT,
    tools=[google_search],
)