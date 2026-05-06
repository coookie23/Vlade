import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import video, audio, image, analyze
from utils import OUTPUT_DIR

app = FastAPI(title="Vlade API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/api/video", tags=["video"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])
app.include_router(image.router, prefix="/api/image", tags=["image"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])


@app.get("/api/download/{filename}")
async def download(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "File not found or expired")
    return FileResponse(path, filename=filename)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
