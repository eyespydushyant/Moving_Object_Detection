"""
Shared UI Styles and Components
Injects CSS and provides reusable Streamlit UI helpers.
"""

import streamlit as st


# ─────────────────────────────────────────────
# Global CSS
# ─────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ── Google Font ───────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root Variables ────────────────────────── */
:root {
  --bg-primary:    #0a0e1a;
  --bg-secondary:  #0f1629;
  --bg-card:       rgba(15, 22, 41, 0.85);
  --accent-blue:   #4f8ef7;
  --accent-purple: #9b59f7;
  --accent-cyan:   #00d4ff;
  --accent-pink:   #f759d4;
  --gradient-1:    linear-gradient(135deg, #4f8ef7 0%, #9b59f7 100%);
  --gradient-2:    linear-gradient(135deg, #00d4ff 0%, #4f8ef7 50%, #9b59f7 100%);
  --gradient-hero: linear-gradient(135deg, #0a0e1a 0%, #1a0a2e 50%, #0a1628 100%);
  --text-primary:  #e8eaf6;
  --text-secondary:#a0aec0;
  --border-color:  rgba(79, 142, 247, 0.2);
  --glass-bg:      rgba(15, 22, 41, 0.7);
  --glass-border:  rgba(79, 142, 247, 0.15);
  --shadow-glow:   0 0 30px rgba(79, 142, 247, 0.15);
}

/* ── Base ──────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg-primary) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--text-primary) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Main Content Area ─────────────────────── */
[data-testid="stMain"] {
  background: transparent !important;
}

.block-container {
  padding: 2rem 3rem !important;
  max-width: 1400px !important;
}

/* ── Sidebar ───────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a0e1a 0%, #0f1629 100%) !important;
  border-right: 1px solid var(--glass-border) !important;
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Headings ──────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Space Grotesk', sans-serif !important;
  color: var(--text-primary) !important;
}

/* ── Buttons ───────────────────────────────── */
.stButton > button {
  background: var(--gradient-1) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 0.6rem 1.8rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  letter-spacing: 0.5px !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 20px rgba(79, 142, 247, 0.3) !important;
}

.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 8px 30px rgba(79, 142, 247, 0.5) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ── Download Button ───────────────────────── */
.stDownloadButton > button {
  background: linear-gradient(135deg, #00d4ff 0%, #4f8ef7 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3) !important;
  transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(0, 212, 255, 0.5) !important;
}

/* ── Inputs & Text Areas ───────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
  background: var(--glass-bg) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
  font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--accent-blue) !important;
  box-shadow: 0 0 0 2px rgba(79, 142, 247, 0.2) !important;
}

/* ── Sliders ───────────────────────────────── */
.stSlider > div > div > div > div {
  background: var(--gradient-1) !important;
}

/* ── File Uploader ─────────────────────────── */
[data-testid="stFileUploader"] {
  background: var(--glass-bg) !important;
  border: 2px dashed var(--glass-border) !important;
  border-radius: 16px !important;
  transition: border-color 0.3s !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--accent-blue) !important;
}

/* ── Metrics ───────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--glass-bg) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 14px !important;
  padding: 1rem !important;
  backdrop-filter: blur(10px) !important;
}

[data-testid="stMetricValue"] {
  background: var(--gradient-1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.8rem !important;
  font-weight: 700 !important;
}

/* ── Expander ──────────────────────────────── */
.streamlit-expanderHeader {
  background: var(--glass-bg) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
  font-weight: 600 !important;
}

/* ── Progress Bar ──────────────────────────── */
.stProgress > div > div > div {
  background: var(--gradient-1) !important;
  border-radius: 99px !important;
}

.stProgress > div > div {
  background: rgba(255,255,255,0.05) !important;
  border-radius: 99px !important;
}

/* ── Tabs ──────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--glass-bg) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 9px !important;
  color: var(--text-secondary) !important;
  font-weight: 500 !important;
  transition: all 0.2s !important;
}

.stTabs [aria-selected="true"] {
  background: var(--gradient-1) !important;
  color: white !important;
}

/* ── Alerts & Messages ─────────────────────── */
.stSuccess {
  background: rgba(0, 212, 100, 0.1) !important;
  border: 1px solid rgba(0, 212, 100, 0.3) !important;
  border-radius: 10px !important;
  color: #00d464 !important;
}

.stWarning {
  background: rgba(255, 165, 0, 0.1) !important;
  border: 1px solid rgba(255, 165, 0, 0.3) !important;
  border-radius: 10px !important;
}

.stError {
  background: rgba(255, 50, 50, 0.1) !important;
  border: 1px solid rgba(255, 50, 50, 0.3) !important;
  border-radius: 10px !important;
}

/* ── Info ──────────────────────────────────── */
.stInfo {
  background: rgba(79, 142, 247, 0.1) !important;
  border: 1px solid rgba(79, 142, 247, 0.3) !important;
  border-radius: 10px !important;
}

/* ── Divider ───────────────────────────────── */
hr { border-color: var(--glass-border) !important; }

/* ── Scrollbar ─────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
  background: var(--gradient-1);
  border-radius: 99px;
}

/* ── Custom Card ───────────────────────────── */
.glass-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 1.5rem 2rem;
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-glow);
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.glass-card:hover {
  border-color: rgba(79, 142, 247, 0.4);
  box-shadow: 0 0 40px rgba(79, 142, 247, 0.2);
}

/* ── Hero Banner ───────────────────────────── */
.hero-banner {
  background: var(--gradient-hero);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 3rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  margin-bottom: 2rem;
}

.hero-banner::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(ellipse at center, rgba(79,142,247,0.08) 0%, transparent 60%);
  animation: pulse-bg 6s ease-in-out infinite;
}

@keyframes pulse-bg {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50%       { transform: scale(1.1); opacity: 1; }
}

/* ── Gradient Text ─────────────────────────── */
.gradient-text {
  background: var(--gradient-2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

/* ── Feature Badge ─────────────────────────── */
.feature-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(79, 142, 247, 0.1);
  border: 1px solid rgba(79, 142, 247, 0.25);
  border-radius: 8px;
  padding: 0.4rem 0.8rem;
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--accent-cyan);
  margin: 4px;
  transition: all 0.2s;
}

.feature-badge:hover {
  background: rgba(79, 142, 247, 0.2);
  border-color: var(--accent-blue);
}

/* ── Stat Card ─────────────────────────────── */
.stat-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 1.2rem;
  text-align: center;
  transition: all 0.3s;
  cursor: default;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(79, 142, 247, 0.5);
  box-shadow: 0 12px 40px rgba(79, 142, 247, 0.15);
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  font-family: 'Space Grotesk', sans-serif;
  background: var(--gradient-1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 0.82rem;
  color: var(--text-secondary);
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-top: 4px;
}

/* ── Glow Orb Animation ────────────────────── */
@keyframes float-glow {
  0%, 100% { transform: translateY(0px) scale(1); opacity: 0.6; }
  50%       { transform: translateY(-12px) scale(1.05); opacity: 1; }
}

.glow-orb {
  animation: float-glow 4s ease-in-out infinite;
}

/* ── Pulse Animation ───────────────────────── */
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.85); }
}

