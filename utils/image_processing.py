"""
Image Processing Utilities
Handles annotation, bounding box drawing, and image conversion.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io


# ─────────────────────────────────────────────
# Color Palette
# ─────────────────────────────────────────────
PALETTE = [
    (0, 212, 255),   # cyan-blue
    (138, 43, 226),  # blue-violet
    (0, 255, 127),   # spring green
    (255, 100, 0),   # orange
    (255, 0, 128),   # hot pink
    (255, 215, 0),   # gold
    (0, 191, 255),   # deep sky blue
    (148, 0, 211),   # dark violet
    (0, 255, 200),   # aquamarine
    (255, 69, 0),    # red-orange
]


def get_color(index: int) -> tuple:
    """Return a color from the palette for a given index."""
    return PALETTE[index % len(PALETTE)]


# ─────────────────────────────────────────────
# Draw Bounding Boxes (PIL-based)
# ─────────────────────────────────────────────
def annotate_image_pil(
    image: Image.Image,
    boxes: np.ndarray,
    scores: np.ndarray,
    labels: list,
    box_color: tuple = None,
    font_size: int = 16,
    line_width: int = 3,
) -> Image.Image:
    """
    Draw bounding boxes and labels on a PIL image.

    Args:
        image: Original PIL image.
        boxes: Array of shape (N, 4) in xyxy format.
        scores: Array of shape (N,) with confidence scores.
        labels: List of N label strings.
        box_color: Optional override color (R, G, B).
        font_size: Font size for labels.
        line_width: Bounding box line width.

    Returns:
        Annotated PIL image.
    """
    annotated = image.copy().convert("RGB")
    draw = ImageDraw.Draw(annotated, "RGBA")

    # Try to load a nicer font; fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        small_font = ImageFont.truetype("arial.ttf", max(font_size - 4, 10))
    except Exception:
        font = ImageFont.load_default()
        small_font = font

    for i, (box, score, label) in enumerate(zip(boxes, scores, labels)):
        x1, y1, x2, y2 = map(int, box)
        color = box_color if box_color else get_color(i)

        # Semi-transparent fill
        draw.rectangle([x1, y1, x2, y2], outline=color + (255,), width=line_width)
        draw.rectangle([x1, y1, x2, y2], fill=color + (25,))

        # Label text
        text = f"{label}: {score:.2f}"
        # Text background
        try:
            bbox = draw.textbbox((x1, y1 - font_size - 4), text, font=font)
            draw.rectangle(bbox, fill=color + (200,))
            draw.text((x1, y1 - font_size - 4), text, fill=(255, 255, 255), font=font)
        except Exception:
            draw.text((x1, max(y1 - 20, 0)), text, fill=color)

    return annotated


# ─────────────────────────────────────────────
# Draw Bounding Boxes (OpenCV-based, for video)
# ─────────────────────────────────────────────
def annotate_frame_cv2(
    frame: np.ndarray,
    boxes: np.ndarray,
    scores: np.ndarray,
    labels: list,
    box_color: tuple = None,
    font_size: float = 0.6,
    line_width: int = 2,
) -> np.ndarray:
    """
    Draw bounding boxes on an OpenCV (BGR) frame.

    Args:
        frame: OpenCV BGR numpy array.
        boxes: Array of shape (N, 4) in xyxy format.
        scores: Array of shape (N,) confidence scores.
        labels: List of N label strings.
        box_color: Optional BGR tuple override.
        font_size: OpenCV font scale.
        line_width: Box line thickness.

    Returns:
        Annotated BGR numpy array.
    """
    annotated = frame.copy()
    for i, (box, score, label) in enumerate(zip(boxes, scores, labels)):
        x1, y1, x2, y2 = map(int, box)
        # Convert RGB palette to BGR for OpenCV
        rgb = box_color if box_color else get_color(i)
        bgr = (rgb[2], rgb[1], rgb[0])

        # Box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), bgr, line_width)

        # Label background
        text = f"{label}: {score:.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)
        label_y = max(y1, th + 10)
        cv2.rectangle(annotated, (x1, label_y - th - 8), (x1 + tw + 4, label_y + 2), bgr, -1)
        cv2.putText(
            annotated, text,
            (x1 + 2, label_y - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_size,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
    return annotated


# ─────────────────────────────────────────────
# Conversion Helpers
# ─────────────────────────────────────────────
def pil_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert a PIL image to bytes."""
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def cv2_to_pil(frame: np.ndarray) -> Image.Image:
    """Convert an OpenCV BGR frame to a PIL RGB image."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def pil_to_cv2(image: Image.Image) -> np.ndarray:
    """Convert a PIL RGB image to an OpenCV BGR frame."""
    rgb = np.array(image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
