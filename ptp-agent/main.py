import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from agent import ptp_agent

from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.adk.runners import Runner

app = FastAPI(title="Google Data Center PTP Agent Engine Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = SqliteSessionService(db_path="agent_sessions.sqlite")
runner = Runner(
    agent=ptp_agent,
    app_name="Mortenson_App",
    session_service=session_service,
    auto_create_session=True
)

@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    Accepts JSON with "message" and "session_id".
    Streams SSE responses compatible with Vertex AI Agent Engine.
    """
    body = await request.json()
    message = body.get("message", "")
    session_id = body.get("session_id", "default_session")

    async def generate():
        from google.genai import types
        try:
            content_msg = types.Content(role='user', parts=[types.Part.from_text(text=message)])
            async for event in runner.run_async(user_id="demo-user", session_id=session_id, new_message=content_msg):
                # Extract model text responses
                if hasattr(event, "content") and event.content and hasattr(event.content, "parts"):
                    for part in event.content.parts:
                        if getattr(part, "text", None):
                            payload = {"text": part.text}
                            yield f"data: {json.dumps(payload)}\n\n"
                            
                # Extract tool execution traces 
                if hasattr(event, "get_function_calls"):
                    calls = event.get_function_calls()
                    if calls:
                        tc_names = [call.name for call in calls]
                        payload = {"tool_calls": tc_names}
                        yield f"data: {json.dumps(payload)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
