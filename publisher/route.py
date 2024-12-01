from fastapi import FastAPI
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uuid
import asyncio
from websocket_manager import manager
from observer import elasticsearch_observer
from contextlib import asynccontextmanager


router = APIRouter()
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

user_sessions = {}

@router.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/start-monitoring")
async def start_monitoring(request: Request):
    form_data = await request.form()
    email = form_data.get("email")
    product_name = form_data.get("product_name")
    
    try:
        max_price = int(form_data.get("max_price", "0"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid max price value")
    
    session_id = str(uuid.uuid4())
    user_data = {
        "email": email,
        "product_name": product_name,
        "max_price": max_price  
    }
    user_sessions[session_id] = user_data
    elasticsearch_observer.register(session_id, user_data)
    
    return RedirectResponse(url=f"/results/{session_id}", status_code=303)


@router.get("/results/{session_id}")
async def get_results(request: Request, session_id: str):
    if session_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    user_data = user_sessions[session_id]
    return templates.TemplateResponse("results.html", {
        "request": request,
        "session_id": session_id,
        "email": user_data["email"],
        "max_price": user_data["max_price"]
    })


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    if session_id not in user_sessions:
        await websocket.close(code=1000)
        return
    
    await manager.connect(websocket, session_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        elasticsearch_observer.unregister(session_id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    observer_task = asyncio.create_task(elasticsearch_observer.notify())
    yield
    observer_task.cancel()
    try:
        await observer_task
    except asyncio.CancelledError:
        pass