# Frontend Architecture

## Tech Stack

### Core
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI primitives)

### State Management
- **Server State**: TanStack Query (React Query)
- **Client State**: Zustand (for global UI state)
- **Form State**: React Hook Form + Zod validation

### Additional Libraries
- **Date handling**: date-fns
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Charts** (optional): Recharts
- **Markdown**: react-markdown

---

## Project Structure

```
apps/web/
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth layout group
│   │   ├── login/
│   │   └── register/
│   ├── (main)/              # Main app layout group
│   │   ├── page.tsx         # Home page
│   │   ├── projects/
│   │   ├── ideas/
│   │   ├── requests/
│   │   ├── events/
│   │   ├── members/
│   │   └── playground/
│   ├── admin/               # Admin layout group
│   ├── api/                 # API routes (if needed)
│   ├── layout.tsx           # Root layout
│   └── globals.css          # Global styles
├── components/
│   ├── ui/                  # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── drawer.tsx
│   │   └── ...
│   ├── layout/              # Layout components
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   └── sidebar.tsx
│   ├── projects/            # Feature-specific components
│   │   ├── project-card.tsx
│   │   ├── project-filters.tsx
│   │   └── ...
│   ├── ideas/
│   ├── events/
│   └── shared/              # Shared components
│       ├── empty-state.tsx
│       ├── loading-skeleton.tsx
│       └── error-boundary.tsx
├── lib/
│   ├── api/                 # API client
│   │   ├── client.ts
│   │   ├── projects.ts
│   │   ├── ideas.ts
│   │   └── ...
│   ├── hooks/               # Custom hooks
│   │   ├── use-auth.ts
│   │   ├── use-permission.ts
│   │   └── ...
│   ├── utils/               # Utility functions
│   │   ├── cn.ts            # Class name merger
│   │   ├── format.ts        # Date/number formatting
│   │   └── validation.ts    # Zod schemas
│   └── constants.ts         # App constants
├── stores/                  # Zustand stores
│   ├── auth-store.ts
│   └── ui-store.ts
├── types/                   # TypeScript types
│   ├── api.ts               # API response types
│   ├── models.ts            # Data models
│   └── index.ts
└── public/                  # Static assets
    ├── images/
    └── icons/
```

---

## Design System

### Tailwind Configuration
```typescript
// tailwind.config.ts
export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#...',
          // ... full scale
          900: '#...',
        },
        // ... other colors
      },
      borderRadius: {
        lg: '12px',
        md: '8px',
        sm: '4px',
      },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
      },
    },
  },
};
```

### Design Tokens
```typescript
// lib/constants.ts
export const DESIGN_TOKENS = {
  spacing: {
    xs: '0.5rem',   // 8px
    sm: '1rem',     // 16px
    md: '1.5rem',   // 24px
    lg: '2rem',     // 32px
    xl: '3rem',     // 48px
  },
  radius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    full: '9999px',
  },
  transition: {
    fast: '150ms',
    normal: '250ms',
    slow: '350ms',
  },
  shadow: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
  },
};
```

---

## Component Patterns

### Base UI Components (shadcn/ui)
Install and customize:
```bash
npx shadcn-ui@latest add button card input drawer modal
```

### Feature Components
```typescript
// components/projects/project-card.tsx
interface ProjectCardProps {
  project: Project;
  variant?: 'default' | 'compact';
  onEdit?: () => void;
}

export function ProjectCard({ project, variant = 'default', onEdit }: ProjectCardProps) {
  const canEdit = usePermission('edit', 'project');
  
  return (
    <Card className={cn('hover:shadow-lg transition-shadow', {
      'p-4': variant === 'compact',
      'p-6': variant === 'default',
    })}>
      <CardHeader>
        <CardTitle>{project.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{project.summary}</p>
      </CardContent>
      {canEdit && (
        <CardFooter>
          <Button onClick={onEdit}>Edit</Button>
        </CardFooter>
      )}
    </Card>
  );
}
```

### Shared Components
```typescript
// components/shared/empty-state.tsx
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      {icon && <div className="mb-4 text-muted-foreground">{icon}</div>}
      <h3 className="text-lg font-semibold">{title}</h3>
      {description && <p className="mt-2 text-sm text-muted-foreground">{description}</p>}
      {action && (
        <Button onClick={action.onClick} className="mt-4">
          {action.label}
        </Button>
      )}
    </div>
  );
}
```

---

## State Management

### Server State (TanStack Query)
```typescript
// lib/api/projects.ts
export const projectsApi = {
  getAll: (params?: ProjectFilters) => 
    api.get<Project[]>('/projects', { params }),
  
  getBySlug: (slug: string) => 
    api.get<Project>(`/projects/${slug}`),
  
  create: (data: ProjectCreate) => 
    api.post<Project>('/projects', data),
};

// Usage in component
function ProjectsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectsApi.getAll(),
  });

  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorState error={error} />;

  return <ProjectGrid projects={data} />;
}
```

### Client State (Zustand)
```typescript
// stores/ui-store.ts
interface UIState {
  sidebarOpen: boolean;
  chatbotOpen: boolean;
  sackbotDismissed: boolean;
  toggleSidebar: () => void;
  toggleChatbot: () => void;
  dismissSackbot: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: false,
  chatbotOpen: false,
  sackbotDismissed: false,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  toggleChatbot: () => set((state) => ({ chatbotOpen: !state.chatbotOpen })),
  dismissSackbot: () => set({ sackbotDismissed: true }),
}));
```

