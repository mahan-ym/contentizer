from fastapi import APIRouter
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from src.agent import root_agent
from src.runner import call_agent
from src.shared_state import SharedState

router = APIRouter()

_shared_state = SharedState()

# Initialize the Runner with the root agent
runner = Runner(
    agent=root_agent, app_name="contentizer", session_service=InMemorySessionService()
)


class PromptRequest(BaseModel):
    video_id: str
    time: str
    prompt: str


@router.post("/prompt")
async def get_agent_prompt(request: PromptRequest):
    try:
        # Execute the agent with async runtime
        response = await call_agent(
            query=request.prompt,
            runner=runner,
            user_id=request.video_id,  # Using video_id as user_id
            session_id=f"{request.video_id}_{request.time}",  # Creating unique session
        )

        return {
            "video_id": request.video_id,
            "time": request.time,
            "response": response,
            "generated_video_path": _shared_state.get_video_path(),
            "status": "success",
        }
    except Exception as e:
        print(f"Error processing agent prompt: {e}")
        return {
            "video_id": request.video_id,
            "time": request.time,
            "error": str(e),
            "status": "error",
        }
