# Component Library

## Overview
This document catalogs all shared UI components in the app.
All components are built with shadcn/ui (Radix UI primitives) and Tailwind CSS.

---

## Base Components (shadcn/ui)

### Button
**Location**: `components/ui/button.tsx`

**Variants**:
- `default`: Primary button
- `secondary`: Secondary button
- `outline`: Outlined button
- `ghost`: Transparent button
- `link`: Link-styled button
- `destructive`: Danger/delete button

**Sizes**: `sm`, `default`, `lg`, `icon`

**Usage**:
```tsx
<Button variant="default" size="lg">
  Click me
</Button>

<Button variant="outline" size="sm" disabled>
  Disabled
</Button>
```

**Do's**:
- Use `default` for primary actions
- Use `outline` for secondary actions
- Use `destructive` for delete/dangerous actions
- Include loading state for async actions

**Don'ts**:
- Don't use multiple primary buttons in same section
- Don't use `destructive` without confirmation
- Don't hide important actions in `ghost` buttons

---

### Card
**Location**: `components/ui/card.tsx`

**Parts**:
- `Card`: Container
- `CardHeader`: Top section
- `CardTitle`: Title
- `CardDescription`: Subtitle
- `CardContent`: Main content
- `CardFooter`: Bottom section (actions)

**Usage**:
```tsx
<Card>
  <CardHeader>
    <CardTitle>Project Title</CardTitle>
    <CardDescription>A brief description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Main content here</p>
  </CardContent>
  <CardFooter>
    <Button>View Details</Button>
  </CardFooter>
</Card>
```

**Do's**:
- Use consistent padding
- Include hover effects for clickable cards
- Use CardFooter for actions

**Don'ts**:
- Don't nest cards deeply
- Don't make cards too tall (max 400px)

---

### Input
**Location**: `components/ui/input.tsx`

**Usage**:
```tsx
<Input
  type="text"
  placeholder="Enter title"
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>
```

**Do's**:
- Always include labels (use Label component)
- Show error states
- Include placeholder text
- Use appropriate input types

**Don'ts**:
- Don't use placeholder as label
- Don't forget error messages

---

### Drawer
**Location**: `components/ui/drawer.tsx`

**Usage**:
```tsx
<Drawer open={open} onOpenChange={setOpen}>
  <DrawerContent>
    <DrawerHeader>
      <DrawerTitle>Title</DrawerTitle>
      <DrawerDescription>Description</DrawerDescription>
    </DrawerHeader>
    <div className="p-4">
      Content here
    </div>
    <DrawerFooter>
      <Button onClick={() => setOpen(false)}>Close</Button>
    </DrawerFooter>
  </DrawerContent>
</Drawer>
```

**Do's**:
- Use for detail views (idea details, request details)
- Include close button
- Make dismissible by clicking outside
- Support keyboard navigation (Escape to close)

**Don'ts**:
- Don't nest drawers
- Don't make drawer too wide (max 600px)

---

## Feature Components

### ProjectCard
**Location**: `components/projects/project-card.tsx`

**Props**:
```typescript
interface ProjectCardProps {
  project: Project;
  variant?: 'default' | 'compact';
  showActions?: boolean;
  onEdit?: () => void;
  onDelete?: () => void;
}
```

**Usage**:
```tsx
<ProjectCard
  project={project}
  variant="default"
  showActions={canEdit}
  onEdit={handleEdit}
/>
```

**Features**:
- Displays project title, summary, tags
- Shows cover image
- Hover effects
- Edit/delete actions (if permitted)
- Links to project detail page

---

### IdeaCard
**Location**: `components/ideas/idea-card.tsx`

**Props**:
```typescript
interface IdeaCardProps {
  idea: Idea;
  onVote?: () => void;
  onComment?: () => void;
}
```

**Usage**:
```tsx
<IdeaCard
  idea={idea}
  onVote={handleVote}
  onComment={handleComment}
/>
```

**Features**:
- Portrait orientation (taller than wide)
- Shows title, pitch, tags
- Vote count and button
- Comment count
- Click to open detail drawer

---

### EventCard
**Location**: `components/events/event-card.tsx`

**Props**:
```typescript
interface EventCardProps {
  event: Event;
  onRSVP?: () => void;
}
```

**Usage**:
```tsx
<EventCard
  event={event}
  onRSVP={handleRSVP}
/>
```

**Features**:
- Shows date/time prominently
- Location or "Virtual" badge
- RSVP count
- RSVP button
- Countdown for upcoming events

---

