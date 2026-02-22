# Testing Strategy

## Overview
We use a multi-layered testing approach:
- **Unit tests**: Test individual functions/components
- **Integration tests**: Test API endpoints and database interactions
- **E2E tests**: Test complete user flows
- **Property-based tests**: Test invariants (Phase 2)

---

## Testing Frameworks

### Backend
- **pytest**: Test runner
- **pytest-cov**: Coverage reporting
- **httpx**: API client for testing
- **faker**: Generate test data

### Frontend
- **Vitest**: Test runner (faster than Jest)
- **React Testing Library**: Component testing
- **Playwright**: E2E testing
- **MSW**: Mock API responses

---

## Coverage Targets

### Minimum Coverage
- Backend: 80% overall, 90% for critical paths (auth, payments)
- Frontend: 70% overall, 80% for business logic

### What to Test
**High priority**:
- Authentication and authorization
- Data validation
- Business logic (voting, RSVP, status changes)
- API endpoints
- Critical user flows

**Medium priority**:
- UI components
- Utility functions
- Error handling

**Low priority** (can skip):
- Simple getters/setters
- Configuration files
- Type definitions

---

## Backend Testing

### Unit Tests
```python
# tests/services/test_project_service.py
def test_create_project():
    service = ProjectService()
    project = service.create(
        db=mock_db,
        data=ProjectCreate(title="Test", summary="Test project"),
        user=mock_user
    )
    assert project.title == "Test"
    assert project.slug == "test"

def test_create_project_duplicate_slug():
    service = ProjectService()
    with pytest.raises(ValueError, match="already exists"):
        service.create(db=mock_db, data=duplicate_data, user=mock_user)
```

### Integration Tests
```python
# tests/api/test_projects.py
def test_list_projects(client):
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0

def test_create_project_unauthorized(client):
    response = client.post("/api/v1/projects", json={"title": "Test"})
    assert response.status_code == 401

def test_create_project_as_lead(client, lead_token):
    response = client.post(
        "/api/v1/projects",
        json={"title": "New Project", "summary": "Test"},
        headers={"Authorization": f"Bearer {lead_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "New Project"
```

### Test Fixtures
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)

@pytest.fixture
def mock_user(db):
    user = User(email="test@example.com", name="Test User")
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def lead_token(mock_user):
    return create_access_token({"sub": str(mock_user.id), "role": "lead"})
```

---

## Frontend Testing

### Component Tests
```typescript
// components/projects/project-card.test.tsx
import { render, screen } from '@testing-library/react';
import { ProjectCard } from './project-card';

describe('ProjectCard', () => {
  const mockProject = {
    id: 1,
    slug: 'test-project',
    title: 'Test Project',
    summary: 'A test project',
    tags: ['ai', 'ml'],
  };

  it('renders project title', () => {
    render(<ProjectCard project={mockProject} />);
    expect(screen.getByText('Test Project')).toBeInTheDocument();
  });

  it('renders tags', () => {
    render(<ProjectCard project={mockProject} />);
    expect(screen.getByText('ai')).toBeInTheDocument();
    expect(screen.getByText('ml')).toBeInTheDocument();
  });

  it('calls onEdit when edit button clicked', async () => {
    const onEdit = vi.fn();
    render(<ProjectCard project={mockProject} onEdit={onEdit} />);
    
    const editButton = screen.getByRole('button', { name: /edit/i });
    await userEvent.click(editButton);
    
    expect(onEdit).toHaveBeenCalledTimes(1);
  });
});
```

### API Mocking (MSW)
```typescript
// lib/test/mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/v1/projects', (req, res, ctx) => {
    return res(
      ctx.json({
        data: [
          { id: 1, title: 'Project 1' },
          { id: 2, title: 'Project 2' },
        ],
      })
    );
  }),

  rest.post('/api/v1/projects', (req, res, ctx) => {
    return res(
      ctx.json({
        data: { id: 3, title: req.body.title },
      })
    );
  }),
];
```

### Hook Testing
```typescript
// lib/hooks/use-projects.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useProjects } from './use-projects';

