import os
import time
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware 
from ultralytics import YOLO

# Verrous CPU pour OpenVINO sous Linux
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

app = FastAPI(title="YOLOv8 Web Streaming Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle optimisé OpenVINO INT8 (en résolution 320)
model = YOLO("yolov8n_int8_openvino_model/", task="detect")


def generate_frames():
    """Générateur de frames : capture, inférence et encodage en continu"""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Initialisation du temps pour le calcul des FPS
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Inférence YOLO ultra-rapide (taille 320)
        results = model.predict(
            frame, verbose=False, conf=0.15, imgsz=320, device="cpu"
        )

        # 2. Dessiner les boîtes directement sur l'image côté serveur
        annotated_frame = results[0].plot()

        # 3. Calcul du FPS réel du traitement backend
        new_time = time.time()
        fps = 1 / (new_time - prev_time)
        prev_time = new_time

        # 4. Incrustation du texte FPS sur l'image annotée
        cv2.putText(
            annotated_frame,
            f"FPS Serveur: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        # 5. Encodage du frame final en JPEG
        ret, buffer = cv2.imencode(".jpg", annotated_frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        # 6. Formatage spécial MJPEG pour le streaming web (Norme HTTP)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

    cap.release()


@app.get("/video_feed")
def video_feed():
    """Cette route expose le flux vidéo en direct pour le Frontend"""
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)