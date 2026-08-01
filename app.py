"""
Moving Object Detection & Tracking
Powered by Grounding DINO Transformer + Hugging Face

Run with: streamlit run app.py
"""

import streamlit as st

# ── Page Config (MUST be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="Moving Object Detection & Tracking",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help":     None,
        "Report a bug": None,
        "About":        "Moving Object Detection & Tracking\nComputer Vision & Deep Learning",
    },
)

# ── Page imports ────────────────────────────────────────────────────────────
from views.home          import render_home
from views.image_detection import render_image_detection
from views.video_detection import render_video_detection
from views.about         import render_about
from views.performance   import render_performance
from views.documentation import render_documentation
from utils.styles        import inject_css, GLOBAL_CSS


# ── Session State Defaults ──────────────────────────────────────────────────
def init_session_state():
    defaults = {
        "page":          "🏠 Home",
        "dark_mode":     True,
        "perf_history":  [],
        "settings": {
            "box_threshold":  0.35,
            "text_threshold": 0.25,
            "box_color":      "Gradient (Auto)",
            "font_size":      16,
            "model_name":     "Grounding DINO Base",
        },
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()


# ── Sidebar ─────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo / Title
        st.markdown(
            """
            <div style="text-align:center;padding:1rem 0 0.5rem;">
              <div style="font-size:3rem;animation:float-glow 4s ease-in-out infinite;">🤖</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:1rem;font-weight:700;
                           background:linear-gradient(135deg,#4f8ef7,#9b59f7);
                           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                           background-clip:text;line-height:1.3;margin-top:0.3rem;">
                Moving Object<br>Detection & Tracking
              </div>
              <div style="font-size:0.72rem;color:#606880;margin-top:0.2rem;letter-spacing:0.5px;">
                Computer Vision · Deep Learning
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<hr style="border-color:rgba(79,142,247,0.15);margin:0.75rem 0;">',
            unsafe_allow_html=True,
        )

        # Navigation
        st.markdown(
            '<div style="font-size:0.72rem;color:#606880;font-weight:700;letter-spacing:1.5px;'
            'text-transform:uppercase;margin-bottom:0.5rem;padding:0 0.3rem;">Navigation</div>',
            unsafe_allow_html=True,
        )

        nav_items = [
            ("🏠 Home",            "🏠"),
            ("🖼️ Image Detection",  "🖼️"),
            ("🎥 Video Detection",  "🎥"),
            ("🦕 Model Info",       "🦕"),
            ("📊 Performance",      "📊"),
            ("📚 Documentation",    "📚"),
        ]

        for page_name, icon in nav_items:
            is_active = st.session_state["page"] == page_name
            btn_style = (
                "background:linear-gradient(135deg,rgba(79,142,247,0.25),rgba(155,89,247,0.25));"
                "border:1px solid rgba(79,142,247,0.4);"
                if is_active else
                "background:transparent;border:1px solid transparent;"
            )
            if st.button(
                page_name,
                key=f"nav_{page_name}",
                use_container_width=True,
            ):
                st.session_state["page"] = page_name
                st.rerun()

        st.markdown(
            '<hr style="border-color:rgba(79,142,247,0.15);margin:0.75rem 0;">',
            unsafe_allow_html=True,
        )

        # ── Settings Section ─────────────────────────────────────
        st.markdown(
            '<div style="font-size:0.72rem;color:#606880;font-weight:700;letter-spacing:1.5px;'
            'text-transform:uppercase;margin-bottom:0.5rem;padding:0 0.3rem;">⚙️ Settings</div>',
            unsafe_allow_html=True,
        )

        with st.expander("🎛️ Detection Settings", expanded=False):
            s = st.session_state["settings"]

            s["model_name"] = st.selectbox(
                "🧠 Model",
                ["Grounding DINO Base", "Grounding DINO Tiny"],
                index=["Grounding DINO Base", "Grounding DINO Tiny"].index(s["model_name"]),
                help="Base = higher accuracy; Tiny = faster inference",
            )

            s["box_threshold"] = st.slider(
                "🎯 Box Confidence",
                min_value=0.1, max_value=0.9, value=s["box_threshold"], step=0.05,
                help="Minimum confidence for a detection to be kept",
            )

            s["text_threshold"] = st.slider(
                "📝 Text Confidence",
                min_value=0.1, max_value=0.9, value=s["text_threshold"], step=0.05,
                help="Minimum text-alignment confidence for a label",
            )

            s["box_color"] = st.selectbox(
                "🎨 Box Color",
                ["Gradient (Auto)", "Cyan", "Purple", "Green", "Orange", "Pink"],
                index=["Gradient (Auto)", "Cyan", "Purple", "Green", "Orange", "Pink"].index(
                    s["box_color"]
                ),
            )

            s["font_size"] = st.slider(
                "🔤 Label Font Size",
                min_value=10, max_value=28, value=s["font_size"], step=2,
            )

            st.session_state["settings"] = s

        # Dark mode toggle (cosmetic)
        st.markdown(
            '<hr style="border-color:rgba(79,142,247,0.15);margin:0.75rem 0;">',
            unsafe_allow_html=True,
        )
        dark = st.toggle("🌙 Dark Mode", value=st.session_state["dark_mode"])
        st.session_state["dark_mode"] = dark

        # System info widget
        st.markdown(
            '<hr style="border-color:rgba(79,142,247,0.15);margin:0.75rem 0;">',
            unsafe_allow_html=True,
        )
        try:
            import torch
            device_label = "🟢 CUDA GPU" if torch.cuda.is_available() else "🔵 CPU"
        except ImportError:
            device_label = "❓ Unknown"

        run_count = len(st.session_state.get("perf_history", []))

        st.markdown(
            f"""
            <div style="font-size:0.75rem;color:#606880;padding:0 0.2rem;">
              <div style="margin-bottom:4px;">Device: <strong style="color:#4f8ef7;">{device_label}</strong></div>
              <div>Runs: <strong style="color:#9b59f7;">{run_count}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Footer
        st.markdown(
            """
            <div style="position:absolute;bottom:1rem;left:0;right:0;text-align:center;
                        font-size:0.72rem;color:#404660;">
              Moving Object Detection & Tracking<br>
              PyTorch · OpenCV · Streamlit
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Main Router ──────────────────────────────────────────────────────────────
def main():
    # Inject global CSS
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    render_sidebar()

    page     = st.session_state["page"]
    settings = st.session_state["settings"]

    if page == "🏠 Home":
        render_home()
    elif page == "🖼️ Image Detection":
        render_image_detection(settings)
    elif page == "🎥 Video Detection":
        render_video_detection(settings)
    elif page == "🦕 Model Info":
        render_about(settings)
    elif page == "📊 Performance":
        render_performance(settings)
    elif page == "📚 Documentation":
        render_documentation(settings)
    else:
        render_home()


if __name__ == "__main__":
    main()
