# SkillMatch AI

**SkillMatch AI** is an intelligent platform that bridges the gap between job seekers and employers by leveraging advanced Natural Language Processing (NLP) and Data Structures & Algorithms (DSA). It uses AI to match resumes with job descriptions, identify skill gaps, and generate personalized learning roadmaps.

## 🚀 Features

- **AI-Powered Matching**: Uses spaCy and TF-IDF to calculate semantic similarity between resumes and jobs.
- **Skill Gap Analysis**: Identifies missing skills and ranks them by importance.
- **Learning Roadmaps**: Generates dependency-ordered learning paths using Trie and Graph algorithms.
- **Modern UI**: A fast and responsive frontend built with React and Vite.
- **Scalable Backend**: A robust API built with FastAPI and PostgreSQL.

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **AI/NLP**: [spaCy](https://spacy.io/), [scikit-learn](https://scikit-learn.org/)
- **Data Structures**: Trie, Graph (for learning paths)

### Frontend
- **Framework**: [React](https://react.dev/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **State Management**: React Hooks

## 📂 Project Structure

```
skillmatcher/
├── backend/          # FastAPI Application
│   ├── app/
│   │   ├── api/        # API Routes
│   │   ├── core/       # Configuration & Database
│   │   ├── models/     # Pydantic Models
│   │   └── services/   # Business Logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # React Application
│   ├── src/
│   │   ├── components/ # UI Components
│   │   ├── services/   # API Clients
│   │   ├── pages/      # Page Components
│   │   └── App.tsx     # Main App
│   ├── Dockerfile
│   └── vite.config.ts
├── docker-compose.yml  # Orchestration
└── README.md
```

## ⚙️ Setup & Installation

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd skillmatcher
```

### 2. Start the Application
Use Docker Compose to build and run the entire stack:

```bash
docker-compose up --build
```

### 3. Access the Application
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testing

### Backend Tests
Run the test suite for the backend:
```bash
docker-compose exec backend pytest
```

### Frontend Tests
Run the frontend tests:
```bash
docker-compose exec frontend npm test
```

## 📂 API Endpoints

### Resumes
- `POST /api/v1/resumes/`: Upload and parse a resume.
- `GET /api/v1/resumes/`: List all resumes.
- `GET /api/v1/resumes/{id}`: Get a specific resume.

### Jobs
- `POST /api/v1/jobs/`: Create a new job posting.
- `GET /api/v1/jobs/`: List all jobs.
- `GET /api/v1/jobs/{id}`: Get a specific job.

### Matching
- `POST /api/v1/match/`: Match resumes to jobs.
- `GET /api/v1/match/resume/{resume_id}`: Get matches for a specific resume.
- `GET /api/v1/match/job/{job_id}`: Get matches for a specific job.

### Skills
- `GET /api/v1/skills/`: List all skills.
- `GET /api/v1/skills/gap/{resume_id}`: Get skill gap analysis for a resume.
- `GET /api/v1/skills/roadmap/{resume_id}`: Get learning roadmap.

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/AmazingFeature`).
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
3. Push to the branch (`git push origin feature/AmazingFeature`).
4. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Author**: [Your Name]
- **Email**: [Your Email]

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [spaCy](https://spacy.io/)
