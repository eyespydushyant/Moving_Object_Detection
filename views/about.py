"""
About Model Page
Deep-dive into Grounding DINO architecture, comparisons, and capabilities.
"""

import streamlit as st
from utils.styles import inject_css, gradient_header, divider_with_label, info_box, glass_card


def render_about(settings: dict):
    """Render the Model Information page."""
    inject_css()
    gradient_header(
        "About the Model",
        "Deep dive into Grounding DINO — Architecture, Capabilities & Comparisons",
        "🦕",
    )

    # ── Tabs ──────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧠 Overview",
        "🔬 Architecture",
        "⚖️ vs YOLO",
        "✅ Advantages",
        "⚠️ Limitations",
    ])

    # ─────────────────── TAB 1: Overview ──────────────────────────
    with tab1:
        col_a, col_b = st.columns([3, 2], gap="large")

        with col_a:
            st.markdown(
                """
                <div class="glass-card">
                  <h2 style="font-family:'Space Grotesk',sans-serif;margin-top:0;
                              background:linear-gradient(135deg,#4f8ef7,#9b59f7);
                              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                              background-clip:text;">
                    What is Grounding DINO?
                  </h2>
                  <p style="color:#c0cadc;line-height:1.8;">
                    <strong style="color:#e8eaf6;">Grounding DINO</strong> (Detection with INstance-level
                    Grounding) is a state-of-the-art open-set object detector developed by
                    <span style="color:#4f8ef7;">IDEA Research</span>. It extends the
                    <strong style="color:#00d4ff;">DINO (DETR with Improved deNoising anchOR boxes)</strong>
                    detection framework by incorporating a language model for open-vocabulary detection.
                  </p>
                  <p style="color:#c0cadc;line-height:1.8;">
                    Unlike conventional detectors that are limited to a fixed set of categories,
                    Grounding DINO can detect <em>any object</em> described in natural language,
                    making it a powerful tool for flexible and zero-shot object detection tasks.
                  </p>
                  <p style="color:#c0cadc;line-height:1.8;">
                    The model was introduced in the paper
                    <em style="color:#9b59f7;">"Grounding DINO: Marrying DINO with Grounded Pre-Training
                    for Open-Set Object Detection"</em> (Liu et al., 2023).
                  </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_b:
            st.markdown(
                """
                <div class="glass-card" style="text-align:center;">
                  <div style="font-size:5rem;margin-bottom:1rem;">🦕</div>
                  <h3 style="font-family:'Space Grotesk',sans-serif;color:#4f8ef7;margin-top:0;">
                    IDEA-Research
                  </h3>
                  <div style="color:#a0aec0;font-size:0.9rem;line-height:1.6;margin-bottom:1rem;">
                    grounding-dino-base
                  </div>

                  <div style="display:grid;gap:8px;text-align:left;">
                    <div style="background:rgba(79,142,247,0.1);border-radius:8px;padding:0.5rem 0.8rem;
                                font-size:0.83rem;color:#c0cadc;">
                      📦 <strong style="color:#4f8ef7;">Model Size:</strong> ~172M parameters
                    </div>
                    <div style="background:rgba(155,89,247,0.1);border-radius:8px;padding:0.5rem 0.8rem;
                                font-size:0.83rem;color:#c0cadc;">
                      🦴 <strong style="color:#9b59f7;">Backbone:</strong> Swin-B Transformer
                    </div>
                    <div style="background:rgba(0,212,255,0.1);border-radius:8px;padding:0.5rem 0.8rem;
                                font-size:0.83rem;color:#c0cadc;">
                      📝 <strong style="color:#00d4ff;">Language:</strong> BERT encoder
                    </div>
                    <div style="background:rgba(247,89,212,0.1);border-radius:8px;padding:0.5rem 0.8rem;
                                font-size:0.83rem;color:#c0cadc;">
                      🎯 <strong style="color:#f759d4;">Type:</strong> Open-vocabulary
                    </div>
                    <div style="background:rgba(0,212,100,0.1);border-radius:8px;padding:0.5rem 0.8rem;
                                font-size:0.83rem;color:#c0cadc;">
                      ⚡ <strong style="color:#00d464;">Pre-training:</strong> Grounded Cap.
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Key concepts
        st.markdown("<br>", unsafe_allow_html=True)
        divider_with_label("KEY CONCEPTS")
        k1, k2, k3 = st.columns(3, gap="medium")
        concepts = [
            ("🎯", "Open-Vocabulary Detection", "#4f8ef7",
             "Detects any object category described in text, without retraining. No fixed class list — infinite categories."),
            ("🔢", "Zero-Shot Transfer", "#9b59f7",
             "Generalizes to unseen classes at inference time. No labeled examples needed for new categories."),
            ("🤝", "Vision-Language Fusion", "#00d4ff",
             "Deep fusion between image features and text embeddings enables language-guided object localization."),
        ]
        for col, (icon, title, color, desc) in zip([k1, k2, k3], concepts):
            with col:
                st.markdown(
                    f"""
                    <div class="glass-card" style="text-align:center;min-height:200px;">
                      <div style="font-size:2.5rem;margin-bottom:0.5rem;">{icon}</div>
                      <div style="font-size:1rem;font-weight:700;color:{color};margin-bottom:0.5rem;
                                   font-family:'Space Grotesk',sans-serif;">{title}</div>
                      <div style="font-size:0.83rem;color:#a0aec0;line-height:1.6;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ─────────────────── TAB 2: Architecture ──────────────────────
    with tab2:
        st.markdown("### 🏗️ Architecture Overview")

        # Mermaid diagram
        st.markdown(
            """
            <div class="glass-card">
              <h4 style="color:#4f8ef7;margin-top:0;">Model Pipeline</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.code(
            """
            ┌─────────────────────────────────────────────────────────────────┐
            │                    GROUNDING DINO ARCHITECTURE                    │
            ├─────────────────────────────────────────────────────────────────┤
            │                                                                   │
            │   Input Image ──► Swin Transformer Backbone ──► Multi-scale     │
            │                        (Feature Extractor)        Feature Maps   │
            │                                                        │          │
            │   Text Prompt ──► BERT Text Encoder ──► Text Features           │
            │                                                        │          │
            │                    Feature Enhancer (Deformable Transformer)     │
            │                    ┌─────────────────────────────────┐           │
            │                    │  Image Features ◄──► Text Feats │           │
            │                    │  (Cross-Attention Fusion)       │           │
            │                    └─────────────────────────────────┘           │
            │                                │                                  │
            │                    Language-Guided Query Selection                │
            │                    (Anchor Points from Text-Image Fusion)        │
            │                                │                                  │
            │                    DINO Decoder (Box Prediction)                 │
            │                    ┌─────────────────────────────────┐           │
            │                    │  Self-Attention + Cross-Attention│           │
            │                    │  Iterative Box Refinement        │           │
            │                    └─────────────────────────────────┘           │
            │                                │                                  │
            │                    ┌───────────┴───────────┐                     │
            │                    │                       │                      │
            │               Box Predictions         Phrase Scores              │
            │               (x, y, w, h)           (object-text align)        │
            │                    │                       │                      │
            │                    └───────────┬───────────┘                     │
            │                                │                                  │
            │                    Predicted Bounding Boxes + Labels              │
            └─────────────────────────────────────────────────────────────────┘
            """,
            language=None,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#4f8ef7;margin-top:0;">🦴 Image Backbone: Swin Transformer</h4>
                  <p style="color:#c0cadc;line-height:1.7;font-size:0.9rem;">
                    The <strong style="color:#4f8ef7;">Swin Transformer</strong> serves as the image backbone.
                    It uses a hierarchical design with shifted windows to produce multi-scale feature maps,
                    enabling detection of objects at various scales.
                  </p>
                  <ul style="color:#c0cadc;font-size:0.88rem;line-height:1.8;">
                    <li>Hierarchical feature extraction</li>
                    <li>Shifted window self-attention</li>
                    <li>Linear computational complexity</li>
                    <li>Outputs 4 feature map scales</li>
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#9b59f7;margin-top:0;">📝 Text Backbone: BERT Encoder</h4>
                  <p style="color:#c0cadc;line-height:1.7;font-size:0.9rem;">
                    <strong style="color:#9b59f7;">BERT</strong> (Bidirectional Encoder Representations
                    from Transformers) processes the text prompt and produces rich contextual embeddings
                    that are fused with visual features for language-guided detection.
                  </p>
                  <ul style="color:#c0cadc;font-size:0.88rem;line-height:1.8;">
                    <li>Bidirectional text understanding</li>
                    <li>Sub-word tokenization</li>
                    <li>512-token context window</li>
                    <li>768-dim token embeddings</li>
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        col3, col4 = st.columns(2, gap="large")
        with col3:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#00d4ff;margin-top:0;">🔗 Feature Enhancer: Cross-Modal Fusion</h4>
                  <p style="color:#c0cadc;line-height:1.7;font-size:0.9rem;">
                    A <strong style="color:#00d4ff;">deformable transformer</strong> module acts as
                    a feature enhancer, performing bidirectional cross-attention between image and
                    text features to create linguistically grounded visual representations.
                  </p>
                  <ul style="color:#c0cadc;font-size:0.88rem;line-height:1.8;">
                    <li>Image-to-text cross-attention</li>
                    <li>Text-to-image cross-attention</li>
                    <li>6 encoder layer stack</li>
                    <li>Multi-scale deformable attention</li>
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                """
                <div class="glass-card">
                  <h4 style="color:#f759d4;margin-top:0;">🎯 DINO Decoder</h4>
                  <p style="color:#c0cadc;line-height:1.7;font-size:0.9rem;">
                    The <strong style="color:#f759d4;">DINO decoder</strong> uses language-guided
                    query initialization and contrastive denoising training to predict bounding boxes
                    and alignment scores between detected regions and text phrases.
                  </p>
                  <ul style="color:#c0cadc;font-size:0.88rem;line-height:1.8;">
                    <li>Query-based box regression</li>
                    <li>Iterative box refinement (6 layers)</li>
                    <li>DN (denoising) training</li>
                    <li>Sub-sentence level alignment</li>
                  </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ─────────────────── TAB 3: vs YOLO ───────────────────────────
    with tab3:
        st.markdown("### ⚖️ Grounding DINO vs YOLO")

        st.markdown(
            """
            <div class="glass-card">
              <div style="overflow-x:auto;">
                <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
                  <thead>
                    <tr style="background:rgba(79,142,247,0.15);">
                      <th style="padding:12px 16px;text-align:left;color:#4f8ef7;border-bottom:1px solid rgba(79,142,247,0.25);">Feature</th>
                      <th style="padding:12px 16px;text-align:left;color:#9b59f7;border-bottom:1px solid rgba(79,142,247,0.25);">Grounding DINO</th>
                      <th style="padding:12px 16px;text-align:left;color:#00d4ff;border-bottom:1px solid rgba(79,142,247,0.25);">YOLO (v8/v9)</th>
                    </tr>
                  </thead>
                  <tbody style="color:#c0cadc;">
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Vocabulary</td>
                      <td style="padding:10px 16px;color:#00d464;">✅ Open (any object via text)</td>
                      <td style="padding:10px 16px;color:#f7a059;">⚠️ Fixed (e.g., 80 COCO classes)</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Zero-shot Detection</td>
                      <td style="padding:10px 16px;color:#00d464;">✅ Yes</td>
                      <td style="padding:10px 16px;color:#ff6b6b;">❌ No</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Text Prompt Support</td>
                      <td style="padding:10px 16px;color:#00d464;">✅ Natural language</td>
                      <td style="padding:10px 16px;color:#ff6b6b;">❌ None</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Architecture</td>
                      <td style="padding:10px 16px;">Vision-Language Transformer</td>
                      <td style="padding:10px 16px;">CNN + CSP bottleneck</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Inference Speed</td>
                      <td style="padding:10px 16px;color:#f7a059;">⚠️ Moderate (GPU recommended)</td>
                      <td style="padding:10px 16px;color:#00d464;">✅ Very Fast (even on CPU)</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Model Size</td>
                      <td style="padding:10px 16px;">~172M parameters (Base)</td>
                      <td style="padding:10px 16px;">~3–68M parameters</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">COCO AP</td>
                      <td style="padding:10px 16px;color:#00d464;">🏆 ~57.2 AP (state-of-the-art)</td>
                      <td style="padding:10px 16px;">~53.9 AP (YOLOv9-E)</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Training Required</td>
                      <td style="padding:10px 16px;color:#00d464;">✅ No (zero-shot)</td>
                      <td style="padding:10px 16px;color:#ff6b6b;">❌ For new classes</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,142,247,0.1);">
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">HuggingFace Support</td>
                      <td style="padding:10px 16px;color:#00d464;">✅ Native transformers</td>
                      <td style="padding:10px 16px;color:#f7a059;">⚠️ Via ultralytics</td>
                    </tr>
                    <tr>
                      <td style="padding:10px 16px;font-weight:600;color:#e8eaf6;">Best Use Case</td>
                      <td style="padding:10px 16px;">Research, new categories, NLP integration</td>
                      <td style="padding:10px 16px;">Real-time, edge deployment, known classes</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        info_box(
            "Grounding DINO excels in research and scenarios with new/unknown object categories, "
            "while YOLO is preferred for real-time inference on edge devices with known classes.",
            "💡",
        )

    # ─────────────────── TAB 4: Advantages ────────────────────────
    with tab4:
        st.markdown("### ✅ Advantages of Grounding DINO")
        advantages = [
            ("🌐", "Open-Vocabulary",       "#4f8ef7",
             "Can detect any object described in text. No retraining required for new object categories. "
             "Simply change the text prompt to detect new objects."),
            ("🎯", "High Accuracy",          "#9b59f7",
             "Achieves state-of-the-art 57.2 AP on COCO benchmark. Significantly outperforms traditional "
             "detectors on complex scenes with overlapping objects."),
            ("✏️", "Text-Guided Flexibility", "#00d4ff",
             "Use natural language to guide detection. Supports descriptive prompts, multiple objects, "
             "and attribute-based queries like 'red car' or 'person with umbrella'."),
            ("🤗", "HuggingFace Integration","#f759d4",
             "Seamlessly integrates with the HuggingFace ecosystem. Easy model loading, no complex "
             "setup required — just a few lines of Python code."),
            ("🔬", "Transformer Architecture","#00d464",
             "Built on the proven DETR/DINO transformer paradigm with global attention mechanisms, "
             "enabling better context understanding than CNN-based detectors."),
            ("🚀", "Zero-Shot Transfer",     "#f7a059",
             "Generalizes to completely new domains without fine-tuning. Trained on large-scale "
             "grounding datasets, it has broad world knowledge about objects."),
        ]
        col1, col2 = st.columns(2, gap="large")
        for i, (icon, title, color, desc) in enumerate(advantages):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding:1.2rem 1.5rem;">
                      <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;">
                        <span style="font-size:1.6rem;">{icon}</span>
                        <span style="font-size:1rem;font-weight:700;color:{color};
                                     font-family:'Space Grotesk',sans-serif;">{title}</span>
                      </div>
                      <p style="color:#a0aec0;font-size:0.87rem;line-height:1.6;margin:0;">{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ─────────────────── TAB 5: Limitations ───────────────────────
    with tab5:
        st.markdown("### ⚠️ Limitations & Considerations")

        limitations = [
            ("🐌", "Inference Speed",      "#f7a059",
             "Grounding DINO is slower than YOLO for real-time inference. A GPU is strongly recommended "
             "for acceptable frame rates. CPU inference can take 2–10 seconds per frame."),
            ("💾", "Memory Footprint",     "#ff6b6b",
             "The base model requires ~4–6 GB GPU VRAM. Loading multiple models simultaneously "
             "can exhaust GPU memory on consumer hardware."),
            ("📡", "Internet Required",    "#f7a059",
             "First-time use requires downloading the model weights (~680 MB for base) from "
             "HuggingFace Hub. An internet connection is mandatory for initial setup."),
            ("📝", "Prompt Sensitivity",   "#ff6b6b",
             "Detection quality depends on prompt quality. Ambiguous or overly verbose prompts "
             "may yield inconsistent results. Periods between objects are required."),
            ("🔢", "Batch Processing",     "#f7a059",
             "Does not natively support batch inference in all scenarios, which can limit throughput "
             "when processing large numbers of images sequentially."),
            ("🎞️", "Video Latency",        "#ff6b6b",
             "For video, the model processes frames sequentially. There is no tracking between frames, "
             "so detections are independent — no object ID persistence between frames."),
        ]

        col1, col2 = st.columns(2, gap="large")
        for i, (icon, title, color, desc) in enumerate(limitations):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding:1.2rem 1.5rem;border-color:rgba(247,160,89,0.2);">
                      <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;">
                        <span style="font-size:1.6rem;">{icon}</span>
                        <span style="font-size:1rem;font-weight:700;color:{color};
                                     font-family:'Space Grotesk',sans-serif;">{title}</span>
                      </div>
                      <p style="color:#a0aec0;font-size:0.87rem;line-height:1.6;margin:0;">{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
        info_box(
            "Despite these limitations, Grounding DINO remains the best choice for open-vocabulary "
            "detection tasks. Future versions are expected to be significantly faster.",
            "💡",
        )
