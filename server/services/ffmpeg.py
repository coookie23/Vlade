import os
import re
import subprocess
import threading
import ffmpeg


def get_duration(input_path: str) -> float:
    probe = ffmpeg.probe(input_path)
    return float(probe["format"]["duration"])


def _run_with_progress(task_id: str, input_path: str, output_path: str, build_cmd, label: str = "处理中"):
    """Run ffmpeg subprocess and pipe progress updates to the shared store."""
    from utils import task_start, task_progress, task_done, task_error

    dur = get_duration(input_path)
    task_start(task_id, dur, label)  # update with real duration

    cmd = build_cmd(output_path)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    time_pattern = re.compile(r"time=(\d+):(\d+):(\d+)[\\.](\d+)")
    speed_pattern = re.compile(r"speed=\s*([\d\\.]+)x")

    for line in proc.stdout:
        m = time_pattern.search(line)
        if m and dur > 0:
            h, mi, s, cs = int(m[1]), int(m[2]), int(m[3]), int(m[4])
            elapsed = h * 3600 + mi * 60 + s + cs / 100.0
            pct = (elapsed / dur) * 100
            sp = 0.0
            sm = speed_pattern.search(line)
            if sm:
                sp = float(sm[1])
            task_progress(task_id, pct, sp)

    proc.wait()
    if proc.returncode != 0:
        task_error(task_id, "FFmpeg 处理失败")
        raise RuntimeError("FFmpeg processing failed")
    task_done(task_id)
    return output_path


def compress_video(input_path: str, output_path: str, crf: int = 28):
    def cmd(out):
        return ffmpeg.input(input_path).output(
            out, vcodec="libx264", crf=crf, preset="fast",
            acodec="aac", audio_bitrate="128k", movflags="faststart",
        ).overwrite_output().compile()
    subprocess.run(cmd(output_path), capture_output=True)
    return output_path


def convert_video(input_path: str, output_path: str, fmt: str = "mp4"):
    def cmd(out):
        return ffmpeg.input(input_path).output(
            out, vcodec="libx264", crf=23, preset="medium",
            acodec="aac", audio_bitrate="192k",
        ).overwrite_output().compile()
    subprocess.run(cmd(output_path), capture_output=True)
    return output_path


def trim_video(input_path: str, output_path: str, start: float, duration: float):
    def cmd(out):
        return ffmpeg.input(input_path, ss=start, t=duration).output(
            out, vcodec="libx264", acodec="aac", movflags="faststart",
        ).overwrite_output().compile()
    subprocess.run(cmd(output_path), capture_output=True)
    return output_path


def merge_videos(input_paths: list, output_path: str):
    concat_file = output_path + ".txt"
    with open(concat_file, "w") as f:
        for p in input_paths:
            f.write(f"file '{p}'\n")
    def cmd(out):
        return ffmpeg.input(concat_file, format="concat", safe=0).output(
            out, vcodec="libx264", acodec="aac", movflags="faststart",
        ).overwrite_output().compile()
    subprocess.run(cmd(output_path), capture_output=True)
    os.remove(concat_file)
    return output_path


def extract_audio(input_path: str, output_path: str, fmt: str = "mp3"):
    codec_map = {"mp3": "libmp3lame", "aac": "aac", "wav": "pcm_s16le"}
    acodec = codec_map.get(fmt, "libmp3lame")
    def cmd(out):
        return ffmpeg.input(input_path).output(
            out, vn=True, acodec=acodec, audio_bitrate="192k",
        ).overwrite_output().compile()
    subprocess.run(cmd(output_path), capture_output=True)
    return output_path


def add_subtitle(input_path: str, output_path: str, subtitle_path: str):
    subtitle_path_norm = subtitle_path.replace("\\", "/").replace(":", "\\\\:")
    def cmd(out):
        return ffmpeg.input(input_path).output(
            out, vf=f"subtitles='{subtitle_path_norm}'",
            vcodec="libx264", acodec="aac", movflags="faststart",
        ).overwrite_output().compile()
    subprocess.run(cmd(output_path), capture_output=True)
    return output_path


# ── Audio services (no progress needed, fast enough) ──

