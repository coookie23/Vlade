import os
import uuid
import threading
import time
import aiofiles
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Progress store ──
_progress: dict[str, dict] = {}
_lock = threading.Lock()


def task_start(task_id: str, duration: float, label: str = "处理中"):
    """Register a new task and begin tracking."""
    with _lock:
        _progress[task_id] = {
            "label": label,
            "duration": duration,
            "percent": 0.0,
            "speed": 0.0,
            "done": False,
            "error": None,
        }


def task_progress(task_id: str, percent: float, speed: float = 0.0):
    with _lock:
        if task_id in _progress:
            _progress[task_id]["percent"] = min(percent, 99.0)
            _progress[task_id]["speed"] = speed


def task_done(task_id: str):
    with _lock:
        if task_id in _progress:
            _progress[task_id]["percent"] = 100.0
            _progress[task_id]["done"] = True


def task_error(task_id: str, msg: str):
    with _lock:
        if task_id in _progress:
            _progress[task_id]["error"] = msg
            _progress[task_id]["done"] = True


def task_read(task_id: str) -> dict | None:
    with _lock:
        return _progress.get(task_id)


def task_cleanup(task_id: str):
    with _lock:
        _progress.pop(task_id, None)


async def save_upload(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename or "file")[1] or ".bin"
    name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, name)
    async with aiofiles.open(path, "wb") as f:
        content = await file.read()
        await f.write(content)
    return path


def output_filename(ext: str) -> tuple:
    name = f"{uuid.uuid4().hex}{ext}"
    return os.path.join(OUTPUT_DIR, name), name
