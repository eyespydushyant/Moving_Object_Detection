"""
Image Detection Page
Upload an image, enter a text prompt, and run Grounding DINO inference.
"""

import time
import numpy as np
import streamlit as st
from PIL import Image

from utils.styles import inject_css, gradient_header, divider_with_label, info_box
from utils.model import load_model, get_system_info
from utils.image_processing import annotate_image_pil, pil_to_bytes


# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
EXAMPLE_PROMPTS = [
    "person. car. bus. truck. bicycle. dog.",
    "person. motorcycle. traffic light. stop sign.",
    "cat. dog. bird. chair. couch.",
    "bottle. cup. fork. knife. bowl.",
]


def render_image_detection(settings: dict):
    """Render the Image Detection page."""
    inject_css()
    gradient_header(
        "Image Detection",
        "Upload an image and detect objects using natural language prompts",
        "🖼️",
    )

    # ── Settings read-out ─────────────────────────────────────────
    box_threshold  = settings.get("box_threshold", 0.35)
    text_threshold = settings.get("text_threshold", 0.25)
    box_color_name = settings.get("box_color", "Gradient (Auto)")
    font_size      = settings.get("font_size", 16)
    model_name     = settings.get("model_name", "Grounding DINO Base")
    box_color_map  = {
        "Gradient (Auto)": None,
        "Cyan":   (0, 212, 255),
        "Purple": (155, 89, 247),
        "Green":  (0, 212, 100),
        "Orange": (255, 140, 0),
        "Pink":   (247, 89, 212),
    }
    box_color = box_color_map.get(box_color_name)

    # ── Layout: upload + prompt ───────────────────────────────────
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            '<div class="glass-card" style="padding:1.5rem;">',
            unsafe_allow_html=True,
        )
        st.markdown("### 📤 Upload Image")
        uploaded = st.file_uploader(
            "Drop your image here",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            key="img_upload",
            label_visibility="collapsed",
        )

        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded Image", use_container_width=True)
            st.markdown(
                f"""
                <div style="background:rgba(79,142,247,0.08);border-radius:8px;padding:0.6rem 0.8rem;
                            margin-top:0.5rem;font-size:0.83rem;color:#a0aec0;">
                  📏 Size: <strong style="color:#4f8ef7;">{image.width} × {image.height}</strong> px &nbsp;|&nbsp;
                  🎨 Mode: <strong style="color:#9b59f7;">{image.mode}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown(
            '<div class="glass-card" style="padding:1.5rem;">',
            unsafe_allow_html=True,
        )
        st.markdown("### ✏️ Detection Settings")

        # Prompt
        prompt = st.text_area(
            "Text Prompt",
            value="person. car. bus. truck. bicycle. dog.",
            height=80,
            help="Enter object names separated by periods. Example: 'person. car. bus.'",
        )

        # Example prompts
        st.markdown(
            "<p style='color:#a0aec0;font-size:0.82rem;margin-bottom:4px;'>💡 Quick examples:</p>",
            unsafe_allow_html=True,
        )
        for ep in EXAMPLE_PROMPTS:
            if st.button(f"📌 {ep}", key=f"ep_{ep}", use_container_width=True):
                st.session_state["img_prompt_override"] = ep
                st.rerun()

        if "img_prompt_override" in st.session_state:
            prompt = st.session_state.pop("img_prompt_override")

        # Active settings preview
        st.markdown(
            f"""
            <div style="background:rgba(79,142,247,0.06);border:1px solid rgba(79,142,247,0.15);
                        border-radius:10px;padding:0.8rem;margin-top:0.5rem;font-size:0.83rem;">
              <div style="color:#a0aec0;margin-bottom:6px;font-weight:600;">⚙️ Active Settings</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;color:#c0cadc;">
                <span>🎯 Box Threshold: <strong style="color:#4f8ef7;">{box_threshold}</strong></span>
                <span>📝 Text Threshold: <strong style="color:#9b59f7;">{text_threshold}</strong></span>
                <span>🎨 Box Color: <strong style="color:#00d4ff;">{box_color_name}</strong></span>
                <span>🔤 Font Size: <strong style="color:#f759d4;">{font_size}</strong></span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Detect button
        detect_btn = st.button(
            "🔍 Detect Objects",
            type="primary",
            use_container_width=True,
            disabled=(uploaded is None),
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Inference ─────────────────────────────────────────────────
    if detect_btn and uploaded:
        st.markdown("<br>", unsafe_allow_html=True)
        divider_with_label("DETECTION RESULTS")

        with st.spinner("🔄 Loading model… (first run may take a moment)"):
            processor, model, device = load_model(model_name)

        if processor is None:
            st.error("❌ Failed to load model. Please check your internet connection.")
            return

        with st.spinner("🔬 Running inference…"):
            from utils.model import run_inference
            image_rgb = Image.open(uploaded).convert("RGB")
            result = run_inference(
                image_rgb, prompt, processor, model, device,
                box_threshold, text_threshold,
            )

        # Annotate
        annotated = annotate_image_pil(
            image_rgb,
            result["boxes"],
            result["scores"],
            result["labels"],
            box_color=box_color,
            font_size=font_size,
        )

        # Log to session performance history
        if "perf_history" not in st.session_state:
            st.session_state["perf_history"] = []
        st.session_state["perf_history"].append({
            "type":           "Image",
            "inference_time": result["inference_time"],
            "detections":     result["num_detections"],
            "avg_confidence": float(np.mean(result["scores"])) if len(result["scores"]) > 0 else 0.0,
            "timestamp":      time.time(),
        })

        # ── Metrics row ────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🎯 Objects Found",  result["num_detections"])
        m2.metric("⏱️ Inference Time", f"{result['inference_time']*1000:.1f} ms")
        m3.metric("📊 Avg Confidence",
                  f"{float(np.mean(result['scores']))*100:.1f}%" if len(result["scores"]) > 0 else "N/A")
        sysinfo = get_system_info()
        m4.metric("🖥️ Device", sysinfo["device"])

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Side-by-side images ────────────────────────────────────
        img_col, det_col = st.columns(2, gap="large")
        with img_col:
            st.markdown("#### 🖼️ Original Image")
            st.image(image_rgb, use_container_width=True)
        with det_col:
            st.markdown("#### ✅ Detected Objects")
            st.image(annotated, use_container_width=True)

        # ── Detection table ────────────────────────────────────────
        if result["num_detections"] > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            divider_with_label("DETECTION DETAILS")
            with st.expander("📋 View All Detections", expanded=True):
                import pandas as pd
                import plotly.express as px
                rows = []
                for i, (box, score, label) in enumerate(
                    zip(result["boxes"], result["scores"], result["labels"])
                ):
                    x1, y1, x2, y2 = map(int, box)
                    w = x2 - x1
                    h = y2 - y1
                    rows.append({
                        "#":               i + 1,
                        "Label":           str(label).upper(),
                        "Confidence (%)":  round(float(score) * 100, 1),
                        "Confidence":      f"{float(score)*100:.1f}%",
                        "X1":              x1,
                        "Y1":              y1,
                        "W":               w,
                        "H":               h,
                        "Area (px²)":      w * h,
                    })
                df = pd.DataFrame(rows)
                # Display table without numeric confidence column
                st.dataframe(
                    df.drop(columns=["Confidence (%)"]),
                    use_container_width=True, hide_index=True
                )

                # Confidence bar chart — use numeric column
                fig = px.bar(
                    df,
                    x="Label",
                    y="Confidence (%)",
                    color="Confidence (%)",
                    color_continuous_scale=["#4f8ef7", "#9b59f7", "#f759d4"],
                    title="Detection Confidence Scores",
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(15,22,41,0.5)",
                    font_color="#e8eaf6",
                    title_font_size=16,
                    coloraxis_showscale=False,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            info_box(
                "No objects detected. Try lowering the confidence threshold in Settings "
                "or adjusting your text prompt.",
                "⚠️",
            )

        # ── Download ───────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        img_bytes = pil_to_bytes(annotated, "PNG")
        st.download_button(
            label="⬇️ Download Annotated Image",
            data=img_bytes,
            file_name="detected_objects.png",
            mime="image/png",
            use_container_width=True,
        )
        st.success("✅ Detection complete! Download your annotated image above.")
        st.toast("🎉 Detection successful!", icon="✅")

    elif not uploaded:
        info_box(
            "Upload an image using the file uploader above to get started. "
            "Supports JPG, JPEG, PNG, BMP, and WebP formats.",
            "👆",
        )
