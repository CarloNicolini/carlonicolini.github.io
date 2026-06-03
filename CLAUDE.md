---
description: 
alwaysApply: true
---

# CLAUDE.md

## Development Workflow

- Jekyll-based site with a Makefile controlling build and serving locally.
- Use `make build` for local builds.
- Use `make serve` for serving the website at localhost:4002
- CSS is in `_sass/` using `@use` module system.

## Writing articles

- Articles are in jekyll format, they require 'title',' description', 'date', 'layout: post', 'date' at least.
- You can link articles using the jekyll command {% link %}
- Articles have a centralized bibtex file to use jekyll-scholar with the {% cite authoryear %} syntax
- At the end of articles, if use add the  {% bibliography --cited %} command that autogenerates the bibliography.
- Footnotes use the [jekyll-footnotes](https://github.com/orangejulius/jekyll-footnotes) plugin. Inline reference: `{% fn %}`. At the end of the article:

  ```
  {% footnotes %}
  {% fnbody %}First note text{% endfnbody %}
  {% fnbody %}Second note text{% endfnbody %}
  {% endfootnotes %}
  ```

  Custom numbering: `{% fn 3 %}` / `{% fnbody 3 %}`. Place the `{% footnotes %}` block at the end of the article body (before `{% bibliography --cited %}` if present).
- In writing markdown math formulas must be used for both inline mode and display mode. For both use double dollars delimiting. Don't use \[ \] nor \( \) otherwise kramdown has problems with delimiters.

## Design System

The markdown articles are automatically formatted in html by the jekyll buidl system.
In case you are required to change the layout read the `DESIGN.md` before making any visual or UI decisions.
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
