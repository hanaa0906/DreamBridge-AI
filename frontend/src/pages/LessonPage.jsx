import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api.js'

export default function LessonPage() {
  const { lessonId } = useParams()
  const [lesson, setLesson] = useState(null)
  const [quiz, setQuiz] = useState(null)
  const [translated, setTranslated] = useState('')
  const [targetLang, setTargetLang] = useState('ta')
  const [studentId, setStudentId] = useState('2')
  const [profile, setProfile] = useState({
    language: 'ta',
    learning_style: 'visual',
    accessibility_type: 'dyslexia',
    difficulty: 'beginner',
  })
  const [personalized, setPersonalized] = useState(null)
  const [chatLog, setChatLog] = useState([])
  const [chatInput, setChatInput] = useState('')
  const [busy, setBusy] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    api.getLesson(lessonId).then(setLesson).catch((e) => setError(e.message))
  }, [lessonId])

  async function run(step, fn) {
    setBusy(step)
    setError('')
    try {
      await fn()
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy('')
    }
  }

  const doExtract = () => run('extract', async () => setLesson(await api.extractLesson(lessonId)))
  const doSummarize = () => run('summarize', async () => setLesson(await api.summarizeLesson(lessonId)))
  const doQuiz = () => run('quiz', async () => setQuiz(await api.quizLesson(lessonId, 5)))
  const doTranslate = () =>
    run('translate', async () => {
      const res = await api.translateLesson(lessonId, targetLang)
      setTranslated(res.translated_text)
    })
  const doSaveProfile = () =>
    run('profile', async () => api.upsertStudentProfile({ student_id: Number(studentId), ...profile }))
  const doPersonalize = () =>
    run('personalize', async () =>
      setPersonalized(await api.personalizeLesson(lessonId, Number(studentId)))
    )
  const doChat = () =>
    run('chat', async () => {
      const res = await api.tutorChat({ lesson_id: Number(lessonId), student_id: Number(studentId), message: chatInput })
      setChatLog((log) => [...log, { role: 'user', content: chatInput }, { role: 'assistant', content: res.reply }])
      setChatInput('')
    })

  if (!lesson) return <p>Loading…</p>

  return (
    <div>
      <div className="card">
        <h2>{lesson.title}</h2>
        {error && <p style={{ color: '#f87171' }}>{error}</p>}

        <button onClick={doExtract} disabled={busy === 'extract'}>
          {busy === 'extract' ? 'Extracting…' : '1. Extract content'}
        </button>{' '}
        <button onClick={doSummarize} disabled={!lesson.content_text || busy === 'summarize'}>
          {busy === 'summarize' ? 'Summarizing…' : '2. Summarize'}
        </button>{' '}
        <button onClick={doQuiz} disabled={!lesson.content_text || busy === 'quiz'}>
          {busy === 'quiz' ? 'Generating…' : '3. Generate quiz'}
        </button>

        {lesson.content_text && (
          <details style={{ marginTop: 12 }}>
            <summary>Extracted text</summary>
            <pre>{lesson.content_text}</pre>
          </details>
        )}
        {lesson.summary && (
          <details open style={{ marginTop: 12 }}>
            <summary>Summary</summary>
            <pre>{lesson.summary}</pre>
          </details>
        )}
        {quiz && (
          <details open style={{ marginTop: 12 }}>
            <summary>Quiz ({quiz.questions.length} questions)</summary>
            <ol>
              {quiz.questions.map((q, i) => (
                <li key={i}>
                  <strong>{q.question}</strong>
                  {q.options?.length > 0 && (
                    <ul>{q.options.map((o, j) => <li key={j}>{o}</li>)}</ul>
                  )}
                  <p style={{ color: 'var(--muted)' }}>Answer: {q.answer}</p>
                </li>
              ))}
            </ol>
          </details>
        )}
      </div>

      <div className="card">
        <h3>Translate</h3>
        <label>Target language code (e.g. ta, hi, es)</label>
        <input value={targetLang} onChange={(e) => setTargetLang(e.target.value)} />
        <button onClick={doTranslate} disabled={!lesson.content_text || busy === 'translate'}>
          {busy === 'translate' ? 'Translating…' : 'Translate'}
        </button>
        {translated && <pre style={{ marginTop: 12 }}>{translated}</pre>}
      </div>

      <div className="card">
        <h3>Student Profile &amp; Personalization</h3>
        <label>Student ID</label>
        <input value={studentId} onChange={(e) => setStudentId(e.target.value)} />

        <label>Language</label>
        <input value={profile.language} onChange={(e) => setProfile({ ...profile, language: e.target.value })} />

        <label>Learning style</label>
        <select value={profile.learning_style} onChange={(e) => setProfile({ ...profile, learning_style: e.target.value })}>
          <option value="visual">Visual</option>
          <option value="auditory">Auditory</option>
          <option value="reading">Reading</option>
          <option value="kinesthetic">Kinesthetic</option>
        </select>

        <label>Accessibility type</label>
        <select
          value={profile.accessibility_type}
          onChange={(e) => setProfile({ ...profile, accessibility_type: e.target.value })}
        >
          <option value="none">None</option>
          <option value="dyslexia">Dyslexia</option>
          <option value="low_vision">Low vision</option>
          <option value="hearing_impaired">Hearing impaired</option>
        </select>

        <label>Difficulty</label>
        <select value={profile.difficulty} onChange={(e) => setProfile({ ...profile, difficulty: e.target.value })}>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>

        <button onClick={doSaveProfile} disabled={busy === 'profile'}>
          {busy === 'profile' ? 'Saving…' : 'Save profile'}
        </button>{' '}
        <button onClick={doPersonalize} disabled={!lesson.content_text || busy === 'personalize'}>
          {busy === 'personalize' ? 'Personalizing…' : 'Generate personalized lesson'}
        </button>

        {personalized && (
          <details open style={{ marginTop: 12 }}>
            <summary>Personalized version ({personalized.format_notes})</summary>
            <pre>{personalized.adapted_text}</pre>
          </details>
        )}
      </div>

      <div className="card">
        <h3>AI Tutor</h3>
        <div style={{ marginBottom: 12 }}>
          {chatLog.map((m, i) => (
            <p key={i}>
              <strong>{m.role === 'user' ? 'You' : 'Tutor'}:</strong> {m.content}
            </p>
          ))}
        </div>
        <input
          value={chatInput}
          placeholder="Ask a question about this lesson…"
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && chatInput && doChat()}
        />
        <button onClick={doChat} disabled={!chatInput || !lesson.content_text || busy === 'chat'}>
          {busy === 'chat' ? 'Thinking…' : 'Send'}
        </button>
      </div>
    </div>
  )
}
