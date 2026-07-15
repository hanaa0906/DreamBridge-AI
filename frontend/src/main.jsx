import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import UploadPage from './pages/UploadPage.jsx'
import LessonPage from './pages/LessonPage.jsx'
import DashboardPage from './pages/DashboardPage.jsx'
import './styles.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <header className="app-header">
          <h1>DreamBridge AI</h1>
          <nav>
            <NavLink to="/" end>Upload</NavLink>
            <NavLink to="/dashboard">Teacher Dashboard</NavLink>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/lessons/:lessonId" element={<LessonPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
