"""
Home Page — Moving Object Detection & Tracking
Hero banner, project overview, and feature showcase.
"""

import streamlit as st
from utils.styles import inject_css, gradient_header, feature_badges, divider_with_label, glass_card, stat_cards


def render_home():
    inject_css()

    # ── Hero Banner ────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-banner">
          <!-- Animated orbs -->
          <div style="position:absolute;top:20px;left:10%;width:120px;height:120px;
                      border-radius:50%;background:radial-gradient(circle,rgba(79,142,247,0.25),transparent);
                      animation:float-glow 5s ease-in-out infinite;"></div>
          <div style="position:absolute;bottom:20px;right:10%;width:80px;height:80px;
                      border-radius:50%;background:radial-gradient(circle,rgba(155,89,247,0.3),transparent);
                      animation:float-glow 4s ease-in-out infinite 1s;"></div>
          <div style="position:absolute;top:50%;left:5%;width:60px;height:60px;
                      border-radius:50%;background:radial-gradient(circle,rgba(0,212,255,0.2),transparent);
                      animation:float-glow 6s ease-in-out infinite 2s;"></div>

          <!-- Content -->
          <div style="position:relative;z-index:2;">
            <div style="font-size:3.5rem;margin-bottom:0.5rem;">🤖</div>
            <h1 style="font-family:'Space Grotesk',sans-serif;font-size:2.8rem;font-weight:800;
                        background:linear-gradient(135deg,#00d4ff,#4f8ef7,#9b59f7);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;margin:0 0 0.5rem;">
              Moving Object Detection
            </h1>
            <h2 style="font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:600;
                        background:linear-gradient(135deg,#9b59f7,#f759d4);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;margin:0 0 1rem;">
              &amp; Tracking System
            </h2>
            <p style="color:#a8c4f5;font-size:1.1rem;max-width:640px;margin:0 auto 1.5rem;line-height:1.7;">
              Advanced <strong style="color:#00d4ff;">Computer Vision</strong> system for
              real-time object detection in images &amp; videos using
              <strong style="color:#9b59f7;">Transformer-based</strong> deep learning
            </p>
            <!-- Status Badges -->
            <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
              <span style="background:rgba(0,212,100,0.15);border:1px solid rgba(0,212,100,0.35);
                           border-radius:20px;padding:0.3rem 1rem;font-size:0.85rem;color:#00d464;font-weight:600;">
                <span class="pulse-dot" style="width:8px;height:8px;margin-right:6px;"></span>
                Live Detection
              </span>
              <span style="background:rgba(79,142,247,0.15);border:1px solid rgba(79,142,247,0.35);
                           border-radius:20px;padding:0.3rem 1rem;font-size:0.85rem;color:#4f8ef7;font-weight:600;">
                🤗 Hugging Face
              </span>
              <span style="background:rgba(155,89,247,0.15);border:1px solid rgba(155,89,247,0.35);
                           border-radius:20px;padding:0.3rem 1rem;font-size:0.85rem;color:#9b59f7;font-weight:600;">
                🔬 DINO Architecture
              </span>
              <span style="background:rgba(255,87,212,0.15);border:1px solid rgba(255,87,212,0.35);
                           border-radius:20px;padding:0.3rem 1rem;font-size:0.85rem;color:#f759d4;font-weight:600;">
                🎓 Final Year Project
              </span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Quick Stats ────────────────────────────────────────────────
    stat_cards({
        "Model Params":      ("172M",  "🧠"),
        "Architecture":      ("DINO",  "🔬"),
        "Vocab Size":        ("Open",  "📖"),
        "Modalities":        ("2",     "🎯"),
        "Backbone":          ("Swin-B","⚙️"),
        "Source":            ("HF 🤗", "📦"),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Features Grid ──────────────────────────────────────────────
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown(
            """
            <div class="glass-card">
              <h3 style="font-family:'Space Grotesk',sans-serif;margin-top:0;
                          background:linear-gradient(135deg,#00d4ff,#4f8ef7);
                          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                          background-clip:text;">
                🚀 Core Capabilities
              </h3>
            """,
            unsafe_allow_html=True,
        )
        feature_badges([
            "Transformer Architecture",
            "Open Vocabulary Detection",
            "Supports Images (JPG/PNG)",
            "Supports Videos (MP4/AVI/MOV)",
            "Bounding Box Visualization",
            "Confidence Score Display",
            "Text Prompt Detection",
            "Multi-Object Detection",
            "Real-time Inference Stats",
        ])
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown(
            """
            <div class="glass-card">
              <h3 style="font-family:'Space Grotesk',sans-serif;margin-top:0;
                          background:linear-gradient(135deg,#9b59f7,#f759d4);
                          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                          background-clip:text;">
                🛠️ Technology Stack
              </h3>
            """,
            unsafe_allow_html=True,
        )
        feature_badges([
            "Hugging Face Transformers",
            "PyTorch Deep Learning",
            "Google Colab Compatible",
            "OpenCV Video Processing",
            "Pillow Image Handling",
            "Plotly Visualizations",
            "Streamlit Web Framework",
            "CUDA GPU Acceleration",
            "Modern Computer Vision",
        ])
        st.markdown("</div>", unsafe_allow_html=True)

    # ── How It Works ───────────────────────────────────────────────
    divider_with_label("HOW IT WORKS")

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    steps = [
        ("01", "📤", "Upload", "Upload an image or video file through the intuitive file uploader"),
        ("02", "✏️", "Prompt", "Enter a text prompt describing the objects you want to detect"),
        ("03", "🔍", "Detect", "Grounding DINO processes your input using its transformer backbone"),
        ("04", "📊", "Results", "View annotated output with bounding boxes and confidence scores"),
    ]
    for col, (num, icon, title, desc) in zip([col1, col2, col3, col4], steps):
        with col:
            st.markdown(
                f"""
                <div class="stat-card" style="padding:1.5rem 1rem;min-height:180px;">
                  <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
                  <div style="font-size:0.7rem;color:var(--accent-cyan);font-weight:700;
                               letter-spacing:2px;margin-bottom:0.3rem;">STEP {num}</div>
                  <div style="font-size:1rem;font-weight:700;color:var(--text-primary);
                               margin-bottom:0.5rem;font-family:'Space Grotesk',sans-serif;">{title}</div>
                  <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.5;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Model Highlight ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    divider_with_label("ABOUT THE MODEL")

    st.markdown(
        """
        <div class="glass-card">
          <div style="display:flex;align-items:flex-start;gap:1.5rem;flex-wrap:wrap;">
            <div style="font-size:4rem;line-height:1;">🦕</div>
            <div style="flex:1;min-width:280px;">
              <h2 style="font-family:'Space Grotesk',sans-serif;margin:0 0 0.5rem;
                          background:linear-gradient(135deg,#4f8ef7,#9b59f7);
                          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                          background-clip:text;">
                Grounding DINO
              </h2>
              <p style="color:#a0aec0;line-height:1.7;margin-bottom:0.8rem;">
                <strong style="color:#e8eaf6;">IDEA-Research/grounding-dino-base</strong> — A state-of-the-art
                open-set object detector that combines a <span style="color:#00d4ff;">DINO</span> (DETR with Improved
                deNoising anchOR boxes) backbone with a <span style="color:#9b59f7;">Grounding</span> mechanism,
                enabling zero-shot detection of any object described in natural language.
              </p>
              <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <span style="background:rgba(0,212,255,0.12);border:1px solid rgba(0,212,255,0.3);
                             border-radius:6px;padding:3px 10px;font-size:0.8rem;color:#00d4ff;">Zero-shot</span>
                <span style="background:rgba(79,142,247,0.12);border:1px solid rgba(79,142,247,0.3);
                             border-radius:6px;padding:3px 10px;font-size:0.8rem;color:#4f8ef7;">Open-vocabulary</span>
                <span style="background:rgba(155,89,247,0.12);border:1px solid rgba(155,89,247,0.3);
                             border-radius:6px;padding:3px 10px;font-size:0.8rem;color:#9b59f7;">Transformer-based</span>
                <span style="background:rgba(247,89,212,0.12);border:1px solid rgba(247,89,212,0.3);
                             border-radius:6px;padding:3px 10px;font-size:0.8rem;color:#f759d4;">Text-guided</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Navigation CTA ─────────────────────────────────────────────
    divider_with_label("GET STARTED")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;cursor:pointer;">
              <div style="font-size:2.5rem;margin-bottom:0.5rem;">🖼️</div>
              <div style="font-size:1.1rem;font-weight:700;color:#4f8ef7;margin-bottom:0.3rem;">Image Detection</div>
              <div style="font-size:0.85rem;color:#a0aec0;">Upload images and detect objects with custom text prompts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;cursor:pointer;">
              <div style="font-size:2.5rem;margin-bottom:0.5rem;">🎥</div>
              <div style="font-size:1.1rem;font-weight:700;color:#9b59f7;margin-bottom:0.3rem;">Video Detection</div>
              <div style="font-size:0.85rem;color:#a0aec0;">Process videos frame-by-frame with real-time progress tracking</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;cursor:pointer;">
              <div style="font-size:2.5rem;margin-bottom:0.5rem;">📊</div>
              <div style="font-size:1.1rem;font-weight:700;color:#00d4ff;margin-bottom:0.3rem;">Performance</div>
              <div style="font-size:0.85rem;color:#a0aec0;">View inference metrics, FPS, and detection statistics</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Footer ─────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;margin-top:3rem;padding-top:2rem;
                    border-top:1px solid var(--glass-border);color:#a0aec0;font-size:0.85rem;">
          Built with ❤️ using
          <span style="color:#4f8ef7;">Streamlit</span> ·
          <span style="color:#9b59f7;">PyTorch</span> ·
          <span style="color:#00d4ff;">OpenCV</span> ·
          <span style="color:#f759d4;">Computer Vision</span>
          <br><span style="color:#606880;font-size:0.78rem;margin-top:0.3rem;display:block;">
            Computer Vision &amp; Deep Learning
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
