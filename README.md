# 🎯 SkillMatch AI

> **AI-powered resume–job matching platform** that uses NLP (spaCy + TF-IDF) and advanced Data Structures (Trie + Graph) to match resumes to jobs, detect skill gaps, and generate dependency-ordered learning roadmaps.

![SkillMatch AI](https://img.shields.io/badge/SkillMatch-AI-6366f1?style=for-the-badge&logo=sparkles)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18.2-61dafb?style=for-the-badge&logo=react)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Option 1: Docker Compose (Recommended)](#option-1-docker-compose-recommended)
  - [Option 2: Manual Local Setup](#option-2-manual-local-setup)
- [🔧 Environment Variables](#-environment-variables)
- [📡 API Reference](#-api-reference)
- [🖥️ Frontend Pages](#️-frontend-pages)
- [🧠 DSA Components](#-dsa-components)
- [🛠️ Tech Stack](#️-tech-stack)
- [🧪 Running Tests](#-running-tests)
- [📦 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Parsing** | Upload PDF, DOCX, or TXT resumes. Extracts skills, experience, education, and projects using spaCy NLP. |
| 🎯 **AI Job Matching** | TF-IDF cosine similarity engine matches resumes against job descriptions with scored results. |
| 🌲 **Skill Trie** | O(k) prefix search over 100+ known skills for instant autocomplete and skill normalization. |
| 🕸️ **Skill Graph** | Directed dependency graph enabling topological-sort-based learning roadmap generation. |
| 🗺️ **Roadmap Generator** | Identifies skill gaps and produces an ordered learning path from beginner → expert. |
| 📊 **Visual Dashboard** | Interactive charts showing match scores, skill overlap, and learning progression. |
| 🐳 **Docker Ready** | Full Docker Compose stack with MongoDB, PostgreSQL, backend, and frontend services. |
| 🔒 **In-Memory Fallback** | Thread-safe in-memory store runs the app fully locally without any database. |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SkillMatch AI                            │
│                                                                 │
│  ┌──────────────┐     HTTP/REST      ┌──────────────────────┐   │
│  │   React 18   │ ◄─────────────── ► │   FastAPI Backend    │   │
│  │  (Vite + TS) │                    │                      │   │
│  │              │                    │  ┌────────────────┐  │   │
│  │  Pages:      │                    │  │  Resume Parser │  │   │
│  │  • Landing   │                    │  │  spaCy + NLP   │  │   │
│  │  • Upload    │                    │  └────────────────┘  │   │
│  │  • Jobs      │                    │  ┌────────────────┐  │   │
│  │  • Results   │                    │  │  Skill Trie    │  │   │
│  │  • Roadmap   │                    │  │  (Prefix O(k)) │  │   │
│  └──────────────┘                    │  └────────────────┘  │   │
│                                      │  ┌────────────────┐  │   │
│                                      │  │  Skill Graph   │  │   │
│                                      │  │ (DAG + TopoSort│  │   │
│                                      │  └────────────────┘  │   │
│                                      │  ┌────────────────┐  │   │
│                                      │  │  TF-IDF Matcher│  │   │
│                                      │  │  Cosine Sim    │  │   │
│                                      │  └────────────────┘  │   │
│                                      └──────────┬───────────┘   │
│                                                 │               │
│                           ┌─────────────────────┴────────────┐  │
│                           │         Data Layer               │  │
│                           │  ┌──────────┐  ┌──────────────┐  │  │
│                           │  │ MongoDB  │  │  PostgreSQL  │  │  │
│                           │  │(Resumes/ │  │  (Jobs/      │  │  │
│                           │  │ Results) │  │   Users)     │  │  │
│                           │  └──────────┘  └──────────────┘  │  │
│                           └──────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
skillmatcher/
├── 📄 docker-compose.yml          # Full stack orchestration
├── 📄 .gitignore
├── 📄 README.md
│
├── 🔵 backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example               # Environment variable template
│   ├── tests/
│   │   └── ...                    # Unit & integration tests
│   └── app/
│       ├── main.py                # FastAPI application entry point
│       ├── core/
│       │   ├── config.py          # Pydantic settings management
│       │   └── database.py        # MongoDB & PostgreSQL connections
│       ├── routers/
│       │   ├── resume.py          # POST /resume/upload, GET /resume/{id}
│       │   ├── jobs.py            # GET /jobs, POST /jobs
│       │   ├── match.py           # POST /match — AI matching engine
│       │   └── skills.py          # GET /skills, GET /skills/search/{prefix}
│       ├── services/
│       │   ├── resume_parser.py   # spaCy NLP parser (PDF/DOCX/TXT)
│       │   ├── skill_trie.py      # Trie data structure with 100+ skills
│       │   ├── skill_graph.py     # DAG with topological sort
│       │   ├── matcher.py         # TF-IDF cosine similarity matching
│       │   └── roadmap.py         # Learning roadmap generator
│       ├── models/
│       │   └── schemas.py         # Pydantic request/response models
│       └── utils/
│           └── store.py           # In-memory thread-safe data store
│
└── 🟣 frontend/
    ├── Dockerfile
    ├── nginx.conf                 # Production nginx config
    ├── vite.config.js
    ├── package.json
    ├── index.html
    └── src/
        ├── main.jsx               # React entry point
        ├── App.jsx                # Router + layout
        ├── index.css              # Global styles & design tokens
        ├── pages/
        │   ├── LandingPage.jsx    # Hero, features, CTA
        │   ├── UploadPage.jsx     # Drag-and-drop resume upload
        │   ├── JobsPage.jsx       # Browse & select job postings
        │   ├── ResultPage.jsx     # Match scores + skill gap analysis
        │   └── RoadmapPage.jsx    # Visual learning roadmap
        ├── hooks/
        │   └── useAppContext.jsx  # Global app state context
        ├── components/
        │   └── ...                # Reusable UI components
        └── utils/
            └── api.js             # Axios API client
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Notes |
|---|---|---|
| **Docker** | 24+ | For Docker Compose setup |
| **Docker Compose** | v2+ | Bundled with Docker Desktop |
| **Python** | 3.10+ | For manual backend setup |
| **Node.js** | 18+ | For manual frontend setup |

---

### Option 1: Docker Compose (Recommended)

This spins up the **entire stack** (backend + frontend + MongoDB + PostgreSQL) with a single command.

```bash
# 1. Clone the repository
git clone https://github.com/MustakimShaikh01/skill-matcher.git
cd skill-matcher

# 2. Create environment file
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration (or use defaults for local)

# 3. Start all services
docker-compose up --build

# 4. Open in browser
#    Frontend:  http://localhost:3000
#    API Docs:  http://localhost:8000/docs
#    ReDoc:     http://localhost:8000/redoc
```

**Stop all services:**
```bash
docker-compose down
# To also remove volumes (database data):
docker-compose down -v
```

---

### Option 2: Manual Local Setup

#### Backend (FastAPI)

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm

# Configure environment
cp .env.example .env
# Edit .env as needed (databases are optional — in-memory fallback is used)

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend available at: `http://localhost:8000`  
✅ Swagger UI: `http://localhost:8000/docs`

---

#### Frontend (React + Vite)

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend available at: `http://localhost:5173`

> **Note:** The frontend proxies API calls to `http://localhost:8000`. Ensure the backend is running first.

---

## 🔧 Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

```env
# ── MongoDB ─────────────────────────────────────────────────────────────
# Local (Docker):
MONGODB_URL=mongodb://mongo:27017/skillmatch

# Atlas (Production):
MONGODB_URL=mongodb+srv://<username>:<password>@cluster0.mongodb.net/skillmatch?retryWrites=true&w=majority

# ── PostgreSQL ───────────────────────────────────────────────────────────
# Local (Docker):
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/skillmatch

# Supabase (Production):
DATABASE_URL=postgresql://postgres:<password>@db.<project>.supabase.co:5432/postgres

# ── App Config ───────────────────────────────────────────────────────────
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV=development                   # development | production
MAX_FILE_SIZE_MB=2                # Max resume file size
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

> **💡 No databases?** The app runs perfectly with its built-in **in-memory store** — no `.env` configuration required for quick demos.

---

## � API Reference

Interactive docs available at **`http://localhost:8000/docs`** (Swagger UI) and **`http://localhost:8000/redoc`** (ReDoc).

### 📄 Resume Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/resume/upload` | Upload a resume (PDF/DOCX/TXT, max 2 MB) |
| `GET` | `/api/v1/resume/{resume_id}` | Retrieve a parsed resume by ID |
| `GET` | `/api/v1/resume/` | List all stored resumes |

**Upload Example:**
```bash
curl -X POST http://localhost:8000/api/v1/resume/upload \
  -F "file=@my_resume.pdf"
```

**Response:**
```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "skills": ["Python", "React", "FastAPI", "Docker"],
  "experience": ["Software Engineer at Acme Corp (2021–2024)"],
  "education": ["B.Tech Computer Science, IIT Bombay"],
  "projects": ["Built a microservices-based e-commerce platform"],
  "message": "Resume parsed successfully"
}
```

---

### 💼 Jobs Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/jobs/` | List all available job postings |
| `POST` | `/api/v1/jobs/` | Add a new job posting |
| `GET` | `/api/v1/jobs/{job_id}` | Get a specific job by ID |

**Pre-seeded Jobs:** The app ships with 6 demo jobs:
- Full Stack Developer
- Machine Learning Engineer
- Backend Engineer (Python)
- Frontend React Developer
- DevOps Engineer
- Data Scientist

---

### 🎯 Match Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/match/` | Match a resume against all jobs |
| `POST` | `/api/v1/match/{job_id}` | Match a resume against a specific job |

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/match/ \
  -H "Content-Type: application/json" \
  -d '{"resume_id": "550e8400-e29b-41d4-a716-446655440000"}'
```

**Response:**
```json
{
  "matches": [
    {
      "job_id": "job-001",
      "title": "Full Stack Developer",
      "match_score": 0.87,
      "matched_skills": ["Python", "React", "Docker"],
      "missing_skills": ["Node.js", "TypeScript"],
      "match_percentage": 87
    }
  ]
}
```

---

### 🌲 Skills Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/skills/` | List all 100+ known skills |
| `GET` | `/api/v1/skills/search/{prefix}` | Prefix search via Trie (O(k)) |
| `GET` | `/api/v1/skills/dependencies/{skill}` | Get skill prerequisites & dependants |
| `GET` | `/api/v1/skills/graph` | Return full dependency graph (nodes + edges) |

**Prefix Search Example:**
```bash
curl http://localhost:8000/api/v1/skills/search/py
# Returns: ["Python", "PyTorch", "Pygame", ...]
```

**Skill Dependency Example:**
```bash
curl http://localhost:8000/api/v1/skills/dependencies/machine%20learning
```
```json
{
  "skill": "machine learning",
  "level": 2,
  "prerequisites": ["Python", "NumPy", "Pandas"],
  "enables": ["Deep Learning", "NLP", "Computer Vision"]
}
```

---

### 🗺️ Roadmap Endpoint

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/match/roadmap` | Generate a learning roadmap for skill gaps |

**Response:**
```json
{
  "roadmap": [
    { "step": 1, "skill": "Python", "level": "Beginner", "reason": "Foundation skill" },
    { "step": 2, "skill": "NumPy", "level": "Beginner", "reason": "Required for ML" },
    { "step": 3, "skill": "Machine Learning", "level": "Intermediate", "reason": "Target skill" }
  ],
  "total_steps": 3
}
```

---

## 🖥️ Frontend Pages

| Page | Route | Description |
|---|---|---|
| **Landing** | `/` | Hero section, feature highlights, and CTA |
| **Upload** | `/upload` | Drag-and-drop or click-to-upload resume (PDF/DOCX/TXT) |
| **Jobs** | `/jobs` | Browse 6 pre-seeded job listings and select a target |
| **Results** | `/results` | View AI match scores, skill overlap charts, and gaps |
| **Roadmap** | `/roadmap` | Visualised, step-by-step learning path for missing skills |

---

## � DSA Components

### 🌲 Skill Trie (`skill_trie.py`)
A **prefix tree (Trie)** storing 100+ curated technology skills.

- **Insert:** O(k) where k = length of skill name
- **Search:** O(k) exact lookup
- **Prefix match:** O(k + P) where P = number of prefix matches
- **Use case:** Instant skill autocomplete + normalization of extracted skills

```
       root
      /    \
     p      r
    / \      \
   y   a      e
   |   |      |
   t   n      a
   |   |      |
   h   d      c
   |   |      |
   o   a      t
   |
   n  →  "Python"
```

---

### 🕸️ Skill Graph (`skill_graph.py`)
A **Directed Acyclic Graph (DAG)** encoding skill dependencies.

- **Nodes:** Individual technology skills
- **Edges:** `A → B` means "learning A enables B" (A is a prerequisite of B)
- **Topological Sort (DFS-based):** Ensures roadmap is dependency-ordered
- **Cycle Detection:** Prevents infinite loops in dependency resolution

**Example Graph Excerpt:**
```
Python ──► NumPy ──► scikit-learn ──► Machine Learning ──► Deep Learning
                                                          ├──► NLP
                                                          └──► Computer Vision
HTML ──► CSS ──► JavaScript ──► React ──► Next.js
```

---

### 🔢 TF-IDF Matcher (`matcher.py`)
**Term Frequency–Inverse Document Frequency** with cosine similarity.

- Vectorises both the resume text and job descriptions
- Computes pairwise cosine similarity scores (0.0 → 1.0)
- Returns ranked job matches sorted by score descending

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| **FastAPI** | 0.104.1 | Async REST API framework |
| **spaCy** | 3.7.2 | NLP — entity extraction & text processing |
| **scikit-learn** | 1.3.2 | TF-IDF vectorization & cosine similarity |
| **pdfplumber** | 0.10.3 | PDF text extraction |
| **docx2txt** | 0.8 | DOCX text extraction |
| **Motor** | 3.3.2 | Async MongoDB driver |
| **asyncpg** | 0.29.0 | Async PostgreSQL driver |
| **SQLAlchemy** | 2.0.23 | ORM & async query layer |
| **Pydantic** | 2.5.2 | Data validation & settings |
| **python-jose** | 3.3.0 | JWT token handling |
| **uvicorn** | 0.24.0 | ASGI server |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| **React** | 18.2 | UI framework |
| **Vite** | 4.5 | Build tooling & dev server |
| **React Router** | 6.22 | Client-side routing |
| **Framer Motion** | 11.0 | Animations & transitions |
| **Chart.js** | 4.4 | Match score & skill charts |
| **Lucide React** | 0.338 | Icon library |
| **Axios** | 1.6 | HTTP client |
| **React Dropzone** | 14.2 | File upload UX |
| **React Hot Toast** | 2.4 | Toast notifications |

### Infrastructure
| Technology | Purpose |
|---|---|
| **Docker & Compose** | Containerisation & orchestration |
| **MongoDB 7** | Document store (resumes, match results) |
| **PostgreSQL 16** | Relational store (jobs, users) |
| **Nginx** | Frontend production server & reverse proxy |

---

## 🧪 Running Tests

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## � Deployment

### Docker Compose (Production)

```bash
# Build production images
docker-compose build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Scale backend (optional)
docker-compose up -d --scale backend=3
```

### Manual Production Build

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the dist/ folder with nginx or any static file server
```

### Cloud Deployment Options

| Platform | Service | Notes |
|---|---|---|
| **Render** | Web Service | Connect repo, set env vars, auto-deploy |
| **Railway** | Full stack | Docker Compose support out-of-the-box |
| **Vercel** | Frontend only | Deploy `frontend/dist` |
| **AWS ECS** | Full stack | Uses Docker images from ECR |
| **MongoDB Atlas** | Database | Free tier available |
| **Supabase** | PostgreSQL | Free tier + dashboard |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'feat: add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Code Style
- **Backend:** Follow PEP 8. Use `black` for formatting.
- **Frontend:** Follow ESLint rules. Use Prettier for formatting.

---

## � License

This project is licensed under the **MIT License**.

```
MIT License — Copyright (c) 2026 Mustakim Shaikh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

<div align="center">

**Built with ❤️ by [Mustakim Shaikh](https://github.com/MustakimShaikh01)**

⭐ Star this repo if you found it useful!

</div>