### Form State (React Hook Form + Zod)
```typescript
// lib/utils/validation.ts
export const projectSchema = z.object({
  title: z.string().min(3).max(100),
  description: z.string().min(10).max(500),
  tags: z.array(z.string()).min(1).max(10),
  repoUrl: z.string().url().optional(),
});

type ProjectFormData = z.infer<typeof projectSchema>;

// Usage in component
function ProjectForm() {
  const form = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
  });

  const mutation = useMutation({
    mutationFn: projectsApi.create,
    onSuccess: () => {
      toast.success('Project created!');
      router.push('/projects');
    },
  });

  return (
    <form onSubmit={form.handleSubmit((data) => mutation.mutate(data))}>
      <Input {...form.register('title')} />
      {form.formState.errors.title && <ErrorMessage />}
      <Button type="submit" disabled={mutation.isPending}>
        Create Project
      </Button>
    </form>
  );
}
```

---

## API Client

### Base Client
```typescript
// lib/api/client.ts
class ApiClient {
  private baseUrl = process.env.NEXT_PUBLIC_API_URL || '/api/v1';

  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(error);
    }

    const json = await response.json();
    return json.data; // Extract data from response wrapper
  }

  get<T>(endpoint: string, options?: { params?: Record<string, any> }) {
    const url = options?.params 
      ? `${endpoint}?${new URLSearchParams(options.params)}`
      : endpoint;
    return this.request<T>(url);
  }

  post<T>(endpoint: string, data: any) {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  patch<T>(endpoint: string, data: any) {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  delete<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const api = new ApiClient();
```

---

## Routing & Navigation

### App Router Structure
```
app/
├── (auth)/
│   ├── layout.tsx           # Auth layout (centered, no nav)
│   ├── login/page.tsx
│   └── register/page.tsx
├── (main)/
│   ├── layout.tsx           # Main layout (header, footer)
│   ├── page.tsx             # Home
│   ├── projects/
│   │   ├── page.tsx         # Projects list
│   │   └── [slug]/page.tsx  # Project detail
│   └── ...
└── admin/
    ├── layout.tsx           # Admin layout (sidebar)
    └── page.tsx
```

### Navigation Component
```typescript
// components/layout/header.tsx
export function Header() {
  const { user } = useAuth();
  const pathname = usePathname();

  const navItems = [
    { label: 'Projects', href: '/projects' },
    { label: 'Ideas', href: '/ideas' },
    { label: 'Requests', href: '/requests' },
    { label: 'Events', href: '/events' },
    { label: 'Playground', href: '/playground' },
    { label: 'Members', href: '/members' },
  ];

  return (
    <header className="sticky top-0 z-50 backdrop-blur-sm bg-background/80">
      <nav className="container flex items-center justify-between py-4">
        <Link href="/" className="text-xl font-bold">
          AI Club
        </Link>
        <ul className="flex gap-6">
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={cn('hover:text-primary transition-colors', {
                  'text-primary font-semibold': pathname.startsWith(item.href),
                })}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
        <div className="flex items-center gap-4">
          {user ? (
            <UserMenu user={user} />
          ) : (
            <Button asChild>
              <Link href="/login">Login</Link>
            </Button>
          )}
        </div>
      </nav>
    </header>
  );
}
```

---

## Performance Optimization

### Code Splitting
```typescript
// Lazy load heavy components
const Whiteboard = dynamic(() => import('@/components/playground/whiteboard'), {
  loading: () => <LoadingSkeleton />,
  ssr: false, // Disable SSR for canvas-based components
});
```

### Image Optimization
```typescript
import Image from 'next/image';

<Image
  src={project.coverUrl}
  alt={project.title}
  width={400}
  height={300}
  className="rounded-lg"
  placeholder="blur"
  blurDataURL={project.blurHash}
/>
```

### Prefetching
```typescript
// Prefetch on hover
<Link href={`/projects/${project.slug}`} prefetch={true}>
  {project.title}
</Link>
```

---

## Accessibility

### Keyboard Navigation
- All interactive elements focusable
- Visible focus indicators
- Logical tab order
- Escape key closes modals/drawers

### ARIA Labels
```typescript
<button
  aria-label="Vote for this idea"
  aria-pressed={hasVoted}
  onClick={handleVote}
>
  <ThumbsUp />
</button>
```

### Screen Reader Support
```typescript
<div role="status" aria-live="polite">
  {isLoading && <span className="sr-only">Loading projects...</span>}
</div>
```

---

## Testing Strategy

### Unit Tests (Vitest)
```typescript
// components/projects/project-card.test.tsx
describe('ProjectCard', () => {
  it('renders project title', () => {
    render(<ProjectCard project={mockProject} />);
    expect(screen.getByText(mockProject.title)).toBeInTheDocument();
  });

  it('shows edit button for authorized users', () => {
    render(<ProjectCard project={mockProject} />, {
      wrapper: AuthProvider,
    });
    expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument();
  });
});
```

### E2E Tests (Playwright)
```typescript
// e2e/projects.spec.ts
test('can create a new project', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'lead@aiclub.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');

  await page.goto('/projects');
  await page.click('text=New Project');
  await page.fill('[name="title"]', 'Test Project');
  await page.fill('[name="description"]', 'A test project');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL(/\/projects\/.+/);
  await expect(page.locator('h1')).toContainText('Test Project');
});
```

---

## Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_SENTRY_DSN=...
```

---

## Build & Deployment

### Build Command
```bash
npm run build
```

### Deployment (Vercel)
- Automatic deployments on push to main
- Preview deployments for PRs
- Environment variables in Vercel dashboard

---

## Testing Checklist
- All pages render without errors
- Navigation works correctly
- Forms validate properly
- Loading states show correctly
- Error states handled gracefully
- Responsive on mobile/tablet/desktop
- Keyboard navigation works
- Screen reader compatible
- Dark mode works (if implemented)
