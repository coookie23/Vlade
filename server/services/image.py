from PIL import Image


def compress_image(input_path: str, output_path: str, quality: int = 75) -> str:
    """Compress JPEG/WebP by reducing quality. PNG handled differently."""
    img = Image.open(input_path).convert("RGB")
    ext = output_path.rsplit(".", 1)[-1].lower()
    if ext == "png":
        # For PNG output, quantize colors
        img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        img.save(output_path, "PNG", optimize=True)
    elif ext in ("webp",):
        img.save(output_path, "WEBP", quality=quality)
    else:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
    return output_path


def convert_image(input_path: str, output_path: str, fmt: str = "png") -> str:
    """Convert image format."""
    img = Image.open(input_path)
    if img.mode in ("RGBA", "P") and fmt.upper() in ("JPEG", "JPG"):
        img = img.convert("RGB")
    img.save(output_path, fmt.upper())
    return output_path


def crop_image(input_path: str, output_path: str,
               x: int, y: int, w: int, h: int) -> str:
    """Crop image to rectangle (x, y, w, h)."""
    img = Image.open(input_path)
    cropped = img.crop((x, y, x + w, y + h))
    cropped.save(output_path)
    return output_path


def resize_image(input_path: str, output_path: str,
                 width: int = 0, height: int = 0) -> str:
    """Resize image. If one dimension is 0, maintain aspect ratio."""
    img = Image.open(input_path)
    orig_w, orig_h = img.size
    if width and height:
        new_size = (width, height)
    elif width:
        ratio = width / orig_w
        new_size = (width, int(orig_h * ratio))
    elif height:
        ratio = height / orig_h
        new_size = (int(orig_w * ratio), height)
    else:
        new_size = (orig_w, orig_h)
    img = img.resize(new_size, Image.LANCZOS)
    img.save(output_path)
    return output_path


def add_watermark(input_path: str, output_path: str, text: str = "",
                   opacity: int = 128) -> str:
    """Add text watermark at bottom-right corner."""
    img = Image.open(input_path).convert("RGBA")
    if not text:
        img.convert("RGB").save(output_path)
        return output_path

    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype("arial.ttf", size=max(16, min(img.size) // 20))
    except (OSError, IOError):
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = img.size[0] - tw - 20
    y = img.size[1] - th - 20
    draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)
    combined = Image.alpha_composite(img, overlay)
    combined.convert("RGB").save(output_path)
    return output_path
