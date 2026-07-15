const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: options.body instanceof FormData ? undefined : { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText)
    throw new Error(`API error ${res.status}: ${text}`)
  }
  return res.json()
}

export const api = {
  createUser: (payload) => request('/users', { method: 'POST', body: JSON.stringify(payload) }),

  uploadLesson: (formData) => request('/upload', { method: 'POST', body: formData }),
  extractLesson: (lessonId) => request(`/lessons/${lessonId}/extract`, { method: 'POST' }),
  summarizeLesson: (lessonId) => request(`/lessons/${lessonId}/summarize`, { method: 'POST' }),
  quizLesson: (lessonId, numQuestions = 5) =>
    request(`/lessons/${lessonId}/quiz?num_questions=${numQuestions}`, { method: 'POST' }),
  translateLesson: (lessonId, targetLanguage) =>
    request(`/lessons/${lessonId}/translate`, {
      method: 'POST',
      body: JSON.stringify({ target_language: targetLanguage, use_summary: true }),
    }),
  personalizeLesson: (lessonId, studentId) =>
    request(`/lessons/${lessonId}/personalize`, {
      method: 'POST',
      body: JSON.stringify({ student_id: studentId }),
    }),
  getLesson: (lessonId) => request(`/lessons/${lessonId}`),

  upsertStudentProfile: (payload) => request('/students', { method: 'POST', body: JSON.stringify(payload) }),
  getStudentProfile: (studentId) => request(`/students/${studentId}`),

  tutorChat: (payload) => request('/tutor/chat', { method: 'POST', body: JSON.stringify(payload) }),

  logProgress: (payload) => request('/progress', { method: 'POST', body: JSON.stringify(payload) }),
  getProgress: (studentId) => request(`/progress/${studentId}`),

  listTeacherLessons: (teacherId) => request(`/teacher/lessons?teacher_id=${teacherId}`),
  listStudents: () => request('/teacher/students'),
}
