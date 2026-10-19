# Carlo Nicolini — design system

Personal academic homepage. Introduce Carlo by name and portrait; use concrete biographical prose rather than promotional slogans. Give computational neuroscience visible space alongside current AI research. Warm white and deep orange; stone black and bright orange in dark mode. Instrument Serif for display, Instrument Sans for body, JetBrains Mono for metadata and code, with system fallbacks. Spacious typography and fine rules. Base reading size is 19px on desktop and 18px on mobile; article text is 20px on desktop. Keep metadata secondary without shrinking explanatory prose. No decorative stock imagery.

Navigation: Writing, Publications, Software, Curriculum, AI Academy. Long-form content uses a narrow reading column; archives use searchable rows. Respect reduced motion, keyboard focus, semantic headings, and responsive layouts.

AI Academy presents a proposed programme of one-to-one lessons, with optional beginner preparation and AI/portfolio routes. Each lesson has a focus, an exercise, and an outcome. Avoid invented availability, prices, endorsements, or promises of financial performance.

Code blocks use locally bundled Prism toolbar plugins. Show the language on the left, with Copy and a keyboard-accessible line-number toggle on the upper right; use theme-aware syntax colors and horizontal scrolling inside the box.

## Local style exploration

Compare four homepage directions at `/styles/`: Swiss Index, Field Journal,
Observatory, and Cobalt Studio. Each renders `_includes/home.html`, shared with
the original homepage, and applies isolated rules in `assets/css/style-lab.css`.
The preview bar switches between studies and links to the original. Other site
sections retain the existing design pending a choice. No style is persisted or
applied to the default homepage. Preview pages are excluded from the sitemap.
