import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api.js'

export default function DashboardPage() {
  const [teacherId, setTeacherId] = useState('1')
  const [lessons, setLessons] = useState([])
  const [students, setStudents] = useState([])
  const [progressStudentId, setProgressStudentId] = useState('2')
  const [progress, setProgress] = useState([])
  const [error, setError] = useState('')

  async function load() {
    setError('')
    try {
      setLessons(await api.listTeacherLessons(teacherId))
      setStudents(await api.listStudents())
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => { load() }, [])

  async function loadProgress() {
    try {
      setProgress(await api.getProgress(progressStudentId))
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>Teacher Dashboard</h2>
        <label>Teacher ID</label>
        <input value={teacherId} onChange={(e) => setTeacherId(e.target.value)} />
        <button onClick={load}>Refresh</button>
        {error && <p style={{ color: '#f87171' }}>{error}</p>}

        <h3>Lessons</h3>
        <ul>
          {lessons.map((l) => (
            <li key={l.id}>
              <Link to={`/lessons/${l.id}`}>{l.title}</Link> — {l.summary ? 'summarized' : 'not summarized yet'}
            </li>
          ))}
          {lessons.length === 0 && <p style={{ color: 'var(--muted)' }}>No lessons yet.</p>}
        </ul>

        <h3>Students</h3>
        <ul>
          {students.map((s) => <li key={s.id}>#{s.id} — {s.name} ({s.email})</li>)}
          {students.length === 0 && <p style={{ color: 'var(--muted)' }}>No students yet.</p>}
        </ul>
      </div>

      <div className="card">
        <h3>Progress Analytics</h3>
        <label>Student ID</label>
        <input value={progressStudentId} onChange={(e) => setProgressStudentId(e.target.value)} />
        <button onClick={loadProgress}>Load progress</button>
        <table style={{ width: '100%', marginTop: 12, borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ textAlign: 'left', color: 'var(--muted)' }}>
              <th>Lesson</th><th>Score</th><th>Time spent (s)</th><th>Date</th>
            </tr>
          </thead>
          <tbody>
            {progress.map((p) => (
              <tr key={p.id}>
                <td>{p.lesson_id}</td>
                <td>{p.score ?? '—'}</td>
                <td>{p.time_spent_seconds}</td>
                <td>{new Date(p.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
