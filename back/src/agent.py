from google.adk.agents import Agent
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from src.agents_instruction_prompt import (
    DIRECTOR_PROMPT,
    IMAGE_CREATOR_PROMPT,
    VIDEO_CREATOR_PROMPT,
)
from langfuse import get_client
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from src.tools.freepik import gen_vid, gen_image
from src.shared_state import SharedState

# Set shared state for tools
shared_state = SharedState()

# # Configure Langfuse client for production monitoring
# langfuse = get_client()
# # Verify connection
# if langfuse.auth_check():
#     print("Langfuse client is authenticated and ready!")
# else:
#     print("Authentication failed. Please check your credentials and host.")

# try:
#     GoogleADKInstrumentor().instrument()
#     print("Google ADK Instrumentation with Langfuse is set up successfully.")
# except Exception as e:
#     print(f"Failed to set up Google ADK Instrumentation: {e}")
#     print("Continuing without instrumentation.")

video_producer_agent = Agent(
    name="video_producer_agent",
    model="gemini-2.5-flash-lite",
    description=("Generates videos based on provided prompts and images."),
    instruction=VIDEO_CREATOR_PROMPT,
    tools=[gen_vid],
    output_key="video_output"
)

image_creator_agent = Agent(
    name="image_creator_agent",
    model="gemini-2.5-flash-lite",
    description=("Generates images based on provided prompts."),
    instruction=IMAGE_CREATOR_PROMPT,
    tools=[gen_image],
    output_key="image_output"
)

director_agent = LlmAgent(
    name="director_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "generate image based on the users prompt, "
        "then generate a video based on the users prompt"
    ),
    instruction=DIRECTOR_PROMPT,
    output_key="polished_prompt",
)

final_agent = SequentialAgent(
    name="director_agent",
    description=(
        "generate image based on the users prompt, "
        "then generate a video based on the users prompt"
    ),
    sub_agents=[
        director_agent,
        image_creator_agent,
        video_producer_agent,
    ],
)

root_agent = final_agent