.pulse-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  background: #00d464;
  border-radius: 50%;
  animation: pulse-dot 1.5s ease-in-out infinite;
}

/* ── Sidebar Nav Item ──────────────────────── */
.sidebar-nav-item {
  padding: 0.5rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 4px;
  font-weight: 500;
}

.sidebar-nav-item:hover {
  background: rgba(79, 142, 247, 0.15);
}

/* ── Code Block ────────────────────────────── */
.stCodeBlock {
  border-radius: 12px !important;
  border: 1px solid var(--glass-border) !important;
}

/* ── Table ─────────────────────────────────── */
.stDataFrame {
  border-radius: 12px !important;
  overflow: hidden !important;
}

/* ── Toggle / Checkbox ─────────────────────── */
.stCheckbox > label, .stToggle > label {
  color: var(--text-primary) !important;
}
</style>
"""


def inject_css():
    """Inject the global CSS into the Streamlit app."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Reusable Components
# ─────────────────────────────────────────────
def glass_card(content_html: str, extra_class: str = ""):
    """Render a glassmorphism card with arbitrary HTML content."""
    st.markdown(
        f'<div class="glass-card {extra_class}">{content_html}</div>',
        unsafe_allow_html=True,
    )


def gradient_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a gradient page header."""
    st.markdown(
        f"""
        <div style="margin-bottom:1.5rem;">
          <h1 style="margin:0;font-size:2.2rem;font-family:'Space Grotesk',sans-serif;">
            {icon} <span class="gradient-text">{title}</span>
          </h1>
          {"<p style='color:#a0aec0;margin-top:0.4rem;font-size:1.05rem;'>" + subtitle + "</p>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_badges(features: list):
    """Render a row of feature badges."""
    badges_html = "".join(
        f'<span class="feature-badge">✓ {f}</span>' for f in features
    )
    st.markdown(f'<div style="line-height:2.4;">{badges_html}</div>', unsafe_allow_html=True)


def stat_cards(stats: dict):
    """
    Render a row of stat cards.

    Args:
        stats: dict mapping label -> (value, icon)
    """
    cols = st.columns(len(stats))
    for col, (label, (value, icon)) in zip(cols, stats.items()):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                  <div style="font-size:1.8rem;margin-bottom:4px;">{icon}</div>
                  <div class="stat-value">{value}</div>
                  <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def divider_with_label(label: str):
    """Render a horizontal divider with a centered label."""
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:1rem;margin:1.5rem 0;">
          <div style="flex:1;height:1px;background:var(--glass-border);"></div>
          <span style="color:var(--text-secondary);font-size:0.85rem;font-weight:600;
                       letter-spacing:1px;text-transform:uppercase;">{label}</span>
          <div style="flex:1;height:1px;background:var(--glass-border);"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_box(text: str, icon: str = "ℹ️"):
    """Render a styled info box."""
    st.markdown(
        f"""
        <div style="background:rgba(79,142,247,0.08);border:1px solid rgba(79,142,247,0.25);
                    border-radius:12px;padding:1rem 1.2rem;display:flex;gap:0.75rem;
                    align-items:flex-start;margin:0.5rem 0;">
          <span style="font-size:1.2rem;">{icon}</span>
          <span style="color:#a8c4f5;font-size:0.92rem;line-height:1.6;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
