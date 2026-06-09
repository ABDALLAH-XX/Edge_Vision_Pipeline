# Edge Vision Pipeline

![Docker Build Status](https://img.shields.io/badge/Docker%20Build-passing-brightgreen?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

A computer vision pipeline optimized for **Edge AI** deployment on consumer-grade hardware.
YOLOv8n quantized in **INT8** via Intel OpenVINO achieves a **×3.4 FPS speedup** over FP32
on CPU — no GPU required.

Fully containerized with **Docker Compose** (FastAPI backend + React frontend).

---

## Benchmark Results

Evaluated on 150 frames of `Edge_Vision_Pipeline/backend/pedestrian.mp4` — full pipeline cycle  
(frame read + inference + bounding box drawing), CPU only, with model warmup.

| Metric | PyTorch FP32 (640px) | OpenVINO INT8 (320px) | Speedup |
|---|---|---|---|
| FPS mean | 4.3 | 17.5 | **×4.07** |
| FPS median | 4.3 | 17.8 | **×4.14** |
| FPS min | 2.2 | 8.1 | — |
| FPS max | 5.4 | 19.4 | — |
| Frames tested | 200 | 200 | — |

> Hardware: AMD Athlon 300U, 8GB RAM, Ubuntu — no dedicated GPU.  
> Note: INT8 model runs at imgsz=320 vs imgsz=640 for FP32.  
> The speedup combines both INT8 quantization and resolution reduction effects.

---

## Project Architecture

The system is divided into two decoupled services:

* **Backend (FastAPI)**: Webcam capture via OpenCV, INT8 inference via OpenVINO,
  live MJPEG streaming over HTTP.
* **Frontend (React + Vite)**: Responsive dark-themed dashboard consuming the live feed.

```plaintext
Edge_Vision_Pipeline/
├── backend/
│   ├── yolov8n_int8_openvino_model/  # Quantized AI model
│   ├── main.py                       # FastAPI server & OpenCV loop
│   ├── requirements.txt              # Python dependencies
│   ├── pedestrian.mp4                # Test video
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main React component
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Hardware Optimizations

1. **INT8 Quantization**: YOLOv8n converted to OpenVINO INT8 — reduced memory
   footprint and CPU compute time.
2. **Inference Resolution (imgsz=320)**: Input downscaled for inference only,
   dividing computational load by 4 vs. 640px.
3. **CPU Thread Locking**: `OMP_NUM_THREADS=1` and `MKL_NUM_THREADS=1` prevent
   CPU saturation and keep the web server responsive.

---

## Quick Start

Requires [Docker](https://docs.docker.com/get-docker/) and
[Docker Compose](https://docs.docker.com/compose/install/).

> **Linux users**: your user must belong to the `docker` group for webcam
> access (`/dev/video0`).

```bash
docker compose up --build
```

Once running:
- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs

Press `Ctrl+C` to stop.

---

## License

MIT