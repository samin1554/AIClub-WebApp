from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket import ws_manager

router = APIRouter()

@router.websocket("/ws/{board_id}")
async def websocket_endpoint(websocket: WebSocket, board_id: str):
    await ws_manager.connect(websocket, board_id)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast(board_id, {
                "type": "stroke",
                "data": data
            })
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, board_id)