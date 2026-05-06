import os
from pathlib import Path

import ffmpeg
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image

from utils import save_upload

router = APIRouter()

VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv", ".m4v", ".3gp", ".ts"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".bmp"}
AUDIO_EXTS = {".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"}


def _safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _kind_from_ext(ext: str) -> str:
    ext = ext.lower()
    if ext in VIDEO_EXTS:
        return "video"
    if ext in IMAGE_EXTS:
        return "image"
    if ext in AUDIO_EXTS:
        return "audio"
    return "unknown"


def _format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / 1024 / 1024:.1f} MB"


def _suggestions(kind: str, size: int, metadata: dict) -> list[str]:
    tips = []
    if size > 50 * 1024 * 1024:
        tips.append("文件较大，建议先压缩再分享。")
    if kind == "video":
        if metadata.get("format") not in {"mp4", "m4v"}:
            tips.append("如果要发给大多数平台，建议转成 MP4。")
        if metadata.get("width", 0) > 1920:
            tips.append("分辨率较高，可考虑输出 1080p 预览版。")
        if metadata.get("duration", 0) > 60:
            tips.append("视频较长，可以先裁剪重点片段。")
    elif kind == "image":
        if metadata.get("width", 0) > 2400:
            tips.append("图片尺寸较大，网页使用前建议缩放。")
        if metadata.get("has_alpha"):
            tips.append("图片包含透明通道，转换 JPG 会丢失透明效果。")
        if metadata.get("format") in {"png", "bmp"}:
            tips.append("如果用于网页，WebP 通常更省空间。")
    elif kind == "audio":
        if metadata.get("duration", 0) > 180:
            tips.append("音频较长，可以先剪切需要的片段。")
        if metadata.get("bitrate", 0) > 256000:
            tips.append("码率较高，日常分享可压缩到 128k 或 192k。")
    if not tips:
        tips.append("文件状态正常，可以直接选择需要的处理方式。")
    return tips


def _analyze_av(path: str, kind: str, ext: str) -> dict:
    probe = ffmpeg.probe(path)
    fmt = probe.get("format", {})
    streams = probe.get("streams", [])
    metadata = {
        "format": ext.lstrip("."),
        "duration": round(_safe_float(fmt.get("duration")), 2),
        "bitrate": _safe_int(fmt.get("bit_rate")),
    }
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if kind == "video" and video_stream:
        metadata.update({
            "width": _safe_int(video_stream.get("width")),
            "height": _safe_int(video_stream.get("height")),
            "video_codec": video_stream.get("codec_name", ""),
        })
    if audio_stream:
        metadata.update({
            "audio_codec": audio_stream.get("codec_name", ""),
            "sample_rate": _safe_int(audio_stream.get("sample_rate")),
            "channels": _safe_int(audio_stream.get("channels")),
        })
    return metadata


def _analyze_image(path: str, ext: str) -> dict:
    with Image.open(path) as img:
        return {
            "format": (img.format or ext.lstrip(".")).lower(),
            "width": img.width,
            "height": img.height,
            "mode": img.mode,
            "has_alpha": img.mode in ("RGBA", "LA") or ("transparency" in img.info),
        }


@router.post("")
async def analyze(file: UploadFile = File(...)):
    path = await save_upload(file)
    ext = Path(file.filename or path).suffix.lower()
    kind = _kind_from_ext(ext)
    size = os.path.getsize(path)
    if kind == "unknown":
      raise HTTPException(400, "暂不支持分析这个文件格式")
    try:
        metadata = _analyze_image(path, ext) if kind == "image" else _analyze_av(path, kind, ext)
    except Exception as exc:
        raise HTTPException(500, f"读取文件信息失败: {exc}")
    return {
        "kind": kind,
        "filename": file.filename or os.path.basename(path),
        "size": size,
        "size_label": _format_bytes(size),
        "format": metadata.get("format", ext.lstrip(".")),
        "metadata": metadata,
        "suggestions": _suggestions(kind, size, metadata),
    }
