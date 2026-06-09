import os
import time
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware 
from ultralytics import YOLO

# Verrous CPU pour OpenVINO sous Linux / Hub de calcul
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

app = FastAPI(title="YOLOv8 Web Streaming Server - Production")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement UNIQUE du modèle optimisé
print("Chargement du modèle de production (OpenVINO INT8)...")
model_opti = YOLO("yolov8n_int8_openvino_model/", task="detect")
print("Modèle prêt.")


def generate_frames():
    """Générateur de flux webcam optimisé haute performance"""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    prev_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            # Inférence ultra-rapide (taille 320)
            results = model_opti.predict(
                frame, verbose=False, conf=0.15, imgsz=320, device="cpu"
            )
            annotated_frame = results[0].plot()

            # Calcul des FPS réels
            new_time = time.time()
            fps = 1 / (new_time - prev_time)
            prev_time = new_time

            # Badge 1 : Statut du modèle (Vert)
            status_text = "YOLOv8 INT8"
            (text_w, text_h), baseline = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(annotated_frame, (20, 35 - text_h - 6), (20 + text_w + 6, 35 + baseline + 6), (0, 0, 0), thickness=cv2.FILLED)
            cv2.putText(annotated_frame, status_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

            # Badge 2 : Compteur de FPS (Jaune)
            fps_text = f"FPS: {int(fps)}"
            (fps_w, fps_h), fps_baseline = cv2.getTextSize(fps_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            fps_x = annotated_frame.shape[1] - fps_w - 20
            cv2.rectangle(annotated_frame, (fps_x - 6, 35 - fps_h - 6), (fps_x + fps_w + 6, 35 + fps_baseline + 6), (0, 0, 0), thickness=cv2.FILLED)
            cv2.putText(annotated_frame, fps_text, (fps_x, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)

            # Encodage et envoi
            ret, buffer = cv2.imencode(".jpg", annotated_frame)
            if not ret:
                continue

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
            
    finally:
        cap.release()


@app.get("/video_feed")
def video_feed():
    """Route unique simplifiée pour le Frontend"""
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)