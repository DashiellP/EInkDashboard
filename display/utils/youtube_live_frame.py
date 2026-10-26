import io
import subprocess
import yt_dlp
from PIL import Image


def youtube_live_frame(url, width=600):
    with yt_dlp.YoutubeDL({
        "format": "bv*[height>=480]",
        "format_sort": ["+res"],
        "quiet": True,
        "noplaylist": True,
    }) as ydl:
        info = ydl.extract_info(url, download=False)

    if "url" in info:
        stream_url = info["url"]
    elif "requested_formats" in info:
        video_format = next(
            f for f in info["requested_formats"]
            if f.get("vcodec") != "none"
        )
        stream_url = video_format["url"]
    else:
        raise ValueError("No playable stream URL found")

    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-i", stream_url,
            "-frames:v", "1",
            "-vf", f"scale={width}:-2",
            "-f", "image2pipe",
            "-vcodec", "mjpeg",
            "-",
        ],
        capture_output=True,
        timeout=45,
        check=True,
    )

    return Image.open(io.BytesIO(result.stdout)).convert("RGB")