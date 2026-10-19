BUNDLE ?= bundle
JEKYLL := $(BUNDLE) exec jekyll
HOST ?= 127.0.0.1
PORT ?= 4003
LIVERELOAD_PORT ?= 35743
CONFIG := _config.yml,_config.local.yml

.PHONY: help install build serve preview clean check drafts
help:
	@echo "make install  Install Ruby dependencies"
	@echo "make serve    Live preview at http://$(HOST):$(PORT)"
	@echo "make drafts   Preview unpublished and future articles"
	@echo "make build    Build published content into _site"
	@echo "make check    Build and check internal links/assets"
install:
	$(BUNDLE) install
build:
	$(JEKYLL) build --config $(CONFIG)
serve preview:
	$(JEKYLL) serve --config $(CONFIG) --host $(HOST) --port $(PORT) --unpublished --future --livereload --livereload-port $(LIVERELOAD_PORT)
drafts:
	$(JEKYLL) serve --config $(CONFIG) --host $(HOST) --port $(PORT) --unpublished --future --drafts --livereload --livereload-port $(LIVERELOAD_PORT)
check: build
	python3 scripts/check_site.py
clean:
	$(JEKYLL) clean
