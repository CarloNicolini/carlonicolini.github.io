# Jekyll site Makefile
# Run 'make install' once to install Jekyll and plugins, then 'make serve' or 'make build'

CONFIG := _config.local.yml
JEKYLL := bundle exec jekyll
# Avoid collisions when another Jekyll (or tool) already uses the default LiveReload port (35729).
LIVERELOAD_PORT := 35742

.PHONY: install serve build clean lint

# Knowledge-base lint (sections/); agent-friendly diagnostics
lint:
	uv run --with pyyaml --with rich scripts/lint_kb.py

# Fix math delimiters for kramdown ($, \(...\), \[...\]); writes post.md.backup
lint-fix-math:
	uv run --with pyyaml --with rich scripts/lint_kb.py --fix-math

install:
	bundle install

serve:
	$(JEKYLL) serve --unpublished -w --host 0.0.0.0 --port 4002 --livereload --livereload-port $(LIVERELOAD_PORT) --config $(CONFIG)

build:
	$(JEKYLL) build --unpublished --config $(CONFIG) --incremental

clean:
	rm -rf _site
