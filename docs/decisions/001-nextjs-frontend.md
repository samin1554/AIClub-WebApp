# 001. Use Next.js for Frontend

**Date**: 2024-01-15
**Status**: Accepted
**Deciders**: Tech Lead, Frontend Lead

## Context

We need to choose a frontend framework for the AI Club web app. The app needs:
- Server-side rendering for SEO (projects showcase)
- Good routing system
- Easy deployment
- TypeScript support
- Good developer experience for a student team

## Decision

We will use Next.js 14+ with the App Router.

## Consequences

### Positive
- Built-in routing with file-system based structure
- Excellent SEO with server-side rendering
- Image optimization out of the box
- Easy deployment to Vercel with preview deployments
- Large community and extensive documentation
- TypeScript support is first-class
- Server components reduce client bundle size

### Negative
- Learning curve for App Router (newer paradigm)
- Some features require understanding server vs client components
- Vendor lock-in to Vercel ecosystem (though can deploy elsewhere)
- More complex than a simple SPA

### Neutral
- Requires Node.js server (but Vercel handles this)
- Opinionated structure (but this helps team consistency)

## Alternatives Considered

### Vite + React SPA
**Pros**:
- Simpler mental model
- Faster dev server
- More flexible

**Cons**:
- No built-in SSR (bad for SEO)
- Need to set up routing manually
- More configuration needed
- Worse SEO for projects showcase

**Why rejected**: SEO is important for the projects showcase, and Next.js provides this out of the box.

### Remix
**Pros**:
- Excellent routing
- Good data loading patterns
- Modern architecture

**Cons**:
- Smaller community
- Less documentation
- Fewer examples for student team to learn from
- Less mature ecosystem

**Why rejected**: Smaller community means less support for a student team learning.

### Create React App
**Pros**:
- Simple setup
- Well-known

**Cons**:
- No longer actively maintained
- No SSR
- Slow build times
- Being phased out by React team

**Why rejected**: Deprecated by React team, not recommended for new projects.

## Implementation Notes

- Use App Router (not Pages Router)
- Enable TypeScript strict mode
- Use Server Components by default, Client Components only when needed
- Follow Next.js best practices for data fetching
- Use `next/image` for all images
- Use `next/font` for font optimization

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [App Router Migration Guide](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration)
