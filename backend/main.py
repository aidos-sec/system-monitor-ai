"""Backend: стриминг метрик по WebSocket + эндпоинт прогноза."""
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from metrics import metrics_stream
from predictor import predictor

app = FastAPI(title="System Monitor with AI Predictions")

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get("/api/predict")
def predict():
    return predictor.predict()

@app.websocket("/ws/metrics")
async def ws_metrics(websocket: WebSocket):
    await websocket.accept()
    try:
        async for m in metrics_stream(interval=1.0):
            predictor.add(m["timestamp"], m["cpu"])
            if int(m["timestamp"]) % 10 == 0:
                m["prediction"] = predictor.predict()
            await websocket.send_text(json.dumps(m))
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
