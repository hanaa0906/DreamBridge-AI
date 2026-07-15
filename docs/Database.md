# DreamBridge AI — Database Schema

SQLite for dev (via SQLAlchemy), swap to PostgreSQL for production by changing
`DATABASE_URL` in `.env` — no code changes needed since SQLAlchemy abstracts it.

## Tables

### users
| column | type | notes |
|---|---|---|
| id | int, PK | |
| name | str | |
| email | str, unique | |
| role | str | `teacher` \| `student` |

### lessons
| column | type | notes |
|---|---|---|
| id | int, PK | |
| teacher_id | int, FK -> users.id | |
| title | str | |
| file_path | str | stored file location |
| content_text | text, nullable | filled by extraction module |
| summary | text, nullable | filled by summarizer |
| created_at | datetime | |

### student_profiles
| column | type | notes |
|---|---|---|
| student_id | int, PK, FK -> users.id | |
| language | str | e.g. `ta`, `en`, `hi` |
| learning_style | str | `visual` \| `auditory` \| `reading` \| `kinesthetic` |
| accessibility_type | str | `none` \| `dyslexia` \| `low_vision` \| `hearing_impaired` |
| difficulty | str | `beginner` \| `intermediate` \| `advanced` |

### personalized_lessons
| column | type | notes |
|---|---|---|
| id | int, PK | |
| lesson_id | int, FK -> lessons.id | |
| student_id | int, FK -> users.id | |
| adapted_text | text | |
| language | str | |
| format_notes | text | e.g. "large font, high contrast" |
| created_at | datetime | |

### quizzes
| column | type | notes |
|---|---|---|
| id | int, PK | |
| lesson_id | int, FK -> lessons.id | |
| questions_json | text | serialized list of {question, options, answer} |
| created_at | datetime | |

### progress
| column | type | notes |
|---|---|---|
| id | int, PK | |
| student_id | int, FK -> users.id | |
| lesson_id | int, FK -> lessons.id | |
| score | float, nullable | |
| time_spent_seconds | int | |
| created_at | datetime | |

### chat_messages
| column | type | notes |
|---|---|---|
| id | int, PK | |
| lesson_id | int, FK -> lessons.id | |
| student_id | int, FK -> users.id | |
| role | str | `user` \| `assistant` |
| content | text | |
| created_at | datetime | |
