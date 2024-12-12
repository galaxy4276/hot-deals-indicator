from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from elasticsearch import Elasticsearch
import json
import os
import asyncio
import uuid

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

es = Elasticsearch(["http://han-box.co.kr:9200"], basic_auth=("id", "password"))

user_sessions = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start-monitoring")
async def start_monitoring(request: Request):
    form_data = await request.form()
    email = form_data.get("email")
    
    session_id = str(uuid.uuid4())
    user_sessions[session_id] = {
        "email": email
    }
    
    return RedirectResponse(url=f"/results/{session_id}", status_code=303)

@app.get("/results/{session_id}")
async def get_results(request: Request, session_id: str):
    if session_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    user_data = user_sessions[session_id]
    return templates.TemplateResponse("results.html", {
        "request": request,
        "session_id": session_id,
        "email": user_data["email"]
    })

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    if session_id not in user_sessions:
        await websocket.close(code=1000)
        return
    
    await manager.connect(websocket, session_id)
    try:
        asyncio.create_task(monitor_elasticsearch(session_id))
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(session_id)

async def monitor_elasticsearch(client_id):
    while True:
        query = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {"dateCreated": "desc"}
            ],
            "size": 10
        }
        
        results = es.search(index="hot_deals", body=query)

        if results["hits"]["total"]["value"] > 0:
            matching_products = []

            for hit in results["hits"]["hits"]:
                product = hit["_source"]
                matching_products.append({
                    "name": product.get("name", "N/A"),
                    "price": product.get("price", "N/A"),
                    "link": product.get("link", "N/A")
                })
            await manager.send_personal_message(json.dumps(matching_products), client_id)
        await asyncio.sleep(10)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)