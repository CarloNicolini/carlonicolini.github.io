"""Dashboard configuration.

The site root can be set with the JEKYLL_SITE environment variable, e.g.

    JEKYLL_SITE=~/some/other/site make run

If unset, DEFAULT_SITE_ROOT is used. All `_posts` folders found anywhere under
the root are scanned.
"""

import os

DEFAULT_SITE_ROOT = "../"


def site_root() -> str:
    if not os.environ.get("JEKYLL_SITE"):
        raise ValueError("Must specify the environment variable JEKYLL_SITE pointing to where markdown files live")
    return os.environ["JEKYLL_SITE"]


# Front matter schema: which keys must be present for a post to be "valid".
REQUIRED_FIELDS = ["layout", "title", "date", "published", "categories", "description"]
OPTIONAL_FIELDS = ["tags"]
