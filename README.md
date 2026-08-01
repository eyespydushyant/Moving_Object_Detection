# 🤖 Moving Object Detection & Tracking
### Powered by Grounding DINO Transformer + Hugging Face

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange?style=for-the-badge&logo=pytorch)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Final Year Engineering Project | Computer Vision & Deep Learning**

</div>

---

## 📋 Project Overview

A professional AI-powered web application for **moving object detection and tracking** using the
**Grounding DINO** transformer model from Hugging Face. The system detects objects in images and
videos using natural language text prompts — no fixed class list required.

### 🌟 Key Features

| Feature | Description |
|---------|-------------|
| 🖼️ **Image Detection** | Upload any image and detect objects with text prompts |
| 🎥 **Video Detection** | Process videos frame-by-frame with progress tracking |
| 🌐 **Open Vocabulary** | Detect any object — no fixed classes, no retraining |
| ⚡ **GPU Accelerated** | Automatic CUDA detection and utilization |
| 📊 **Performance Metrics** | Real-time inference stats, FPS, CPU/GPU monitoring |
| ⬇️ **Export Results** | Download annotated images (PNG) and videos (MP4) |
| 🎛️ **Configurable** | Adjustable confidence thresholds, colors, and model size |

---

## 🚀 Quick Start

### 1. Clone / Download
```bash
git clone <your-repo>
cd Moving_Object_Detection
```

### 2. Create Virtual Environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# or
source venv/bin/activate     # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

> The app will open at `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
Moving_Object_Detection/
│
├── app.py                      # 🚀 Main Streamlit application
│
├── pages/
│   ├── __init__.py
│   ├── home.py                 # 🏠 Hero page with project overview
│   ├── image_detection.py      # 🖼️ Image upload & detection
│   ├── video_detection.py      # 🎥 Video processing & output
│   ├── about.py                # 🦕 Model architecture info
│   ├── performance.py          # 📊 Metrics & monitoring
│   └── documentation.py        # 📚 Full project documentation
│
├── utils/
│   ├── __init__.py
│   ├── model.py                # 🧠 Model loading & inference
│   ├── image_processing.py     # 🖼️ Bounding box annotation
│   ├── video_processing.py     # 🎥 Frame-by-frame processing
│   └── styles.py               # 🎨 CSS & UI components
│
├── requirements.txt            # 📦 Python dependencies
└── README.md                   # 📄 This file
```

---

## 🦕 Model Information

| Property | Value |
|----------|-------|
| **Model** | IDEA-Research/grounding-dino-base |
| **Parameters** | ~172M |
| **Image Backbone** | Swin Transformer (Swin-B) |
| **Text Backbone** | BERT Encoder |
| **Detection Type** | Open-vocabulary (Zero-shot) |
| **Input** | Image + Text prompt |
| **Output** | Bounding boxes + Labels + Confidence |
| **COCO AP** | 57.2 AP (state-of-the-art) |

---

## 📖 How to Use

### Image Detection
1. Navigate to **Image Detection** in the sidebar
2. Upload a JPG, JPEG, or PNG image
3. Enter a text prompt (e.g., `person. car. bus. truck.`)
4. Adjust confidence thresholds in **Settings** if needed
5. Click **🔍 Detect Objects**
6. Download the annotated image

### Video Detection
1. Navigate to **Video Detection** in the sidebar
2. Upload an MP4, AVI, or MOV file
3. Enter a text prompt for detection
4. Set **Frame Skip** (1 = every frame, higher = faster)
5. Click **🚀 Process Video**
6. Monitor real-time progress stats
7. Download the annotated video

---

## ⚙️ Settings

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| Box Confidence | 0.35 | 0.1–0.9 | Minimum detection confidence |
| Text Confidence | 0.25 | 0.1–0.9 | Minimum text-alignment score |
| Box Color | Auto | Various | Bounding box color scheme |
| Font Size | 16 | 10–28 | Label text size |
| Model | Base | Tiny/Base | Model size (accuracy vs speed) |

---

## 🔧 Technical Requirements

- **Python** 3.9+
- **GPU** (Optional but recommended: 4GB+ VRAM for Base model)
- **RAM** 8GB+ recommended
- **Internet** Required for first-time model download (~680MB for Base)
- **Storage** ~2GB for model weights cache

---

## 📊 Performance Benchmarks

| Setup | Inference Time | Notes |
|-------|---------------|-------|
| NVIDIA RTX 3080 | ~0.3–0.5s/frame | GPU (CUDA) |
| NVIDIA T4 (Colab) | ~0.5–1.0s/frame | GPU (Colab) |
| CPU (Intel i7) | ~2–8s/frame | CPU only |

---

## 🙏 Credits & References

- [Grounding DINO Paper](https://arxiv.org/abs/2303.05499) — Liu et al. (2023)
- [IDEA-Research HuggingFace](https://huggingface.co/IDEA-Research) — Model weights
- [HuggingFace Transformers](https://github.com/huggingface/transformers) — Framework
- [Streamlit](https://streamlit.io) — Web framework

---


---

<div align="center">
Built with ❤️ | Computer Vision & Deep Learning
</div>
