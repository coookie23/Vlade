import uuid
import threading
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.ffmpeg import (
    compress_video, convert_video, trim_video, merge_videos,
    extract_audio, add_subtitle, video_to_gif,
    rife_interpolate, douyin_optimize,
)
from utils import save_upload, output_filename, task_read, task_cleanup, task_start

router = APIRouter()


def run_async(fn, *args):
    """Run a function in a background daemon thread."""
    t = threading.Thread(target=fn, args=args, daemon=True)
    t.start()


# ── Progress endpoint ──

@router.get("/progress/{task_id}")
async def get_progress(task_id: str):
    data = task_read(task_id)
    if data is None:
        raise HTTPException(404, "任务不存在")
    return data


# ── RIFE (with progress) ──

@router.post("/rife-interpolate")
async def api_rife(file: UploadFile = File(...), fps: int = Form(60), mode: str = Form("平衡")):
    path = await save_upload(file)
    out, name = output_filename(".mp4")
    task_id = uuid.uuid4().hex
    task_start(task_id, 0, f"智能补帧 {fps}fps")  # placeholder, real dur set in thread
    run_async(rife_interpolate, task_id, path, out, fps, mode)
    return {"task_id": task_id, "filename": name, "download_url": f"/api/download/{name}"}


# ── Douyin ──

@router.post("/douyin-optimize")
async def api_douyin(file: UploadFile = File(...)):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if "." in (file.filename or "") else "mp4"
    out, name = output_filename(f".{ext}")
    try:
        douyin_optimize(path, out)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


# ── Standard tools ──

@router.post("/compress")
async def api_compress(file: UploadFile = File(...), crf: int = Form(28)):
    path = await save_upload(file)
    out, name = output_filename(".mp4")
    try:
        compress_video(path, out, crf=crf)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/convert")
async def api_convert(file: UploadFile = File(...), fmt: str = Form("mp4")):
    path = await save_upload(file)
    out, name = output_filename(f".{fmt}")
    try:
        convert_video(path, out, fmt=fmt)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/trim")
async def api_trim(file: UploadFile = File(...), start: float = Form(...), duration: float = Form(...)):
    path = await save_upload(file)
    out, name = output_filename(".mp4")
    try:
        trim_video(path, out, start, duration)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/merge")
async def api_merge(files: list[UploadFile] = File(...)):
    paths = []
    for f in files:
        paths.append(await save_upload(f))
    out, name = output_filename(".mp4")
    try:
        merge_videos(paths, out)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/extract-audio")
async def api_extract_audio(file: UploadFile = File(...), fmt: str = Form("mp3")):
    path = await save_upload(file)
    out, name = output_filename(f".{fmt}")
    try:
        extract_audio(path, out, fmt=fmt)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/subtitle")
async def api_subtitle(file: UploadFile = File(...), subtitle: UploadFile = File(...)):
    vid_path = await save_upload(file)
    sub_path = await save_upload(subtitle)
    out, name = output_filename(".mp4")
    try:
        add_subtitle(vid_path, out, sub_path)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/to-gif")
async def api_to_gif(file: UploadFile = File(...), fps: int = Form(10), width: int = Form(320)):
    path = await save_upload(file)
    out, name = output_filename(".gif")
    try:
        video_to_gif(path, out, fps=fps, width=width)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}
