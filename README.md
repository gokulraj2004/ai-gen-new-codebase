# New Codebase

A production-ready full-stack application scaffold built with React (TypeScript) + FastAPI (Python) + PostgreSQL 15.

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, React Router v6, TanStack React Query
- **Backend:** FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic
- **Database:** PostgreSQL 15
- **Auth:** JWT (access + refresh tokens), bcrypt password hashing
- **Infrastructure:** Docker, Docker Compose, GitHub Actions CI/CD

## Prerequisites

- Docker & Docker Compose (for containerized development)
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

## Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url> new-codebase
cd new-codebase

# 2. Copy environment variables
cp .env.example .env

# 3. Start all services
docker-compose up --build

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs (Swagger): http://localhost:8000/docs
# API Docs (ReDoc): http://localhost:8000/redoc
```

## Environment Variables

See `.env.example` for all available configuration options with descriptions.

## API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Project Structure

```
new-codebase/
├── frontend/          # React TypeScript SPA
│   ├── src/
│   │   ├── api/       # API client and endpoint functions
│   │   ├── components/ # Reusable UI and feature components
│   │   ├── context/   # React context providers
│   │   ├── hooks/     # Custom React hooks
│   │   ├── pages/     # Page-level components
│   │   ├── router/    # Route definitions
│   │   ├── types/     # TypeScript interfaces
│   │   └── utils/     # Utility functions
│   └── ...
├── backend/           # FastAPI Python application
│   ├── app/
│   │   ├── api/       # Route handlers
│   │   ├── core/      # Security, exceptions, pagination
│   │   ├── middleware/ # CORS and other middleware
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic request/response schemas
│   │   └── services/  # Business logic layer
│   ├── alembic/       # Database migrations
│   └── tests/         # Pytest test suite
└── docker-compose.yml # Multi-service orchestration
```

## Development (Without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt -r requirements-dev.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev  # Starts on http://localhost:5173
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npx vitest run
```

## Database Migrations

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Deployment

The project includes a GitHub Actions CI/CD pipeline (`.github/workflows/ci-cd.yml`) that:

1. **Lints and tests** both frontend and backend on every push/PR
2. **Builds Docker images** and pushes to GitHub Container Registry on merge to `main`

## License

MIT