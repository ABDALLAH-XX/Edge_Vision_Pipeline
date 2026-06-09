import './App.css'

function App() {
  return (
    <div className="app-container">
      <h1>Vision Ordinateur - Inférence Déportée</h1>
      
      <div className="video-container">
        <img 
          src="http://127.0.0.1:8000/video_feed" 
          alt="Flux vidéo YOLOv8 OpenVINO INT8" 
        />
      </div>

      <div className="footer">
        Backend : FastAPI + OpenVINO INT8 (320px) | Frontend : React + Vite
      </div>
    </div>
  )
}

export default App