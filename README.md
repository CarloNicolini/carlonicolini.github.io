# Carlo Nicolini — personal website

Jekyll sources for https://carlonicolini.github.io. GitHub Actions builds and publishes the site when changes land on `master`.

## Local preview

Use Ruby 3.1+ and Bundler (macOS system Ruby is too old):

```sh
make install
make serve
```

Open http://127.0.0.1:4003. LiveReload refreshes the page after edits.
`make drafts` also includes unpublished/future posts. `make build` builds published
content; `make check` checks internal links/assets. Override `PORT=4003` if needed.
`make clean` removes only generated Jekyll output.

## Content tree

- `_posts/`: all article sources, with their original filenames and explicit URLs.
- `_data/publications.yml`, `_data/software.yml`: retained editable databases.
- `_data/career.yml`: structured experience and education from `full_cv.tex`.
- `assets/media/`: everything previously in `static/`, including images, PDFs, documents and figures.
- `assets/postfigures/`: the separate original `assets/postfigures/` collection.
- `assets/{css,js,icons}/`: new UI assets; `_sass/`: the new design system.
- `_bibliography/`: original BibTeX for `{% cite key %}` and `{% bibliography --cited %}`.
- `_layouts/`, `_includes/`: new presentation templates.
- `assets/media/full_cv.tex`: the supplied CV source (no independently verified metrics).

New pages replace the old section landing-page sources, which have been removed. Migration changes asset paths, not article prose. Compatibility
URLs for old `/static/` links and section pages are generated at build time.
The dashboard and old styles are not imported. `_data` is retained in full.

## Writing

Add new articles to `_posts/` using `YYYY-MM-DD-title.md` filenames. New posts default to
`/writing/YYYY/MM/DD/title.html`; migrated articles retain their explicit permalinks.
Use YAML front matter with `layout: post`, `title`, `description`, `date`, and optionally
`published: false`. Rouge highlights fenced code blocks. Kramdown/MathJax render `$$`
math delimiters. Scholar handles citations; jekyll-footnotes supports the original
`fn`, `fnbody`, and `footnotes` tags. Standard Markdown footnotes also work.
MathJax and Google Fonts load from CDNs; text and system-font fallbacks remain usable offline.
Search and topic filters run locally in the browser. Theme follows the OS until manually set.

`_config.yml` is the shared configuration. `_config.local.yml` sets the local URL.
The Pages workflow builds with `_config.yml` only, checks internal links and assets,
and deploys the generated `_site` artifact. Unpublished and future posts are excluded.
For a local production check, run `JEKYLL_ENV=production bundle exec jekyll build --config _config.yml`
and then `python3 scripts/check_site.py`. Scholar uses the full Gemfile plugin build.

Migration also repairs malformed legacy links (missing HTTPS, reversed Markdown links, a wrong article date, and filename case). Five old software documentation PDFs were absent in the original tree: their database entries remain, but unavailable links are not shown.

The preview defaults to port 4003 so it can run alongside the original site on 4002.

All 185 post sources are retained (134 published, 51 unpublished). The draft-inclusive build also repairs a malformed external URL, suppresses a missing old post link, and comments out missing decorative image references in a translated article. Original unavailable targets are recorded inline. Published status is preserved.

A small adapter fixes the legacy footnote plugin’s markup under Kramdown; a duplicate unmatched footnote marker in one article is recorded inline and removed from rendering.

## AI Academy

`/academy/` presents the proposed individual-lesson programme. Edit `_data/academy.yml` for the two preparation lessons and the eight-lesson AI and portfolio routes. The starting-plan selector runs locally; enquiries link to LinkedIn. Timing and arrangements are proposals, not a booking system.

## Writing taxonomy

Categories are defined in `_data/taxonomy.yml`: Science contains AI, Physics, Math, Finance, and Neuroscience; Philosophy and Engineering are separate fields. Articles can cross-list substantial subjects. `categories` in source front matter is the authority; a generator removes Jekyll’s implicit historical folder categories and extracts Markdown headings for search. Every existing post has an explicit permalink to preserve its URL. The title/header review and assignments are recorded in `scripts/writing_classification.json`. Article prose and published flags are preserved; one malformed `+---` delimiter was repaired. Contacts and the downloadable CV copy use LinkedIn instead of an email address.

## Code blocks

Prism.js 1.30.0 is bundled locally in `assets/vendor/prism/`, with its standard toolbar, copy-to-clipboard, show-language, and line-numbers plugins. `assets/js/code-blocks.js` adapts Jekyll/Rouge output and adds the per-block line-number toggle. Numbers start hidden; controls remain at the upper right. Highlighting colors follow the light/dark theme. Supported archive languages include Python, Bash, Scala, Matlab, C/C++, JavaScript, XML/HTML, JSON, LaTeX, Dockerfile, and Mermaid; unsupported languages retain plain source text and the same controls. Inline code remains inline. Rouge remains the static fallback when JavaScript is unavailable.

## Publication and software images

The `image` fields in `_data/software.yml` and `_data/publications.yml` point to local files under `assets/media/img/software/` and `assets/media/img/pub/` (with shared legacy images where applicable). Original local images were preserved byte for byte; externally linked images were downloaded and their source URLs retained in `image_source`. Templates render the supplied artwork without cropping it. Entries without an image remain text-only.

Code toolbar controls use inline SVG icons with accessible names and native tooltips. Copy status is shown by a checkmark or error icon; Prism still owns the clipboard behavior.
