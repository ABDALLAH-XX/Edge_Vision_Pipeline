import './App.css'

function App() {
  return (
    <div className="app-container">
      <h1>Vision Ordinateur - Inférence Déportée Frontend (React)</h1>
      
      <div className="video-container">
        {/* On pointe directement vers le flux vidéo de ton FastAPI */}
        <img 
          src="http://127.0.0.1:8000/video_feed" 
          alt="Flux vidéo YOLOv8 en direct" 
        />
      </div>

      <div className="footer">
        Backend : FastAPI + OpenVINO INT8 | Frontend : React + Vite
      </div>
    </div>
  )
}

export default App