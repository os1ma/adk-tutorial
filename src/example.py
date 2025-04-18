from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import asyncio


load_dotenv()

def get_weather(location: str) -> str:
    """Retrieves the current weather report for a specified location.

    Args:
        location (str): The name of the location for which to retrieve the weather report.

    Returns:
        str: weather report.
    """
    return f"The weather in {location} is sunny with a temperature of 25 degrees"

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the weather in a city."
    ),
    tools=[get_weather],
)

async def main() -> None:
    session_service = InMemorySessionService()

    APP_NAME = "weather_tutorial_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    content = types.Content(role='user', parts=[types.Part(text="What is the weather like in London?")])

    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            break

    print(final_response_text)

if __name__ == "__main__":
    asyncio.run(main())
