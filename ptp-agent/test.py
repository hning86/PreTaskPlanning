import asyncio
from agent import ptp_agent
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions.sqlite_session_service import SqliteSessionService

async def main():
    session_service = SqliteSessionService(db_path="agent_sessions.sqlite")
    runner = Runner(
        agent=ptp_agent,
        app_name="Mortenson_App",
        session_service=session_service,
        auto_create_session=True
    )
    content_msg = types.Content(role='user', parts=[types.Part.from_text(text="What are the upcoming high-risk tasks?")])
    
    print("Testing Runner.run_async...")
    try:
        async for event in runner.run_async(user_id="demo-user", session_id="test_session", new_message=content_msg):
            print("--- EVENT ---")
            if hasattr(event, "content") and event.content:
                print("CONTENT:", event.content)
            
            if hasattr(event, "get_function_calls"):
                calls = event.get_function_calls()
                if calls:
                    print("FUNCTION CALLS:", [f.name for f in calls])
                    
            if hasattr(event, "actions"):
                print("ACTIONS:", event.actions)
    except Exception as e:
        print("EXCEPTION:", str(e))

if __name__ == "__main__":
    asyncio.run(main())
