# backend/server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
from agent.core import graph

app = FastAPI(title="Browser Sidekick API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage (in production, use Redis or database)
sessions = {}

class ChatRequest(BaseModel):
    message: str
    context: dict
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    try:
        # Create or retrieve session
        if not request.session_id or request.session_id not in sessions:
            session_id = str(uuid.uuid4())
            sessions[session_id] = {
                "created_at": datetime.now(),
                "messages": []
            }
        else:
            session_id = request.session_id
        
        # Prepare context message
        context_message = f"""
        Current Page Context:
        - URL: {request.context.get('url', 'Unknown')}
        - Title: {request.context.get('title', 'Unknown')}
        - Selected Text: {request.context.get('selected_text', 'None')}
        - Content Preview: {request.context.get('content', '')[:500]}...
        
        User Question: {request.message}
        """
        
        # Run the agent
        result = graph.invoke({
            "messages": [{"role": "user", "content": context_message}],
            "current_page_content": request.context.get('content', ''),
            "browser_context": request.context
        })
        
        # Extract the final response
        final_response = None
        for msg in result["messages"]:
            if hasattr(msg, 'content') and msg.content:
                final_response = msg.content
                break
        
        if not final_response:
            final_response = "I apologize, but I couldn't generate a proper response."
        
        # Store in session
        sessions[session_id]["messages"].append({
            "user_message": request.message,
            "agent_response": final_response,
            "timestamp": datetime.now()
        })
        
        return ChatResponse(
            response=final_response,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)