from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import json
import uuid
import asyncio
from database import search_products
from websocket_manager import manager

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
    max_price = form_data.get("max_price")
    
    session_id = str(uuid.uuid4())
    user_sessions[session_id] = {
        "email": email,
        "product_name": product_name,
        "max_price": max_price
    }
    
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
        user_data = user_sessions[session_id]
        asyncio.create_task(monitor_elasticsearch(user_data, session_id))
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(session_id)

async def monitor_elasticsearch(user_data, client_id):
    while True:
        results = await search_products(user_data["product_name"], user_data["max_price"])
        if results["hits"]["total"]["value"] > 0:
            matching_products = [
                {
                    "name": hit["_source"]["name"],
                    "price": hit["_source"]["price"],
                    "link": hit["_source"]["link"]
                }
                for hit in results["hits"]["hits"]
            ]
            await manager.send_personal_message(json.dumps(matching_products), client_id)
        await asyncio.sleep(10)