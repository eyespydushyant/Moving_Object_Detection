"""
Documentation Page
Full project documentation — workflow, pipelines, and technical explanations.
"""

import streamlit as st
from utils.styles import inject_css, gradient_header, divider_with_label, info_box


def render_documentation(settings: dict):
    """Render the Project Documentation page."""
    inject_css()
    gradient_header(
        "Project Documentation",
        "Complete technical documentation for Moving Object Detection & Tracking",
        "📚",
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔄 Workflow",
        "🖼️ Image Pipeline",
        "🎥 Video Pipeline",
        "🔬 Transformer",
        "🚀 Applications",
    ])

    # ─────────────────── TAB 1: Workflow ──────────────────────────
    with tab1:
        st.markdown("### 🔄 Project Workflow")
        st.markdown(
            """
            <div class="glass-card">
              <h4 style="color:#4f8ef7;margin-top:0;">End-to-End System Overview</h4>
              <p style="color:#c0cadc;line-height:1.7;">
                The Moving Object Detection and Tracking system follows a modular pipeline
                that separates concerns across input handling, model inference, post-processing,
                and result visualization.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.code(
            """
            ╔══════════════════════════════════════════════════════════════════╗
            ║              MOVING OBJECT DETECTION & TRACKING                  ║
            ║                    System Workflow                                ║
            ╠══════════════════════════════════════════════════════════════════╣
            ║                                                                   ║
            ║  ┌─────────────────────────────────────────────────────────┐    ║
            ║  │                    USER INTERFACE                        │    ║
            ║  │           (Streamlit Web Application)                    │    ║
            ║  └──────────────────┬──────────────────────────────────────┘    ║
            ║                     │                                             ║
            ║           ┌─────────▼─────────┐                                  ║
            ║           │   Input Handler    │                                  ║
            ║           │  (Image / Video)   │                                  ║
            ║           └─────────┬─────────┘                                  ║
            ║                     │                                             ║
            ║           ┌─────────▼─────────┐                                  ║
            ║           │  Pre-Processing   │  ← Resize, normalize, tokenize   ║
            ║           └─────────┬─────────┘                                  ║
            ║                     │                                             ║
            ║           ┌─────────▼─────────┐                                  ║
            ║           │  Text Prompt       │  ← User-defined detection query  ║
            ║           │  Tokenization      │                                  ║
            ║           └─────────┬─────────┘                                  ║
            ║                     │                                             ║
            ║           ┌─────────▼─────────────────────────────┐             ║
            ║           │       GROUNDING DINO MODEL             │             ║
            ║           │   (IDEA-Research/grounding-dino-base)  │             ║
            ║           │                                        │             ║
            ║           │  Swin-B Backbone + BERT + DINO Dec.   │             ║
            ║           └─────────────────────────────┬─────────┘             ║
            ║                                         │                         ║
            ║           ┌─────────────────────────────▼─────────┐             ║
            ║           │         Post-Processing                │             ║
            ║           │  • Box coordinate transformation       │             ║
            ║           │  • Confidence thresholding             │             ║
            ║           │  • Label assignment                    │             ║
            ║           └─────────────────────────────┬─────────┘             ║
            ║                                         │                         ║
            ║           ┌─────────────────────────────▼─────────┐             ║
            ║           │       Annotation & Visualization       │             ║
            ║           │  • Bounding box drawing                │             ║
            ║           │  • Label overlay                       │             ║
            ║           │  • Confidence score display            │             ║
            ║           └─────────────────────────────┬─────────┘             ║
            ║                                         │                         ║
            ║           ┌─────────────────────────────▼─────────┐             ║
            ║           │           Output & Export              │             ║
            ║           │  • Annotated image display             │             ║
            ║           │  • Metrics dashboard                   │             ║
            ║           │  • Download (PNG / MP4)                │             ║
            ║           └────────────────────────────────────────┘             ║
            ╚══════════════════════════════════════════════════════════════════╝
            """,
            language=None,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3, gap="medium")
        workflow_steps = [
            ("📥", "Input",        "#4f8ef7", "Image (JPG/PNG) or Video (MP4/AVI/MOV) uploaded via Streamlit file uploader"),
            ("⚙️", "Processing",   "#9b59f7", "Model loaded from HuggingFace Hub, cached in session. Inference run with text prompt."),
            ("📤", "Output",       "#00d4ff", "Annotated result displayed in UI. Downloadable as PNG or MP4."),
        ]
        for col, (icon, title, color, desc) in zip([col1, col2, col3], workflow_steps):
            with col:
                st.markdown(
                    f"""
                    <div class="glass-card" style="text-align:center;min-height:160px;">
                      <div style="font-size:2.5rem;margin-bottom:0.5rem;">{icon}</div>
                      <div style="font-size:1rem;font-weight:700;color:{color};margin-bottom:0.4rem;
                                   font-family:'Space Grotesk',sans-serif;">{title}</div>
                      <div style="font-size:0.83rem;color:#a0aec0;line-height:1.5;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ─────────────────── TAB 2: Image Pipeline ────────────────────
    with tab2:
        st.markdown("### 🖼️ Image Detection Pipeline")
        col1, col2 = st.columns([2, 1], gap="large")

        with col1:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#4f8ef7;margin-top:0;">Step-by-Step Process</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            steps = [
                ("1️⃣", "Image Upload", "User uploads image via Streamlit file_uploader. Supported formats: JPG, JPEG, PNG, BMP, WebP."),
                ("2️⃣", "PIL Loading",  "Image is opened using Pillow (PIL) and converted to RGB mode to ensure consistent 3-channel input."),
                ("3️⃣", "Preprocessing","AutoProcessor (HuggingFace) resizes image, normalizes pixel values, and tokenizes the text prompt."),
                ("4️⃣", "Inference",    "Inputs are moved to GPU (if available) and fed to the Grounding DINO model in a torch.no_grad() context."),
                ("5️⃣", "Post-process", "post_process_grounded_object_detection() converts raw logits to boxes, scores, and labels."),
                ("6️⃣", "Thresholding", "Detections below box_threshold or text_threshold are filtered out. Remaining are the final detections."),
                ("7️⃣", "Annotation",   "Bounding boxes are drawn using PIL ImageDraw. Labels and confidence scores are overlaid as colored text."),
                ("8️⃣", "Display",      "Original and annotated images shown side-by-side. Detection table with metrics rendered below."),
                ("9️⃣", "Download",     "Annotated image encoded as PNG bytes. st.download_button provides one-click download."),
            ]
            for icon, title, desc in steps:
                st.markdown(
                    f"""
                    <div style="display:flex;gap:1rem;margin-bottom:0.8rem;align-items:flex-start;">
                      <span style="font-size:1.3rem;min-width:30px;">{icon}</span>
                      <div>
                        <div style="font-weight:700;color:#e8eaf6;font-size:0.92rem;">{title}</div>
                        <div style="color:#a0aec0;font-size:0.83rem;line-height:1.5;">{desc}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#9b59f7;margin-top:0;">Key Functions</h4>
                  <div style="font-size:0.82rem;color:#c0cadc;">
                """,
                unsafe_allow_html=True,
            )
            funcs = [
                ("load_model()", "#4f8ef7", "Cached model + processor loading"),
                ("run_inference()", "#9b59f7", "Core HuggingFace inference"),
                ("annotate_image_pil()", "#00d4ff", "PIL bounding box drawing"),
                ("pil_to_bytes()", "#f759d4", "Convert PIL → bytes for download"),
                ("get_system_info()", "#00d464", "GPU/CPU info retrieval"),
            ]
            for fn, color, desc in funcs:
                st.markdown(
                    f"""
                    <div style="margin-bottom:0.8rem;padding:0.5rem 0.7rem;
                                background:rgba(79,142,247,0.06);border-radius:6px;
                                border-left:3px solid {color};">
                      <code style="color:{color};font-size:0.82rem;">{fn}</code>
                      <div style="color:#a0aec0;font-size:0.78rem;margin-top:2px;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("</div></div>", unsafe_allow_html=True)

        # Code snippet
        with st.expander("📄 Core Inference Code"):
            st.code(
                """
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from PIL import Image
import torch

# Load model (cached with @st.cache_resource)
processor = AutoProcessor.from_pretrained("IDEA-Research/grounding-dino-base")
model = AutoModelForZeroShotObjectDetection.from_pretrained(
    "IDEA-Research/grounding-dino-base"
).to("cuda")

# Prepare inputs
image = Image.open("image.jpg").convert("RGB")
text_prompt = "person. car. bus."

inputs = processor(images=image, text=text_prompt, return_tensors="pt")
inputs = {k: v.to("cuda") for k, v in inputs.items()}

# Run inference
with torch.no_grad():
    outputs = model(**inputs)

# Post-process
results = processor.post_process_grounded_object_detection(
    outputs,
    inputs["input_ids"],
    box_threshold=0.35,
    text_threshold=0.25,
    target_sizes=[image.size[::-1]],
)

boxes  = results[0]["boxes"].cpu().numpy()   # [[x1, y1, x2, y2], ...]
scores = results[0]["scores"].cpu().numpy()  # [0.87, 0.72, ...]
labels = results[0]["labels"]                # ["person", "car", ...]
                """,
                language="python",
            )

    # ─────────────────── TAB 3: Video Pipeline ────────────────────
    with tab3:
        st.markdown("### 🎥 Video Detection Pipeline")

        st.code(
            """
            VIDEO PROCESSING PIPELINE
            ─────────────────────────────────────────────────────────────
            Input Video (MP4/AVI/MOV)
                │
                ▼
            cv2.VideoCapture()
            ├── Extract: FPS, total_frames, width, height
            │
            ▼
            cv2.VideoWriter()  ← Initialize output writer (mp4v codec)
            │
            ▼
            ┌─────────────────────────────────────────────┐
            │               FRAME LOOP                     │
            │                                             │
            │  frame = cap.read()                         │
            │  if frame_idx % frame_skip == 0:            │
            │      pil_img = cv2_to_pil(frame)            │
            │      result = run_inference(pil_img, ...)   │
            │      annotated = annotate_frame_cv2(...)    │
            │  else:                                      │
            │      annotated = last_annotated             │  ← Reuse
            │                                             │
            │  writer.write(annotated)                    │
            │  update_progress_bar()                      │
            │  update_live_stats()                        │
            └─────────────────────────────────────────────┘
                │
                ▼
            cap.release()
            writer.release()
                │
                ▼
            Output MP4 (temp file)
                │
                ▼
            st.video() display  +  st.download_button()
            """,
            language=None,
        )

        info_box(
            "Frame Skip optimization: When frame_skip > 1, the model runs on every Nth frame only. "
            "Intermediate frames reuse the last annotation. This significantly speeds up processing "
            "for long videos with minimal loss in detection quality.",
            "⚡",
        )

        with st.expander("📄 Video Processing Code"):
            st.code(
                """
import cv2
from PIL import Image
import tempfile

def process_video(video_path, text_prompt, processor, model, device, ...):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    writer = cv2.VideoWriter(out.name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    frame_idx = 0
    last_annotated = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_skip == 0:
            pil_img  = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            result   = run_inference(pil_img, text_prompt, processor, model, device)
            annotated = annotate_frame_cv2(frame, result["boxes"], ...)
            last_annotated = annotated
        else:
            annotated = last_annotated or frame

        writer.write(annotated)
        frame_idx += 1

    cap.release()
    writer.release()
    return out.name
                """,
                language="python",
            )

    # ─────────────────── TAB 4: Transformer ──────────────────────
    with tab4:
        st.markdown("### 🔬 Transformer Architecture Deep-Dive")

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#4f8ef7;margin-top:0;">🤖 What is a Transformer?</h4>
                  <p style="color:#c0cadc;font-size:0.88rem;line-height:1.7;">
                    A <strong style="color:#4f8ef7;">Transformer</strong> is a neural network architecture
                    based on <em>self-attention mechanisms</em>. Introduced in "Attention Is All You Need"
                    (Vaswani et al., 2017), it processes all input tokens in parallel (rather than
                    sequentially like RNNs), making it highly parallelizable and capable of capturing
                    long-range dependencies.
                  </p>
                  <h5 style="color:#9b59f7;">Key Components:</h5>
                  <ul style="color:#c0cadc;font-size:0.85rem;line-height:1.8;">
                    <li><strong style="color:#e8eaf6;">Self-Attention:</strong> Computes relationships between all pairs of tokens</li>
                    <li><strong style="color:#e8eaf6;">Multi-Head Attention:</strong> Multiple attention heads capture different aspects</li>
                    <li><strong style="color:#e8eaf6;">Feed-Forward Network:</strong> Position-wise nonlinear transformation</li>
                    <li><strong style="color:#e8eaf6;">Layer Normalization:</strong> Stabilizes training</li>
                    <li><strong style="color:#e8eaf6;">Positional Encoding:</strong> Injects spatial/sequential information</li>
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#9b59f7;margin-top:0;">🖼️ Vision Transformer (ViT)</h4>
                  <p style="color:#c0cadc;font-size:0.88rem;line-height:1.7;">
                    <strong style="color:#9b59f7;">Vision Transformers</strong> apply the transformer
                    architecture to images by splitting the image into fixed-size patches, linearly
                    embedding each patch, and processing them as a sequence with transformer layers.
                  </p>
                  <h5 style="color:#00d4ff;">Swin Transformer Improvements:</h5>
                  <ul style="color:#c0cadc;font-size:0.85rem;line-height:1.8;">
                    <li>Hierarchical feature maps (like CNNs)</li>
                    <li>Shifted window attention (local + global)</li>
                    <li>Linear complexity with respect to image size</li>
                    <li>Suitable for dense prediction tasks</li>
                    <li>Better inductive bias for vision tasks</li>
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="glass-card">
              <h4 style="color:#00d4ff;margin-top:0;">🔗 DETR → DINO → Grounding DINO Evolution</h4>
              <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:0.5rem;">
                <div style="background:rgba(79,142,247,0.1);border-radius:10px;padding:1rem;text-align:center;">
                  <div style="font-weight:700;color:#4f8ef7;font-size:1rem;margin-bottom:0.4rem;">DETR (2020)</div>
                  <div style="font-size:0.8rem;color:#a0aec0;line-height:1.5;">First transformer-based end-to-end object detector. Uses bipartite matching loss.</div>
                </div>
                <div style="background:rgba(155,89,247,0.1);border-radius:10px;padding:1rem;text-align:center;">
                  <div style="font-weight:700;color:#9b59f7;font-size:1rem;margin-bottom:0.4rem;">DINO (2022)</div>
                  <div style="font-size:0.8rem;color:#a0aec0;line-height:1.5;">Improved DETR with denoising training, mixed query selection, and better convergence.</div>
                </div>
                <div style="background:rgba(0,212,255,0.1);border-radius:10px;padding:1rem;text-align:center;">
                  <div style="font-weight:700;color:#00d4ff;font-size:1rem;margin-bottom:0.4rem;">Grounding DINO (2023)</div>
                  <div style="font-size:0.8rem;color:#a0aec0;line-height:1.5;">Extended DINO with language grounding for open-vocabulary detection via text prompts.</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ─────────────────── TAB 5: Applications ─────────────────────
    with tab5:
        st.markdown("### 🚀 Applications & Future Scope")

        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            st.markdown("#### 🌍 Real-World Applications")
            apps = [
                ("🚗", "Autonomous Vehicles",   "Detecting pedestrians, vehicles, and traffic signs in real-time for self-driving systems."),
                ("🎥", "Surveillance Systems",  "Monitoring public spaces for suspicious activities, crowd management, and security."),
                ("🏭", "Industrial QA",         "Automated defect detection in manufacturing lines without retraining for new defect types."),
                ("🏥", "Medical Imaging",       "Detecting anatomical structures described in radiologist prompts — zero-shot."),
                ("🛒", "Retail Analytics",      "Tracking products, monitoring shelf stock, and analyzing customer behavior."),
                ("🌿", "Wildlife Monitoring",   "Identifying and counting animals in camera trap footage using natural language queries."),
                ("🏗️", "Construction Safety",  "Detecting PPE compliance — hard hats, vests — without fixed class training."),
                ("🤖", "Robotics",              "Enabling robots to locate and manipulate objects specified via voice/text commands."),
            ]
            for icon, title, desc in apps:
                st.markdown(
                    f"""
                    <div style="display:flex;gap:0.8rem;margin-bottom:0.7rem;padding:0.6rem 0.8rem;
                                background:rgba(79,142,247,0.06);border-radius:8px;
                                border-left:3px solid rgba(79,142,247,0.4);">
                      <span style="font-size:1.2rem;">{icon}</span>
                      <div>
                        <div style="font-weight:600;color:#e8eaf6;font-size:0.9rem;">{title}</div>
                        <div style="color:#a0aec0;font-size:0.8rem;line-height:1.5;">{desc}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col_b:
            st.markdown("#### 🔮 Future Scope")
            future = [
                ("🏃", "Multi-Object Tracking",  "Integrate DeepSORT or ByteTrack to maintain object IDs across video frames for true tracking."),
                ("⚡", "Real-time Inference",    "Optimize with TensorRT, ONNX, or model quantization for ≥30 FPS real-time detection."),
                ("🌐", "REST API",               "Expose detection as a REST API endpoint for integration with other systems."),
                ("📱", "Mobile Deployment",      "Quantize model for Android/iOS deployment using PyTorch Mobile or TFLite."),
                ("🎙️", "Voice Prompts",          "Accept voice-based detection queries using speech-to-text as input."),
                ("📊", "Custom Dashboards",      "Real-time streaming dashboards for live camera feeds with analytics."),
                ("🤝", "SAM Integration",        "Combine with Segment Anything Model (SAM) for precise instance segmentation."),
                ("☁️", "Cloud Deployment",       "Deploy on AWS/GCP/Azure with auto-scaling for production workloads."),
            ]
            for icon, title, desc in future:
                st.markdown(
                    f"""
                    <div style="display:flex;gap:0.8rem;margin-bottom:0.7rem;padding:0.6rem 0.8rem;
                                background:rgba(155,89,247,0.06);border-radius:8px;
                                border-left:3px solid rgba(155,89,247,0.4);">
                      <span style="font-size:1.2rem;">{icon}</span>
                      <div>
                        <div style="font-weight:600;color:#e8eaf6;font-size:0.9rem;">{title}</div>
                        <div style="color:#a0aec0;font-size:0.8rem;line-height:1.5;">{desc}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # References
        st.markdown("<br>", unsafe_allow_html=True)
        divider_with_label("REFERENCES")
        st.markdown(
            """
            <div class="glass-card">
              <h4 style="color:#4f8ef7;margin-top:0;">📄 Key Papers & Resources</h4>
              <ul style="color:#c0cadc;font-size:0.87rem;line-height:2;">
                <li>Liu et al. (2023) — <em style="color:#9b59f7;">Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection</em></li>
                <li>Zhang et al. (2022) — <em style="color:#4f8ef7;">DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection</em></li>
                <li>Carion et al. (2020) — <em style="color:#00d4ff;">End-to-End Object Detection with Transformers (DETR)</em></li>
                <li>Liu et al. (2021) — <em style="color:#f759d4;">Swin Transformer: Hierarchical Vision Transformer using Shifted Windows</em></li>
                <li>Vaswani et al. (2017) — <em style="color:#00d464;">Attention Is All You Need</em></li>
                <li>Devlin et al. (2018) — <em style="color:#f7a059;">BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding</em></li>
              </ul>
              <div style="margin-top:0.5rem;font-size:0.83rem;color:#606880;">
                HuggingFace Hub: <strong style="color:#4f8ef7;">IDEA-Research/grounding-dino-base</strong> &
                <strong style="color:#9b59f7;">IDEA-Research/grounding-dino-tiny</strong>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
