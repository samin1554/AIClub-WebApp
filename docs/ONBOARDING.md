# Developer Onboarding Guide

Welcome to the AI Club Web App team! This guide will get you up and running.

---

## Prerequisites

### Required Software
- **Node.js** 18+ and npm/yarn
- **Python** 3.11+
- **PostgreSQL** 15+
- **Redis** (optional for MVP, required for Phase 2)
- **Git**

### Accounts Needed
- GitHub account (for code access)
- OpenAI API key (for chatbot/prompt lab)
- Spotify Developer account (Phase 2)

---

## Initial Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/ai-club-app.git
cd ai-club-app
```

### 2. Install Dependencies

#### Frontend
```bash
cd apps/web
npm install
```

#### Backend
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Setup

#### Create Database
```bash
createdb aiclub_dev
```

#### Run Migrations
```bash
cd apps/api
alembic upgrade head
```

#### Seed Test Data
```bash
python scripts/seed_data.py
```

This creates:
- Admin user: `admin@aiclub.com` / `password123`
- Lead user: `lead@aiclub.com` / `password123`
- Member user: `member@aiclub.com` / `password123`
- 5 sample projects
- 10 sample ideas
- 3 upcoming events

### 4. Environment Variables

#### Backend (.env)
```bash
cd apps/api
cp .env.example .env
```

Edit `.env`:
```bash
DATABASE_URL=postgresql://localhost:5432/aiclub_dev
SECRET_KEY=dev-secret-key-change-in-production
OPENAI_API_KEY=sk-your-key-here
REDIS_URL=redis://localhost:6379
DEBUG=True
```

#### Frontend (.env.local)
```bash
cd apps/web
cp .env.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Running the App

### Start Backend
```bash
cd apps/api
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Start Frontend
```bash
cd apps/web
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Start Redis (if needed)
```bash
redis-server
```

---

## Verify Setup

### 1. Check Backend
Visit `http://localhost:8000/docs` - you should see the API documentation.

### 2. Check Frontend
Visit `http://localhost:3000` - you should see the home page.

### 3. Test Login
1. Go to `http://localhost:3000/login`
2. Login with `member@aiclub.com` / `password123`
3. You should be redirected to the home page

### 4. Test API
```bash
curl http://localhost:8000/api/v1/projects
```

Should return a list of projects.

---

## Development Workflow

### Creating a New Feature

1. **Create a branch**
```bash
git checkout -b feat/your-feature-name
```

2. **Make changes**
- Follow the code style (see below)
- Write tests
- Update documentation

3. **Test locally**
```bash
# Backend tests
cd apps/api
pytest

# Frontend tests
cd apps/web
npm test
```

4. **Commit changes**
```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` code restructuring
- `test:` adding tests
- `chore:` maintenance

5. **Push and create PR**
```bash
git push origin feat/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Code Style

### Backend (Python)
- Follow PEP 8
- Use type hints
- Max line length: 100 characters
- Use Black for formatting: `black .`
- Use isort for imports: `isort .`

### Frontend (TypeScript)
- Use Prettier for formatting
- Use ESLint for linting
- Run before committing:
```bash
npm run lint
npm run format
```

---

## Common Tasks

### Add a New Database Table

1. Create model in `apps/api/app/models/`
2. Create migration:
```bash
alembic revision --autogenerate -m "Add your_table"
```
3. Review migration file
4. Run migration:
```bash
alembic upgrade head
```

### Add a New API Endpoint

1. Create schema in `apps/api/app/schemas/`
2. Add service logic in `apps/api/app/services/`
3. Add route in `apps/api/app/api/v1/`
4. Test endpoint in `tests/`

### Add a New Frontend Page

1. Create page in `apps/web/app/(main)/your-page/page.tsx`
2. Add navigation link in `components/layout/header.tsx`
3. Create components in `components/your-page/`
4. Add API calls in `lib/api/`

---

## Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**: Make sure PostgreSQL is running:
```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Port Already in Use
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution**: Kill the process using the port:
```bash
# Find process
lsof -i :3000

# Kill process
kill -9 <PID>
```

### Module Not Found
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**: Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Migration Conflicts
```
alembic.util.exc.CommandError: Multiple head revisions are present
```

**Solution**: Merge migration heads:
```bash
alembic merge heads -m "merge migrations"
alembic upgrade head
```

---

## Useful Commands

### Backend
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Format code
black .
isort .

# Type checking
mypy app

# Create migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend
```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Lint
npm run lint

# Format
npm run format

# Type check
npm run type-check
```

---

## Getting Help

### Documentation
- Architecture: `docs/Architecture.md`
- API Contract: `docs/api-contract.md`
- Component docs: `docs/components/`

### Team Communication
- Slack: #ai-club-dev
- Weekly standup: Mondays 10am
- Code reviews: Tag @tech-lead

### Resources
- FastAPI docs: https://fastapi.tiangolo.com
- Next.js docs: https://nextjs.org/docs
- SQLAlchemy docs: https://docs.sqlalchemy.org

---

## Next Steps

1. Read the architecture docs
2. Pick a starter task from the backlog
3. Set up your IDE (VS Code recommended)
4. Join the team Slack channel
5. Attend the next standup

Welcome to the team! 🎉
