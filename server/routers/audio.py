from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.ffmpeg import (
    compress_audio, convert_audio, trim_audio, merge_audios,
    change_volume, denoise_audio,
)
from utils import save_upload, output_filename

router = APIRouter()


@router.post("/compress")
async def api_compress(file: UploadFile = File(...), bitrate: str = Form("128k")):
    path = await save_upload(file)
    out, name = output_filename(".mp3")
    try:
        compress_audio(path, out, bitrate=bitrate)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/convert")
async def api_convert(file: UploadFile = File(...), fmt: str = Form("mp3")):
    path = await save_upload(file)
    out, name = output_filename(f".{fmt}")
    try:
        convert_audio(path, out, fmt=fmt)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/trim")
async def api_trim(file: UploadFile = File(...),
                   start: float = Form(...), duration: float = Form(...)):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if file.filename and "." in file.filename else "mp3"
    out, name = output_filename(f".{ext}")
    try:
        trim_audio(path, out, start, duration)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/merge")
async def api_merge(files: list[UploadFile] = File(...)):
    paths = [await save_upload(f) for f in files]
    out, name = output_filename(".mp3")
    try:
        merge_audios(paths, out)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/volume")
async def api_volume(file: UploadFile = File(...), factor: float = Form(1.5)):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if file.filename and "." in file.filename else "mp3"
    out, name = output_filename(f".{ext}")
    try:
        change_volume(path, out, factor=factor)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/denoise")
async def api_denoise(file: UploadFile = File(...)):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if file.filename and "." in file.filename else "mp3"
    out, name = output_filename(f".{ext}")
    try:
        denoise_audio(path, out)
    except Exception as e:
        raise HTTPException(500, f"FFmpeg error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}