def compress_audio(input_path: str, output_path: str, bitrate: str = "128k"):
    ffmpeg.input(input_path).output(output_path, audio_bitrate=bitrate).overwrite_output().run(quiet=True)
    return output_path


def convert_audio(input_path: str, output_path: str, fmt: str = "mp3"):
    codec_map = {"mp3": "libmp3lame", "aac": "aac", "wav": "pcm_s16le", "ogg": "libvorbis"}
    acodec = codec_map.get(fmt, "libmp3lame")
    ffmpeg.input(input_path).output(output_path, acodec=acodec, audio_bitrate="192k").overwrite_output().run(quiet=True)
    return output_path


def trim_audio(input_path: str, output_path: str, start: float, duration: float):
    ffmpeg.input(input_path, ss=start, t=duration).output(output_path, acodec="copy").overwrite_output().run(quiet=True)
    return output_path


def merge_audios(input_paths: list, output_path: str):
    concat_file = output_path + ".txt"
    with open(concat_file, "w") as f:
        for p in input_paths:
            f.write(f"file '{p}'\n")
    ffmpeg.input(concat_file, format="concat", safe=0).output(output_path, acodec="libmp3lame", audio_bitrate="192k").overwrite_output().run(quiet=True)
    os.remove(concat_file)
    return output_path


def change_volume(input_path: str, output_path: str, factor: float = 1.5):
    ffmpeg.input(input_path).output(output_path, af=f"volume={factor}").overwrite_output().run(quiet=True)
    return output_path


def denoise_audio(input_path: str, output_path: str):
    ffmpeg.input(input_path).output(output_path, af="afftdn=nr=30:nf=-25").overwrite_output().run(quiet=True)
    return output_path


def video_to_gif(input_path: str, output_path: str, fps: int = 10, width: int = 320):
    palette_path = output_path + ".png"
    def cmd(out, pal):
        return [
            *ffmpeg.input(input_path).output(pal, vf=f"fps={fps},scale={width}:-1:flags=lanczos,palettegen").overwrite_output().compile(),
        ]
    subprocess.run(ffmpeg.input(input_path).output(palette_path, vf=f"fps={fps},scale={width}:-1:flags=lanczos,palettegen").overwrite_output().compile(), capture_output=True)
    vid = ffmpeg.input(input_path).video.filter('fps', fps=fps).filter('scale', width, -1, flags='lanczos')
    pal = ffmpeg.input(palette_path).video
    subprocess.run(ffmpeg.filter([vid, pal], 'paletteuse').output(output_path).overwrite_output().compile(), capture_output=True)
    if os.path.exists(palette_path):
        os.remove(palette_path)
    return output_path


# ── RIFE & Douyin ──

def rife_interpolate(task_id: str, input_path: str, output_path: str, target_fps: int = 60, mode: str = "平衡"):
    mode = (mode or "平衡").strip().lower()
    if mode in {"fast", "快速"}:
        vf = f"fps={target_fps}"
        preset = "veryfast"
        crf = 22
    elif mode in {"balanced", "平衡"}:
        vf = f"minterpolate=fps={target_fps}:mi_mode=mci:mc_mode=obmc:me=epzs"
        preset = "fast"
        crf = 20
    else:
        vf = f"minterpolate=fps={target_fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1:me=epzs"
        preset = "medium"
        crf = 18

    def cmd(out):
        return ffmpeg.input(input_path).output(
            out,
            vf=vf,
            vcodec="libx264", crf=crf, preset=preset,
            acodec="aac", audio_bitrate="192k", movflags="faststart",
        ).overwrite_output().compile()
    return _run_with_progress(task_id, input_path, output_path, cmd, f"智能补帧 {target_fps}fps")


def douyin_optimize(input_path: str, output_path: str):
    probe = ffmpeg.probe(input_path)
    fps_str = probe["streams"][0]["r_frame_rate"]
    num, den = fps_str.split("/")
    source_fps = float(num) / float(den)
    itsscale_val = source_fps / 30.0

    ffmpeg.input(input_path, itsscale=str(itsscale_val)).output(
        output_path, vcodec="copy", acodec="copy",
    ).overwrite_output().run(quiet=True)
    return output_path
