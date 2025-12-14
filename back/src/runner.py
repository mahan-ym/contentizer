from google.genai import types


async def call_agent(query: str, runner, user_id: str, session_id: str):
    print(f"Received query: {query}")

    # Ensure session exists before running agent
    session = await runner.session_service.get_session(
        app_name=runner.app_name, user_id=user_id, session_id=session_id
    )

    if session is None:
        # Session doesn't exist, create it
        await runner.session_service.create_session(
            app_name=runner.app_name, user_id=user_id, session_id=session_id
        )

    # Prepare the user's message in ADK format
    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default
    video_output_ready = False

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        print(
            f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}"
        )

        if event.is_final_response():
            print(f"  [DEBUG] Final response event details:")
            print(f"    - event.author: {event.author}")
            print(f"    - event.content: {event.content}")
            print(f"    - event.content type: {type(event.content)}")
            if event.content:
                print(f"    - event.content.parts: {event.content.parts}")
                print(
                    f"    - event.content.parts type: {type(event.content.parts) if event.content.parts is not None else 'None'}"
                )

            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif (
                event.actions and event.actions.escalate
            ):  # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            else:
                # Handle case where content.parts is None or empty
                print(
                    f"  [DEBUG] No text parts in final response, checking for other content"
                )
                if event.content:
                    final_response_text = f"Response received but contains no text content: {event.content}"
                else:
                    final_response_text = "Agent completed but returned no content"

            # Check if this is from video_producer_agent (the final agent we need)
            if event.author == "video_producer_agent":
                print(f"  [DEBUG] Video output is ready from video_producer_agent")
                video_output_ready = True
                break  # Stop processing only when video_producer_agent completes
            else:
                print(
                    f"  [DEBUG] Final response from {event.author}, continuing to wait for video_output..."
                )

    return final_response_text