### MemberCard
**Location**: `components/members/member-card.tsx`

**Props**:
```typescript
interface MemberCardProps {
  member: Member;
  showProjects?: boolean;
}
```

**Usage**:
```tsx
<MemberCard
  member={member}
  showProjects={true}
/>
```

**Features**:
- Avatar with fallback to initials
- Name and role badge
- Top 3 skills
- Project count
- Links to profile page

---

## Shared Components

### EmptyState
**Location**: `components/shared/empty-state.tsx`

**Props**:
```typescript
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}
```

**Usage**:
```tsx
<EmptyState
  icon={<FolderIcon />}
  title="No projects yet"
  description="Create your first project to get started"
  action={{
    label: "New Project",
    onClick: () => router.push('/projects/new')
  }}
/>
```

**When to use**:
- Empty lists (no projects, no ideas)
- No search results
- No data available

---

### LoadingSkeleton
**Location**: `components/shared/loading-skeleton.tsx`

**Variants**:
- `card`: Card-shaped skeleton
- `list`: List of items
- `text`: Text lines
- `avatar`: Circular avatar

**Usage**:
```tsx
<LoadingSkeleton variant="card" count={3} />
```

**When to use**:
- While fetching data
- During page transitions
- Better than spinners for content areas

---

### ErrorState
**Location**: `components/shared/error-state.tsx`

**Props**:
```typescript
interface ErrorStateProps {
  error: Error;
  retry?: () => void;
}
```

**Usage**:
```tsx
<ErrorState
  error={error}
  retry={() => refetch()}
/>
```

**Features**:
- Shows error message
- Retry button
- Reports to Sentry

---

### Tag
**Location**: `components/shared/tag.tsx`

**Props**:
```typescript
interface TagProps {
  label: string;
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger';
  size?: 'sm' | 'md';
  onRemove?: () => void;
}
```

**Usage**:
```tsx
<Tag label="AI" variant="primary" />
<Tag label="ML" variant="default" onRemove={handleRemove} />
```

**When to use**:
- Project tags
- Idea tags
- Skills
- Status badges

---

### Avatar
**Location**: `components/shared/avatar.tsx`

**Props**:
```typescript
interface AvatarProps {
  src?: string;
  alt: string;
  fallback: string; // Initials
  size?: 'sm' | 'md' | 'lg';
}
```

**Usage**:
```tsx
<Avatar
  src={user.avatarUrl}
  alt={user.name}
  fallback="JD"
  size="md"
/>
```

**Features**:
- Shows image if available
- Falls back to initials
- Consistent sizing

---

### BentoTile
**Location**: `components/shared/bento-tile.tsx`

**Props**:
```typescript
interface BentoTileProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
  size?: 'small' | 'medium' | 'large';
  href?: string;
  onClick?: () => void;
}
```

**Usage**:
```tsx
<BentoTile
  title="Chatbot"
  description="Ask questions about the club"
  icon={<MessageSquare />}
  size="large"
  href="/playground/chat"
/>
```

**When to use**:
- Home page highlights
- Playground launcher
- Feature showcases

---

## Layout Components

### Header
**Location**: `components/layout/header.tsx`

**Features**:
- Sticky positioning
- Blur background
- Navigation links
- User menu
- Mobile responsive (hamburger menu)

---

### Footer
**Location**: `components/layout/footer.tsx`

**Features**:
- Links to pages
- Social media links
- Copyright notice

---

### Sidebar
**Location**: `components/layout/sidebar.tsx`

**Features**:
- Collapsible
- Navigation links
- Active state highlighting
- Mobile drawer

---

## Form Components

### FormField
**Location**: `components/shared/form-field.tsx`

**Props**:
```typescript
interface FormFieldProps {
  label: string;
  error?: string;
  required?: boolean;
  children: React.ReactNode;
}
```

**Usage**:
```tsx
<FormField label="Title" error={errors.title} required>
  <Input {...register('title')} />
</FormField>
```

**Features**:
- Label with required indicator
- Error message display
- Consistent spacing

---

## Component Checklist

When creating a new component:
- [ ] TypeScript props interface
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessibility (ARIA labels, keyboard navigation)
- [ ] Loading state (if applicable)
- [ ] Error state (if applicable)
- [ ] Empty state (if applicable)
- [ ] Hover effects (if interactive)
- [ ] Focus styles (keyboard navigation)
- [ ] Dark mode support (if implemented)
- [ ] Documentation in this file
- [ ] Storybook story (optional)
- [ ] Unit tests (for complex logic)
