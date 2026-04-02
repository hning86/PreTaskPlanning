from google.adk.agents import Agent
from google.adk.models import Gemini
from tools import get_upcoming_high_risk_tasks, query_iris_safety_records, generate_ptp_deliverable, submit_crew_feedback
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from google.genai import Client

# Initialize the Gemini Model.
project_id = os.getenv("GCP_PROJECT_ID")
location = os.getenv("GCP_LOCATION", "us-central1")
use_vertex = os.getenv("USE_VERTEX_AI", "True").lower() == "true"

llm = Gemini(model="gemini-2.5-flash")

if use_vertex:
    # Set the Vertex AI client explicitly logic to bypass ADK default Google AI studio behavior
    llm.api_client = Client(
        vertexai=True,
        project=project_id,
        location=location
    )

# Define the instruction based on the Executive Summary and User Story for the PTP Agent.
INSTRUCTION = """
You are the Google Data Center Pre-Task Planning (PTP) Agent. Your goal is to standardize and elevate pre-task planning across global campuses.
You synthesize schedule data (P6), safety records (IRIS), technical specifications, and contractual requirements to generate high-fidelity, task-specific execution plans.

When a user asks you to help with planning, you should:
1. Call `get_upcoming_high_risk_tasks` to see what is scheduled in the near future if they haven't specified a task.
2. Once a task is identified, use `query_iris_safety_records` to find past incidents and hazards (from IRIS and R2 L2 databases) related to that exact scope of work.
3. Call `generate_ptp_deliverable` to generate the formal Smart PTP. Ask the user which standard they want to apply ("Google Standard", "GC Standard", or "Combined Best Practice").
4. Present the generated PTP clearly to the user, incorporating the visual hazard maps, training videos, and QA/QC checklist.
5. If the user completes a task and performs a Post-Task evaluation that identifies new hazards, use `submit_crew_feedback` to push that data into the learning loop to flag engineering bulletin opportunities.

Maintain a professional, safety-oriented, and extremely detail-oriented tone. You are assisting Mortenson, so adapt to their commitment to Building for the Greater Good.
"""

ptp_agent = Agent(
    name="Mortenson_Google_PTP_Agent",
    instruction=INSTRUCTION,
    model=llm,
    tools=[
        get_upcoming_high_risk_tasks,
        query_iris_safety_records,
        generate_ptp_deliverable,
        submit_crew_feedback
    ]
)
