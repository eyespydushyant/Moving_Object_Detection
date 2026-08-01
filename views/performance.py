"""
Performance Metrics Page
Displays inference statistics, FPS, GPU/CPU usage, and detection history.
"""

import time
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

from utils.styles import inject_css, gradient_header, divider_with_label, info_box, stat_cards


# ─────────────────────────────────────────────
# Helper: Dark Plotly Layout
# ─────────────────────────────────────────────
def _dark_layout(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title=title,
        title_font_size=14,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,22,41,0.6)",
        font_color="#c0cadc",
        font_family="Inter",
        margin=dict(l=20, r=20, t=45, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(79,142,247,0.2)"),
        xaxis=dict(gridcolor="rgba(79,142,247,0.1)", linecolor="rgba(79,142,247,0.2)"),
        yaxis=dict(gridcolor="rgba(79,142,247,0.1)", linecolor="rgba(79,142,247,0.2)"),
    )
    return fig


# ─────────────────────────────────────────────
# Render
# ─────────────────────────────────────────────
def render_performance(settings: dict):
    """Render the Performance Metrics page."""
    inject_css()
    gradient_header(
        "Performance Metrics",
        "Real-time inference statistics, system resource usage, and detection history",
        "📊",
    )

    history = st.session_state.get("perf_history", [])

    # ── Live System Stats ─────────────────────────────────────────
    divider_with_label("LIVE SYSTEM STATUS")

    sys_col, gpu_col = st.columns([1, 1], gap="large")

    with sys_col:
        st.markdown('<div class="glass-card" style="padding:1.5rem;">', unsafe_allow_html=True)
        st.markdown("#### 🖥️ CPU & Memory")

        if HAS_PSUTIL:
            cpu_pct = psutil.cpu_percent(interval=0.3)
            mem     = psutil.virtual_memory()
            mem_used_gb   = mem.used / 1e9
            mem_total_gb  = mem.total / 1e9
            mem_pct       = mem.percent

            st.metric("CPU Usage",    f"{cpu_pct:.1f}%")
            st.metric("RAM Used",     f"{mem_used_gb:.1f} / {mem_total_gb:.1f} GB")
            st.metric("RAM Usage",    f"{mem_pct:.1f}%")

            # CPU gauge
            fig_cpu = go.Figure(go.Indicator(
                mode="gauge+number",
                value=cpu_pct,
                domain={"x": [0, 1], "y": [0, 1]},
                number={"suffix": "%", "font": {"color": "#4f8ef7", "size": 28}},
                gauge={
                    "axis":  {"range": [0, 100], "tickcolor": "#a0aec0"},
                    "bar":   {"color": "#4f8ef7"},
                    "steps": [
                        {"range": [0, 50],   "color": "rgba(0,212,100,0.15)"},
                        {"range": [50, 80],  "color": "rgba(255,165,0,0.15)"},
                        {"range": [80, 100], "color": "rgba(255,50,50,0.15)"},
                    ],
                    "bgcolor":   "rgba(15,22,41,0.6)",
                    "bordercolor": "rgba(79,142,247,0.3)",
                },
            ))
            _dark_layout(fig_cpu, "CPU Usage (%)")
            fig_cpu.update_layout(height=220)
            st.plotly_chart(fig_cpu, use_container_width=True)
        else:
            st.warning("psutil not installed — system stats unavailable.")
        st.markdown("</div>", unsafe_allow_html=True)

    with gpu_col:
        st.markdown('<div class="glass-card" style="padding:1.5rem;">', unsafe_allow_html=True)
        st.markdown("#### 🎮 GPU Status")

        if HAS_TORCH and torch.cuda.is_available():
            gpu_name  = torch.cuda.get_device_name(0)
            props     = torch.cuda.get_device_properties(0)
            total_mem = props.total_memory / 1e9
            used_mem  = torch.cuda.memory_allocated(0) / 1e9
            pct       = (used_mem / total_mem) * 100

            st.metric("GPU",      gpu_name[:30])
            st.metric("VRAM Used",f"{used_mem:.2f} / {total_mem:.2f} GB")
            st.metric("VRAM %",   f"{pct:.1f}%")

            fig_gpu = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct,
                domain={"x": [0, 1], "y": [0, 1]},
                number={"suffix": "%", "font": {"color": "#9b59f7", "size": 28}},
                gauge={
                    "axis":  {"range": [0, 100], "tickcolor": "#a0aec0"},
                    "bar":   {"color": "#9b59f7"},
                    "steps": [
                        {"range": [0, 60],   "color": "rgba(0,212,100,0.15)"},
                        {"range": [60, 85],  "color": "rgba(255,165,0,0.15)"},
                        {"range": [85, 100], "color": "rgba(255,50,50,0.15)"},
                    ],
                    "bgcolor":   "rgba(15,22,41,0.6)",
                    "bordercolor": "rgba(155,89,247,0.3)",
                },
            ))
            _dark_layout(fig_gpu, "GPU VRAM Usage (%)")
            fig_gpu.update_layout(height=220)
            st.plotly_chart(fig_gpu, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="text-align:center;padding:2rem;color:#a0aec0;">
                  <div style="font-size:3rem;margin-bottom:0.5rem;">💻</div>
                  <div style="font-size:1rem;font-weight:600;color:#4f8ef7;">Running on CPU</div>
                  <div style="font-size:0.85rem;margin-top:0.3rem;">
                    No CUDA GPU detected. Install CUDA-enabled PyTorch for GPU acceleration.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Auto-refresh ──────────────────────────────────────────────
    if st.button("🔄 Refresh System Stats", use_container_width=False):
        st.rerun()

    # ── Inference History ─────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    divider_with_label("INFERENCE HISTORY")

    if not history:
        info_box(
            "No inference history yet. Run Image or Video detection first to populate metrics here.",
            "📈",
        )
        # Show demo charts with synthetic data
        st.markdown("#### 📊 Sample Chart Preview (Demo Data)")
        demo_times = np.random.uniform(0.4, 2.5, 10).tolist()
        demo_dets  = np.random.randint(0, 8, 10).tolist()
        _render_history_charts(
            [{"inference_time": t, "detections": d, "type": "Demo", "avg_confidence": 0.7, "timestamp": time.time()}
             for t, d in zip(demo_times, demo_dets)],
            demo=True,
        )
        return

    # ── Summary Metrics ───────────────────────────────────────────
    inf_times   = [h["inference_time"] for h in history]
    detections  = [h["detections"] for h in history]
    confidences = [h["avg_confidence"] for h in history if h["avg_confidence"] > 0]

    stat_cards({
        "Total Runs":     (len(history),                           "🏃"),
        "Avg Inf. Time":  (f"{np.mean(inf_times)*1000:.0f} ms",   "⏱️"),
        "Best Inf. Time": (f"{np.min(inf_times)*1000:.0f} ms",    "⚡"),
        "Avg Detections": (f"{np.mean(detections):.1f}",          "🎯"),
        "Avg Confidence": (f"{np.mean(confidences)*100:.0f}%" if confidences else "N/A", "📊"),
    })

    st.markdown("<br>", unsafe_allow_html=True)
    _render_history_charts(history)

    # ── Raw Table ─────────────────────────────────────────────────
    with st.expander("📋 Raw Inference Log"):
        import pandas as pd
        rows = []
        for i, h in enumerate(history):
            rows.append({
                "Run #":          i + 1,
                "Type":           h["type"],
                "Inference (ms)": f"{h['inference_time']*1000:.1f}",
                "Detections":     h["detections"],
                "Avg Confidence": f"{h['avg_confidence']*100:.1f}%",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    if st.button("🗑️ Clear History", use_container_width=False):
        st.session_state["perf_history"] = []
        st.success("History cleared.")
        st.rerun()


def _render_history_charts(history: list, demo: bool = False):
    """Render inference history charts."""
    c1, c2 = st.columns(2, gap="large")

    inf_times  = [h["inference_time"] * 1000 for h in history]
    detections = [h["detections"] for h in history]
    indices    = list(range(1, len(history) + 1))
    types      = [h["type"] for h in history]

    with c1:
        # Inference Time line chart
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=indices,
            y=inf_times,
            mode="lines+markers",
            name="Inference Time (ms)",
            line=dict(color="#4f8ef7", width=2.5),
            marker=dict(size=8, color="#4f8ef7", line=dict(width=2, color="#fff")),
            fill="tozeroy",
            fillcolor="rgba(79,142,247,0.1)",
        ))
        _dark_layout(fig1, "⏱️ Inference Time per Run (ms)")
        fig1.update_xaxes(title_text="Run #")
        fig1.update_yaxes(title_text="Time (ms)")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        # Detection count bar chart
        colors = ["#9b59f7" if t == "Video" else "#4f8ef7" for t in types]
        fig2 = go.Figure(go.Bar(
            x=indices,
            y=detections,
            marker_color=colors,
            name="Detections",
        ))
        _dark_layout(fig2, "🎯 Detections per Run")
        fig2.update_xaxes(title_text="Run #")
        fig2.update_yaxes(title_text="Object Count")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2, gap="large")
    with c3:
        # Type distribution pie
        from collections import Counter
        type_counts = Counter(types)
        fig3 = go.Figure(go.Pie(
            labels=list(type_counts.keys()),
            values=list(type_counts.values()),
            marker=dict(colors=["#4f8ef7", "#9b59f7", "#00d4ff"]),
            hole=0.5,
        ))
        _dark_layout(fig3, "🗂️ Run Type Distribution")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        # FPS indicator (1000 / avg_inf_time)
        avg_inf = float(np.mean(inf_times)) if inf_times else 1000
        fps_val = 1000.0 / max(avg_inf, 1)
        fig4 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=fps_val,
            delta={"reference": 5, "increasing": {"color": "#00d464"}, "decreasing": {"color": "#ff6b6b"}},
            number={"suffix": " FPS", "font": {"color": "#00d4ff", "size": 28}},
            gauge={
                "axis":  {"range": [0, 30], "tickcolor": "#a0aec0"},
                "bar":   {"color": "#00d4ff"},
                "steps": [
                    {"range": [0, 5],  "color": "rgba(255,50,50,0.15)"},
                    {"range": [5, 15], "color": "rgba(255,165,0,0.15)"},
                    {"range": [15, 30],"color": "rgba(0,212,100,0.15)"},
                ],
                "bgcolor":     "rgba(15,22,41,0.6)",
                "bordercolor": "rgba(0,212,255,0.3)",
            },
            title={"text": "Effective FPS", "font": {"color": "#a0aec0"}},
        ))
        _dark_layout(fig4, "⚡ Average Inference FPS")
        st.plotly_chart(fig4, use_container_width=True)
