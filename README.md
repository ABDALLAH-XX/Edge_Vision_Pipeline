# Edge Vision Pipeline 

![Docker Build Status](https://img.shields.io/badge/Docker%20Build-passing-brightgreen?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

This project is a computer vision pipeline optimized for deployment on consumer-grade or embedded hardware (*Edge AI*). It features a **YOLOv8 nano** model quantized in **INT8** and powered by Intel's **OpenVINO** accelerator.

The application is fully decoupled using a modern **Multi-Container Architecture** (FastAPI + React), orchestrated by **Docker Compose**.

---

## 🏗️ Project Architecture

The system is divided into two main services that communicate asynchronously:

* **Backend (FastAPI)**: Manages local webcam capture via OpenCV, executes ultra-fast AI inference using OpenVINO (with input resolution optimized to 320 to maximize performance), and exposes a live video streaming feed over standard HTTP MJPEG.
* **Frontend (React + Vite)**: A modern and responsive web interface that consumes the live video feed and displays it in an optimized dark-themed dashboard.

---

## ⚡ Hardware Optimisations (Edge AI)

To ensure maximum fluidity and a high refresh rate (~15-30 FPS depending on the host machine) even on entry-level processors (e.g., AMD Athlon / Intel Celeron), several key optimizations have been implemented:

1. **INT8 Quantization**: The original YOLOv8n model was converted to the OpenVINO format and compressed to 8-bit integer (`INT8`) precision, drastically reducing memory footprint and CPU compute time.
2. **Adapted Inference Resolution (`imgsz=320`)**: The webcam frame is downscaled for AI analysis without affecting the user display resolution, dividing the computational load by 4.
3. **CPU Thread Locking**: OpenVINO is strictly restricted to a single compute thread via the `OMP_NUM_THREADS=1` and `MKL_NUM_THREADS=1` environment variables. This prevents global CPU saturation and preserves vital resources for FastAPI and the web server to remain perfectly smooth.

---

## 🛠️ Prerequisites

Before launching the project, make sure you have installed:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

> **Note for Linux users (Ubuntu/Debian)**: Your user must belong to the `docker` group so that the container can natively access your physical webcam device (`/dev/video0`).

---

## 🚀 Quick Start

Thanks to Docker Compose, the entire environment (Python requirements installation, Node.js packages, build, and networking) starts with a single command.

1. Open a terminal at the root of the project.
2. Run the following command:

```bash
docker compose up --build
```
3. Once the containers are running, open your browser and access the application:

-   Frontend (React): http://localhost:5173
-   Backend API (FastAPI): http://localhost:8000/docs

To stop the application, simply press Ctrl + C in your terminal.

---

## 📂 File Structure
```PlainText
Edge_Vision_Pipeline/
├── backend/
│   ├── yolov8n_int8_openvino_model/  # Quantized AI model folder
│   ├── main.py                       # FastAPI server & OpenCV loop
│   ├── requirements.txt              # Python dependencies (Ultralytics, OpenVINO...)
│   └── Dockerfile                    # Backend container environment
├── frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main React component (Consumes the video feed)
│   │   ├── App.css                   # Interface styling
│   │   └── main.jsx
│   ├── package.json                  # Node.js dependencies (React, Vite...)
│   └── Dockerfile                    # Frontend container environment
├── docker-compose.yml                # Orchestrator for Backend + Frontend services
└── README.md                         # Project documentation
```