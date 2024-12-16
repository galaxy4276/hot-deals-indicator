from fastapi import FastAPI, APIRouter, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uuid
import asyncio
from contextlib import asynccontextmanager
from websocket_manager import WebSocketNotificationService
from observer import ElasticsearchObserver
from search_query import ElasticsearchProductSearchService
from interfaces import MonitoringLogger
from settings import AppSettings

router = APIRouter()
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

settings = AppSettings()
search_service = ElasticsearchProductSearchService(settings)
notification_service = WebSocketNotificationService()
monitoring_logger = MonitoringLogger()
elasticsearch_observer = ElasticsearchObserver(
    search_service,
    notification_service,
    monitoring_logger,
    settings
)

class UserSessionManager:
    def __init__(self):
        self.user_sessions = {}

    def create_session(self, email: str, product_name: str, category: str,max_price: int) -> str:
        session_id = str(uuid.uuid4())
        self.user_sessions[session_id] = {
            "email": email,
            "product_name": product_name,
            "category" : category,
            "max_price": max_price
        }
        return session_id

    def get_session(self, session_id: str) -> dict:
        return self.user_sessions.get(session_id)

    def delete_session(self, session_id: str):
        if session_id in self.user_sessions:
            del self.user_sessions[session_id]

user_session_manager = UserSessionManager()

@router.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/start-monitoring")
async def start_monitoring(request: Request):
    form_data = await request.form()
    email = form_data.get("email")
    product_name = form_data.get("product_name")
    category = form_data.get("category")

    try:
        max_price = int(form_data.get("max_price", "0"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid max price value")
    
    session_id = user_session_manager.create_session(email, product_name, category,max_price)
    user_data = user_session_manager.get_session(session_id)
    elasticsearch_observer.register(session_id, user_data)
    
    return RedirectResponse(url=f"/results/{session_id}", status_code=303)

@router.get("/results/{session_id}")
async def get_results(request: Request, session_id: str):
    user_data = user_session_manager.get_session(session_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "session_id": session_id,
        "email": user_data["email"],
        "product_name": user_data["product_name"],
        "category": user_data["category"],
        "max_price": user_data["max_price"]
    })

@router.get("/get_session/{session_id}")
async def get_session(session_id: str):
    session = user_session_manager.get_session(session_id)
    if session:
        return session
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@router.delete("/delete_session/{session_id}")
async def delete_session(session_id: str):
    user_session_manager.delete_session(session_id)
    elasticsearch_observer.unregister(session_id)
    return {"detail": "Session deleted"}

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    user_data = user_session_manager.get_session(session_id)
    if not user_data:
        await websocket.close(code=1000)
        return
    
    await notification_service.connect(websocket, session_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_service.disconnect(session_id)
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
