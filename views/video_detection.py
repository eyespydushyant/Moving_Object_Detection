"""
Video Detection Page
Upload a video, enter a text prompt, and process frame-by-frame with Grounding DINO.
"""

import time
import os
import tempfile
import streamlit as st

from utils.styles import inject_css, gradient_header, divider_with_label, info_box, stat_cards
from utils.model import load_model, get_system_info
from utils.video_processing import get_video_info, process_video, read_video_bytes


def render_video_detection(settings: dict):
    """Render the Video Detection page."""
    inject_css()
    gradient_header(
        "Video Detection",
        "Process videos frame-by-frame with Grounding DINO and generate annotated output",
        "🎥",
    )

    # ── Settings ──────────────────────────────────────────────────
    box_threshold  = settings.get("box_threshold", 0.35)
    text_threshold = settings.get("text_threshold", 0.25)
    box_color_name = settings.get("box_color", "Gradient (Auto)")
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

    # ── Layout ────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="glass-card" style="padding:1.5rem;">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload Video")
        uploaded_video = st.file_uploader(
            "Upload your video",
            type=["mp4", "avi", "mov", "mkv", "wmv"],
            key="vid_upload",
            label_visibility="collapsed",
        )

        if uploaded_video:
            # Save to temp so OpenCV can read it
            tfile = tempfile.NamedTemporaryFile(
                delete=False, suffix=os.path.splitext(uploaded_video.name)[-1]
            )
            tfile.write(uploaded_video.read())
            tfile.close()
            st.session_state["video_temp_path"] = tfile.name

            # Display preview
            st.video(uploaded_video)

            # Video metadata
            info = get_video_info(tfile.name)
            if info:
                st.markdown(
                    f"""
                    <div style="background:rgba(79,142,247,0.08);border-radius:8px;padding:0.8rem;
                                margin-top:0.5rem;font-size:0.83rem;display:grid;
                                grid-template-columns:1fr 1fr;gap:6px;color:#c0cadc;">
                      <span>📐 Resolution: <strong style="color:#4f8ef7;">{info['width']}×{info['height']}</strong></span>
                      <span>🎬 FPS: <strong style="color:#9b59f7;">{info['fps']:.1f}</strong></span>
                      <span>🎞️ Frames: <strong style="color:#00d4ff;">{info['total_frames']}</strong></span>
                      <span>⏱️ Duration: <strong style="color:#f759d4;">{info['duration_sec']:.1f}s</strong></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card" style="padding:1.5rem;">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Processing Settings")

        prompt = st.text_area(
            "Text Prompt",
            value="person. car. motorcycle. bicycle. bus. truck.",
            height=80,
            help="Objects to detect, separated by periods",
        )

        frame_skip = st.slider(
            "⚡ Frame Skip (1 = every frame, higher = faster)",
            min_value=1, max_value=10, value=1,
            help="Process every Nth frame. Higher values = faster but less smooth.",
        )

        st.markdown(
            f"""
            <div style="background:rgba(79,142,247,0.06);border:1px solid rgba(79,142,247,0.15);
                        border-radius:10px;padding:0.8rem;margin-top:0.5rem;font-size:0.83rem;">
              <div style="color:#a0aec0;margin-bottom:6px;font-weight:600;">⚙️ Active Settings</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;color:#c0cadc;">
                <span>🎯 Box Threshold: <strong style="color:#4f8ef7;">{box_threshold}</strong></span>
                <span>📝 Text Threshold: <strong style="color:#9b59f7;">{text_threshold}</strong></span>
                <span>🎨 Box Color: <strong style="color:#00d4ff;">{box_color_name}</strong></span>
                <span>⚡ Frame Skip: <strong style="color:#f759d4;">{frame_skip}</strong></span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sysinfo = get_system_info()
        gpu_label = sysinfo.get("gpu_name", "N/A") or "CPU"
        st.markdown(
            f"""
            <div style="margin-top:0.8rem;display:flex;align-items:center;gap:10px;
                        background:rgba(0,212,100,0.08);border:1px solid rgba(0,212,100,0.2);
                        border-radius:8px;padding:0.6rem 0.8rem;font-size:0.85rem;">
              <span class="pulse-dot"></span>
              <span style="color:#00d464;font-weight:600;">Device: {sysinfo['device']}</span>
              <span style="color:#a0aec0;">| {gpu_label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        process_btn = st.button(
            "🚀 Process Video",
            type="primary",
            use_container_width=True,
            disabled=(uploaded_video is None),
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Processing ────────────────────────────────────────────────
    if process_btn and uploaded_video:
        video_path = st.session_state.get("video_temp_path")
        if not video_path or not os.path.exists(video_path):
            st.error("❌ Could not find the uploaded video file. Please re-upload.")
            return

        st.markdown("<br>", unsafe_allow_html=True)
        divider_with_label("PROCESSING")

        # Model loading
        with st.spinner("🔄 Loading Grounding DINO model…"):
            processor, model, device = load_model(model_name)

        if processor is None:
            st.error("❌ Failed to load model.")
            return

        # Live stats containers
        prog_col, stat_col = st.columns([2, 1], gap="large")

        with prog_col:
            progress_bar = st.progress(0.0, text="Initializing…")

        with stat_col:
            stat_container = st.empty()

        status_box = st.empty()

        # Collect stats for display
        live_stats = {}

        def on_progress(frac):
            pct = int(frac * 100)
            progress_bar.progress(frac, text=f"Processing frames… {pct}%")

        def on_stats(s):
            live_stats.update(s)
            elapsed  = s["elapsed"]
            remaining = s["remaining"]
            fps      = s["current_fps"]
            frame    = s["frame_idx"]
            total    = s["total_frames"]

            stat_container.markdown(
                f"""
                <div class="glass-card" style="padding:1rem;">
                  <div style="font-size:0.8rem;color:#a0aec0;font-weight:600;margin-bottom:8px;">
                    LIVE STATS
                  </div>
                  <div style="display:grid;gap:6px;font-size:0.83rem;color:#c0cadc;">
                    <div>🎞️ Frame: <strong style="color:#4f8ef7;">{frame}/{total}</strong></div>
                    <div>⏱️ Elapsed: <strong style="color:#9b59f7;">{elapsed:.1f}s</strong></div>
                    <div>⏳ Remaining: <strong style="color:#00d4ff;">{remaining:.1f}s</strong></div>
                    <div>⚡ FPS: <strong style="color:#f759d4;">{fps:.1f}</strong></div>
                    <div>🎯 Avg Det.: <strong style="color:#00d464;">{s['avg_detections']:.1f}</strong></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.spinner("🔬 Running detection on all frames…"):
            try:
                result = process_video(
                    video_path=video_path,
                    text_prompt=prompt,
                    processor=processor,
                    model=model,
                    device=device,
                    box_threshold=box_threshold,
                    text_threshold=text_threshold,
                    box_color=box_color,
                    progress_callback=on_progress,
                    stats_callback=on_stats,
                    frame_skip=frame_skip,
                )
            except Exception as e:
                st.error(f"❌ Processing failed: {e}")
                return

        progress_bar.progress(1.0, text="✅ Done!")
        status_box.success("🎉 Video processing complete!")
        st.toast("Video processed successfully!", icon="🎥")

        # Log to performance history
        if "perf_history" not in st.session_state:
            st.session_state["perf_history"] = []
        st.session_state["perf_history"].append({
            "type":           "Video",
            "inference_time": result["avg_inf_time"],
            "detections":     result["avg_detections"],
            "avg_confidence": 0.0,
            "timestamp":      time.time(),
        })

        # ── Final Stats ───────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        divider_with_label("PROCESSING SUMMARY")

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("🎞️ Total Frames",   result["total_frames"])
        s2.metric("⏱️ Total Time",     f"{result['elapsed_time']:.1f}s")
        s3.metric("⚡ Avg FPS",        f"{result['avg_fps']:.1f}")
        s4.metric("🎯 Avg Detections", f"{result['avg_detections']:.1f}")

        # ── Output Video ──────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        divider_with_label("OUTPUT VIDEO")

        out_path = result["output_path"]
        if os.path.exists(out_path):
            st.video(out_path)

            video_bytes = read_video_bytes(out_path)
            st.download_button(
                label="⬇️ Download Annotated Video",
                data=video_bytes,
                file_name="detected_video.mp4",
                mime="video/mp4",
                use_container_width=True,
            )
        else:
            st.warning("⚠️ Output video file not found.")

    elif not uploaded_video:
        info_box(
            "Upload a video file (MP4, AVI, MOV) to get started. "
            "The system will process each frame and generate an annotated output video.",
            "👆",
        )

        # ── Demo tips ─────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💡 Tips for Best Results")
        c1, c2, c3 = st.columns(3, gap="medium")
        tips = [
            ("🎥", "Use clear, well-lit videos for higher accuracy"),
            ("📝", "Separate objects in prompt with periods: 'person. car.'"),
            ("⚡", "Use Frame Skip > 1 to speed up long videos"),
        ]
        for col, (icon, tip) in zip([c1, c2, c3], tips):
            with col:
                st.markdown(
                    f"""
                    <div class="glass-card" style="text-align:center;padding:1.2rem;">
                      <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
                      <div style="font-size:0.85rem;color:#a0aec0;line-height:1.5;">{tip}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
