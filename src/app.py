from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

from tools.content_creator import look_for_youtube_trends


prompt_inspector_agent = Agent(
    name="Prompt Inspector Agent",
    description="Inspects and reviews the input prompt.",
    model="gemini-2.5-flash-lite",
    instructions="""You are a creative and professional content creator.""",
    tools=[look_for_youtube_trends],
)

# gather_images_agent = Agent(
#     name="Gather Images Agent",

# )

# generate_video_agent = Agent(
#     name="Generate Video Agent",
# )


# creation_refinement_loop = LoopAgent(
#     name="Creation and Refinement Loop",
#     sub_agents= [ gather_images_agent, generate_video_agent ],
# )
