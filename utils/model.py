"""
Model Loading and Inference Utilities
Handles Grounding DINO model loading, caching, and inference.
"""

import streamlit as st
import torch
import numpy as np
from PIL import Image
import time
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
MODEL_IDS = {
    "Grounding DINO Tiny": "IDEA-Research/grounding-dino-tiny",
    "Grounding DINO Base": "IDEA-Research/grounding-dino-base",
}

DEFAULT_MODEL = "Grounding DINO Tiny"

# ─────────────────────────────────────────────
# Device Detection
# ─────────────────────────────────────────────
def get_device():
    """Return the best available device (CUDA > CPU)."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


# ─────────────────────────────────────────────
# Cached Model Loading
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model(model_name: str = DEFAULT_MODEL):
    """
    Load and cache the Grounding DINO model and processor.
    Uses st.cache_resource so the model is loaded only once per session.

    Args:
        model_name: Key from MODEL_IDS dict.

    Returns:
        Tuple of (processor, model, device)
    """
    model_id = MODEL_IDS.get(model_name, MODEL_IDS[DEFAULT_MODEL])
    device = get_device()

    try:
        processor = AutoProcessor.from_pretrained(model_id)
        model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id)
        model = model.to(device)
        model.eval()
        return processor, model, device
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        return None, None, None


# ─────────────────────────────────────────────
# Core Inference
# ─────────────────────────────────────────────
def run_inference(
    image: Image.Image,
    text_prompt: str,
    processor,
    model,
    device,
    box_threshold: float = 0.35,
    text_threshold: float = 0.25,
):
    """
    Run Grounding DINO inference on a PIL image.

    Args:
        image: PIL RGB image.
        text_prompt: Dot-separated text prompt, e.g. "person. car. bus."
        processor: HuggingFace processor.
        model: HuggingFace Grounding DINO model.
        device: torch device.
        box_threshold: Confidence threshold for bounding boxes.
        text_threshold: Confidence threshold for text labels.

    Returns:
        dict with keys: boxes, scores, labels, inference_time, image_size
    """
    start = time.perf_counter()

    # Ensure the prompt ends with a period
    if not text_prompt.strip().endswith("."):
        text_prompt = text_prompt.strip() + "."

    # Pre-process
    inputs = processor(images=image, text=text_prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Forward pass (no gradient needed)
    with torch.no_grad():
        outputs = model(**inputs)

    import inspect
    sig = inspect.signature(processor.post_process_grounded_object_detection)
    kwargs = {
        "target_sizes": [image.size[::-1]]
    }
    # Check if new API (threshold) or old API (box_threshold)
    if "threshold" in sig.parameters:
        kwargs["threshold"] = box_threshold
        # New API ALSO accepts text_threshold
        if "text_threshold" in sig.parameters:
            kwargs["text_threshold"] = text_threshold
    elif "box_threshold" in sig.parameters:
        kwargs["box_threshold"] = box_threshold
        kwargs["text_threshold"] = text_threshold

    try:
        results = processor.post_process_grounded_object_detection(
            outputs,
            inputs.get("input_ids"),
            **kwargs
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"Post-processing failed. Args: {kwargs}. Error: {type(e).__name__} - {e}")

    elapsed = time.perf_counter() - start

    result = results[0]

    # Handle both tensor and numpy outputs robustly
    boxes_raw  = result["boxes"]
    scores_raw = result["scores"]
    labels     = result.get("labels", [])

    if hasattr(boxes_raw, "cpu"):
        boxes = boxes_raw.cpu().numpy()
    else:
        boxes = np.array(boxes_raw)

    if hasattr(scores_raw, "cpu"):
        scores = scores_raw.cpu().numpy()
    else:
        scores = np.array(scores_raw)

    # Apply text_threshold filter manually when using new API
    if len(scores) > 0:
        mask   = scores >= text_threshold
        boxes  = boxes[mask]
        scores = scores[mask]
        labels = [l for l, m in zip(labels, mask) if m]

    return {
        "boxes": boxes,
        "scores": scores,
        "labels": labels,
        "inference_time": elapsed,
        "image_size": image.size,
        "num_detections": len(boxes),
    }


# ─────────────────────────────────────────────
# System Info
# ─────────────────────────────────────────────
def get_system_info():
    """Return a dict of basic system/GPU info."""
    info = {
        "device": "CUDA (GPU)" if torch.cuda.is_available() else "CPU",
        "gpu_name": None,
        "gpu_memory_total_gb": None,
        "gpu_memory_used_gb": None,
    }
    if torch.cuda.is_available():
        info["gpu_name"] = torch.cuda.get_device_name(0)
        props = torch.cuda.get_device_properties(0)
        info["gpu_memory_total_gb"] = round(props.total_memory / 1e9, 2)
        allocated = torch.cuda.memory_allocated(0)
        info["gpu_memory_used_gb"] = round(allocated / 1e9, 2)
    return info
