"""
Video Processing Utilities
Handles frame extraction, batch inference, and output video generation.
"""

import cv2
import numpy as np
import time
import os
import tempfile
from PIL import Image

from utils.model import run_inference
from utils.image_processing import annotate_frame_cv2, cv2_to_pil


# ─────────────────────────────────────────────
# Video Metadata
# ─────────────────────────────────────────────
def get_video_info(video_path: str) -> dict:
    """
    Extract metadata from a video file.

    Returns:
        dict with fps, total_frames, width, height, duration_sec
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {}
    info = {
        "fps":          cap.get(cv2.CAP_PROP_FPS) or 25.0,
        "total_frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width":        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height":       int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    info["duration_sec"] = info["total_frames"] / max(info["fps"], 1)
    cap.release()
    return info


# ─────────────────────────────────────────────
# Frame-by-Frame Processing
# ─────────────────────────────────────────────
def process_video(
    video_path: str,
    text_prompt: str,
    processor,
    model,
    device,
    box_threshold: float = 0.35,
    text_threshold: float = 0.25,
    box_color: tuple = None,
    font_size: float = 0.6,
    progress_callback=None,
    stats_callback=None,
    frame_skip: int = 1,
) -> dict:
    """
    Process every frame of a video with Grounding DINO and write annotated output.

    Args:
        video_path: Path to input video file.
        text_prompt: Detection prompt.
        processor: HuggingFace processor.
        model: HuggingFace model.
        device: torch device.
        box_threshold: Detection confidence threshold.
        text_threshold: Text confidence threshold.
        box_color: Optional RGB tuple for bounding boxes.
        font_size: OpenCV font scale for labels.
        progress_callback: Callable(fraction: float) for progress updates.
        stats_callback: Callable(stats_dict) for live stats.
        frame_skip: Process every Nth frame (1 = all frames).

    Returns:
        dict with output_path, total_frames, elapsed_time, avg_fps, avg_detections
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps        = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total      = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Prepare output file (temp MP4)
    out_file   = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    out_path   = out_file.name
    out_file.close()

    fourcc     = cv2.VideoWriter_fourcc(*"mp4v")
    writer     = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    frame_idx      = 0
    processed      = 0
    total_det      = 0
    inference_times = []
    start_time     = time.perf_counter()
    last_annotated = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference on selected frames; copy last result for skipped frames
        if frame_idx % frame_skip == 0:
            pil_img = cv2_to_pil(frame)
            t0 = time.perf_counter()
            result  = run_inference(
                pil_img, text_prompt, processor, model, device,
                box_threshold, text_threshold,
            )
            t1 = time.perf_counter()
            inference_times.append(t1 - t0)

            annotated = annotate_frame_cv2(
                frame,
                result["boxes"],
                result["scores"],
                result["labels"],
                box_color=box_color,
                font_size=font_size,
            )
            last_annotated = annotated
            total_det     += result["num_detections"]
            processed     += 1
        else:
            annotated = last_annotated if last_annotated is not None else frame

        writer.write(annotated)
        frame_idx += 1

        # Callbacks for live stats
        elapsed  = time.perf_counter() - start_time
        cur_fps  = frame_idx / max(elapsed, 0.001)
        remaining = ((total - frame_idx) / max(cur_fps, 0.001))

        if progress_callback:
            progress_callback(frame_idx / max(total, 1))

        if stats_callback:
            stats_callback({
                "frame_idx":     frame_idx,
                "total_frames":  total,
                "elapsed":       elapsed,
                "remaining":     remaining,
                "current_fps":   cur_fps,
                "avg_detections": total_det / max(processed, 1),
            })

    cap.release()
    writer.release()

    total_elapsed = time.perf_counter() - start_time
    avg_fps       = frame_idx / max(total_elapsed, 0.001)
    avg_det       = total_det / max(processed, 1)

    return {
        "output_path":    out_path,
        "total_frames":   frame_idx,
        "elapsed_time":   total_elapsed,
        "avg_fps":        avg_fps,
        "avg_detections": avg_det,
        "avg_inf_time":   float(np.mean(inference_times)) if inference_times else 0.0,
    }


def read_video_bytes(path: str) -> bytes:
    """Read a video file and return its bytes."""
    with open(path, "rb") as f:
        return f.read()
