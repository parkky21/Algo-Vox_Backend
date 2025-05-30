from fastapi import FastAPI,Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import agents, vector_stores
from app.api.routes.websockets import agent_ws
from app.api.dependencies import validate_ws_token
from app.utils.mongodb_client import MongoDBClient
from app.api.routes import telephony

app = FastAPI(
    title="Algo Vox API",
    description="Voice agent system with vector search integration",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def protected_agent_ws(
    websocket: WebSocket, 
    agent_id: str = Depends(validate_ws_token)
):
    if not agent_id:  # If None, connection was already closed
        return
    
    return await agent_ws(websocket, agent_id)


app.include_router(vector_stores.router, prefix="/vector_stores", tags=["Vector Stores"])
app.include_router(agents.router, prefix="/v1", tags=["Agent"])
app.add_api_websocket_route("/ws/agent/{agent_id}", protected_agent_ws)
app.include_router(telephony.router, prefix="/telephony", tags=["Telephony"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
