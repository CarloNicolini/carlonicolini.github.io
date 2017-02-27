#!/bin/bash
rm -rf _site/
jekyll serve --unpublished -w --port 4002 --config _config.local.yml
