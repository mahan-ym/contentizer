from google.adk.agents import Agent

from src.tools.content_creator import (
    look_for_youtube_trends,
    get_youtube_video_categories,
)

from src.tools.freepik import gen_vid

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
    instruction=(
        "You are an expert video producer you take an image and transform it into a video by listening to the prompts and negative prompts."
    ),
    tools=[gen_vid],
)

# main_agent = LoopAgent(
#     name="main_agent",
#     sub_agents=[
#         prompt_inspector_agent,
#     ],
# )


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

root_agent = video_producer_agent
