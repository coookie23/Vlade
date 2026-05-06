from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.image import (
    compress_image, convert_image, crop_image, resize_image, add_watermark,
)
from utils import save_upload, output_filename

router = APIRouter()


@router.post("/compress")
async def api_compress(file: UploadFile = File(...), quality: int = Form(75)):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if file.filename else "jpg"
    out, name = output_filename(f".{ext}")
    try:
        compress_image(path, out, quality=quality)
    except Exception as e:
        raise HTTPException(500, f"Image error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/convert")
async def api_convert(file: UploadFile = File(...), fmt: str = Form("png")):
    path = await save_upload(file)
    out, name = output_filename(f".{fmt}")
    try:
        convert_image(path, out, fmt=fmt)
    except Exception as e:
        raise HTTPException(500, f"Image error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/crop")
async def api_crop(file: UploadFile = File(...),
                   x: int = Form(...), y: int = Form(...),
                   w: int = Form(...), h: int = Form(...)):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if file.filename else "png"
    out, name = output_filename(f".{ext}")
    try:
        crop_image(path, out, x, y, w, h)
    except Exception as e:
        raise HTTPException(500, f"Image error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/resize")
async def api_resize(file: UploadFile = File(...),
                     width: int = Form(0), height: int = Form(0)):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if file.filename else "png"
    out, name = output_filename(f".{ext}")
    try:
        resize_image(path, out, width=width, height=height)
    except Exception as e:
        raise HTTPException(500, f"Image error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}


@router.post("/watermark")
async def api_watermark(file: UploadFile = File(...), text: str = Form("")):
    path = await save_upload(file)
    ext = file.filename.rsplit(".", 1)[-1] if file.filename else "png"
    out, name = output_filename(f".{ext}")
    try:
        add_watermark(path, out, text=text)
    except Exception as e:
        raise HTTPException(500, f"Image error: {str(e)}")
    return {"filename": name, "download_url": f"/api/download/{name}"}
