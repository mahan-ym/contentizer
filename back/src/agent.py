from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from src.agents_instruction_prompt import DIRECTOR_PROMPT, IMAGE_CREATOR_PROMPT, VIDEO_CREATOR_PROMPT


from src.tools.content_creator import (
    look_for_youtube_trends,
    get_youtube_video_categories,
)

from src.tools.freepik import gen_vid, gen_image

prompt_inspector_agent = Agent(
    name="prompt_inspector_agent",
    model="gemini-2.5-flash-lite",
    description=("Inspects and reviews the input prompt."),
    instruction=("You are a creative and professional content creator."),
    tools=[look_for_youtube_trends, get_youtube_video_categories],
)

video_producer_agent = Agent(
    name="video_producer_agent",
    model="gemini-2.5-flash-lite",
    description=("Generates videos based on provided prompts and images."),
    instruction= VIDEO_CREATOR_PROMPT,
    tools=[gen_vid],
)

image_creator_agent = Agent(
    name="image_creator_agent",
    model="gemini-2.5-flash-lite",
    description=("Generates images based on provided prompts."),
    instruction= IMAGE_CREATOR_PROMPT,
    tools=[gen_image],
)

director_agent = LlmAgent(
    name="director_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "generate image based on the users prompt, "
        "then generate a video based on the users prompt and the generated image"
    ),
    instruction=DIRECTOR_PROMPT,
    tools=[
        AgentTool(agent=image_creator_agent),
        AgentTool(agent=video_producer_agent),
    ],
)

root_agent = director_agent
