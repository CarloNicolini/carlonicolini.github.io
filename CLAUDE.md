# CLAUDE.md

## Development Workflow
- Jekyll-based site. Use `bundle exec jekyll serve` for local testing.
- CSS is in `_sass/` using `@use` module system.

## Design System
Always read `DESIGN.md` before making any visual or UI decisions.
All font choices, colors, spacing, and aesthetic direction are defined there.
Do not deviate without explicit user approval.
In QA mode, flag any code that doesn't match `DESIGN.md`.

### Typography
- Display: `Instrument Serif`
- Body: `Instrument Sans`
- Code: `JetBrains Mono`

### Colors
- Primary: `#c2410c` (Deep Orange)
- Background: `#fafaf9` (Warm White)
- Dark Mode Background: `#0c0a09` (Stone Black)
