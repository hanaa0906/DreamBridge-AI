import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api.js'

export default function UploadPage() {
  const navigate = useNavigate()
  const [title, setTitle] = useState('')
  const [teacherId, setTeacherId] = useState('1')
  const [file, setFile] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) {
      setError('Choose a file first.')
      return
    }
    setBusy(true)
    setError('')
    try {
      const formData = new FormData()
      formData.append('title', title)
      formData.append('teacher_id', teacherId)
      formData.append('file', file)
      const lesson = await api.uploadLesson(formData)
      navigate(`/lessons/${lesson.id}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="card">
      <h2>Upload a Lesson</h2>
      <p style={{ color: 'var(--muted)' }}>
        Upload a PDF, image, or text file. DreamBridge will extract the content and
        let you generate personalized versions, quizzes, translations, and an AI tutor
        for it.
      </p>
      <form onSubmit={handleSubmit}>
        <label>Lesson title</label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} required />

        <label>Teacher ID</label>
        <input value={teacherId} onChange={(e) => setTeacherId(e.target.value)} required />

        <label>File (.pdf, .png, .jpg, .txt)</label>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} required />

        {error && <p style={{ color: '#f87171' }}>{error}</p>}
        <button type="submit" disabled={busy}>{busy ? 'Uploading…' : 'Upload lesson'}</button>
      </form>
    </div>
  )
}