describe('useProjects', () => {
  it('fetches projects', async () => {
    const { result } = renderHook(() => useProjects());

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.data).toHaveLength(2);
    expect(result.current.data[0].title).toBe('Project 1');
  });

  it('handles errors', async () => {
    server.use(
      rest.get('/api/v1/projects', (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );

    const { result } = renderHook(() => useProjects());

    await waitFor(() => expect(result.current.isError).toBe(true));
  });
});
```

---

## E2E Testing (Playwright)

### Setup
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

### Test Examples
```typescript
// e2e/projects.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Projects', () => {
  test('can view projects list', async ({ page }) => {
    await page.goto('/projects');
    
    await expect(page.locator('h1')).toContainText('Projects');
    await expect(page.locator('[data-testid="project-card"]')).toHaveCount(5);
  });

  test('can create a new project', async ({ page }) => {
    // Login as lead
    await page.goto('/login');
    await page.fill('[name="email"]', 'lead@aiclub.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Navigate to projects
    await page.goto('/projects');
    await page.click('text=New Project');

    // Fill form
    await page.fill('[name="title"]', 'E2E Test Project');
    await page.fill('[name="summary"]', 'Created by E2E test');
    await page.click('[name="tags"]');
    await page.click('text=AI');
    await page.click('button[type="submit"]');

    // Verify redirect and content
    await expect(page).toHaveURL(/\/projects\/.+/);
    await expect(page.locator('h1')).toContainText('E2E Test Project');
  });

  test('cannot create project as member', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'member@aiclub.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await page.goto('/projects');
    
    // New Project button should not exist
    await expect(page.locator('text=New Project')).not.toBeVisible();
  });
});
```

---

## Test Data Management

### Factories (Backend)
```python
# tests/factories.py
from faker import Faker

fake = Faker()

class UserFactory:
    @staticmethod
    def create(db, **kwargs):
        user = User(
            email=kwargs.get('email', fake.email()),
            name=kwargs.get('name', fake.name()),
            hashed_password=hash_password('password123'),
        )
        db.add(user)
        db.commit()
        return user

class ProjectFactory:
    @staticmethod
    def create(db, **kwargs):
        project = Project(
            slug=kwargs.get('slug', fake.slug()),
            title=kwargs.get('title', fake.sentence()),
            summary=kwargs.get('summary', fake.paragraph()),
            tags=kwargs.get('tags', ['ai', 'ml']),
        )
        db.add(project)
        db.commit()
        return project
```

### Fixtures (Frontend)
```typescript
// lib/test/fixtures.ts
export const mockProject = {
  id: 1,
  slug: 'test-project',
  title: 'Test Project',
  summary: 'A test project',
  tags: ['ai', 'ml'],
  createdAt: '2024-01-01T00:00:00Z',
};

export const mockUser = {
  id: 1,
  email: 'test@example.com',
  name: 'Test User',
  role: 'member',
};
```

---

## Running Tests

### Backend
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/api/test_projects.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run only unit tests
pytest tests/services/

# Run only integration tests
pytest tests/api/
```

### Frontend
```bash
# Run all tests
npm test

# Run in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npm run test:e2e -- --ui
```

---

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app
      - uses: codecov/codecov-action@v3

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test -- --coverage
      - run: npm run build

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
```

---

## Testing Checklist

### Before Committing
- [ ] All tests pass locally
- [ ] New code has tests
- [ ] Coverage doesn't decrease
- [ ] No console errors/warnings

### Before Merging PR
- [ ] CI tests pass
- [ ] Code reviewed
- [ ] E2E tests pass
- [ ] Manual testing done (if UI changes)

### Before Deploying
- [ ] All tests pass on staging
- [ ] E2E tests pass on staging
- [ ] Performance tests pass (if applicable)
- [ ] Security scan passes
