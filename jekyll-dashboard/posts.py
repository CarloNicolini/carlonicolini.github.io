"""Read, validate and write Jekyll post front matter.

Design rules:
- Only the front matter block (between the first two `---` lines) is parsed
  and rewritten. The markdown body is preserved byte-for-byte.
- On save we normalize the whole front matter to a canonical shape and key
  order, because the user asked for uniform posts.
- `tags` and `categories` are written as block lists; dates as YYYY-MM-DD.
"""

from __future__ import annotations

import io
import datetime as dt
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq
from ruamel.yaml.error import YAMLError

import config

# Canonical key order for normalized front matter.
CANONICAL_ORDER = [
    "layout",
    "title",
    "description",
    "date",
    "categories",
    "tags",
    "published",
]

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.width = 4096  # avoid line wrapping of long titles/descriptions
# Real posts contain duplicate keys; keep the last value instead of raising.
_yaml.allow_duplicate_keys = True


def root() -> Path:
    return Path(config.site_root()).expanduser()


def resolve_dirs() -> list[Path]:
    """All `_posts` directories found anywhere under the site root."""
    base = root()
    if not base.is_dir():
        return []
    dirs = {p for p in base.rglob("_posts") if p.is_dir()}
    return sorted(dirs)


def section_of(path: Path) -> str:
    """Section = the folder containing `_posts` (e.g. 'science').

    Falls back to the path relative to the root when `_posts` sits at the top.
    """
    grandparent = path.parent.parent  # folder containing `_posts`
    if grandparent == root():
        return root().name  # `_posts` sits directly at the site root
    return grandparent.name


def post_id(path: Path) -> str:
    """Stable id relative to the site root, e.g. 'sections/science/_posts/x.md'."""
    try:
        return str(path.relative_to(root()))
    except ValueError:
        return path.name


def iter_post_paths() -> list[Path]:
    paths: list[Path] = []
    for d in resolve_dirs():
        paths.extend(sorted(d.glob("*.md")))
    return paths


def _split_front_matter(text: str) -> tuple[str, str] | None:
    """Return (front_matter_text, body) or None if no front matter block."""
    if not text.startswith("---"):
        return None
    lines = text.splitlines(keepends=True)
    # First line is the opening '---'. Find the closing one.
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            fm = "".join(lines[1:i])
            body = "".join(lines[i + 1 :])
            return fm, body
    return None


def _to_str_date(value) -> str:
    """Coerce a YAML date/datetime/string to YYYY-MM-DD."""
    if isinstance(value, (dt.datetime, dt.date)):
        return value.strftime("%Y-%m-%d")
    s = str(value).strip()
    # Drop any time portion like '2016-09-01 11:00:00'.
    return s.split()[0] if s else s


def _to_list(value) -> list[str]:
    """Coerce categories/tags from scalar/comma-string/space-string/list."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    s = str(value).strip()
    if not s:
        return []
    sep = "," if "," in s else None  # comma if present, else whitespace
    parts = s.split(sep) if sep else s.split()
    return [p.strip() for p in parts if p.strip()]


def parse_front_matter(text: str) -> tuple[dict, list[str]]:
    """Parse front matter into a plain dict plus a list of duplicate keys found.

    Duplicate keys are detected on the raw text because the YAML loader
    silently keeps only the last value.
    """
    fm_split = _split_front_matter(text)
    if fm_split is None:
        return {}, []
    fm_text, _ = fm_split

    seen: dict[str, int] = {}
    for line in fm_text.splitlines():
        if line and line[0] not in " \t-#":
            key = line.split(":", 1)[0].strip()
            if key:
                seen[key] = seen.get(key, 0) + 1
    duplicates = [k for k, n in seen.items() if n > 1]

    try:
        data = _yaml.load(io.StringIO(fm_text)) or {}
        data = dict(data)
    except YAMLError:
        data = {}
    return data, duplicates


def read_post(path: Path) -> dict:
    """Return a normalized view of a single post for the dashboard."""
    text = path.read_text(encoding="utf-8")
    raw, duplicates = parse_front_matter(text)

    record = {
        "id": post_id(path),
        "path": str(path),
        "filename": path.name,
        "section": section_of(path),
        "title": str(raw.get("title", "")).strip() if raw.get("title") is not None else "",
        "description": str(raw.get("description", "")).strip()
        if raw.get("description") is not None
        else "",
        "date": _to_str_date(raw.get("date")) if raw.get("date") is not None else "",
        "published": bool(raw.get("published", False)),
        "categories": _to_list(raw.get("categories")),
        "tags": _to_list(raw.get("tags")),
        "layout": str(raw.get("layout", "")).strip(),
        "extra_keys": sorted(
            k for k in raw if k not in CANONICAL_ORDER and k not in ("layout",)
        ),
        "duplicate_keys": duplicates,
    }
    record["issues"] = validate(record)
    return record


def validate(record: dict) -> list[str]:
    """Return a list of human-readable schema problems."""
    issues: list[str] = []
    if not record["layout"]:
        issues.append("manca 'layout'")
    if not record["title"]:
        issues.append("manca 'title'")
    if not record["date"]:
        issues.append("manca 'date'")
    elif not _is_iso_date(record["date"]):
        issues.append(f"data non valida: {record['date']!r}")
    if not record["description"]:
        issues.append("manca 'description'")
    if not record["categories"]:
        issues.append("manca 'categories'")
    if record["duplicate_keys"]:
        issues.append("chiavi duplicate: " + ", ".join(record["duplicate_keys"]))
    return issues


def _is_iso_date(s: str) -> bool:
    try:
        dt.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def all_posts() -> list[dict]:
    return [read_post(p) for p in iter_post_paths()]


def tag_universe() -> list[str]:
    tags: set[str] = set()
    for p in iter_post_paths():
        raw, _ = parse_front_matter(p.read_text(encoding="utf-8"))
        tags.update(_to_list(raw.get("tags")))
    return sorted(tags, key=str.lower)


def _build_front_matter(fields: dict) -> str:
    """Render canonical front matter text (without the surrounding ---)."""
    out = io.StringIO()
    ordered: dict = {}
    for key in CANONICAL_ORDER:
        if key not in fields:
            continue
        ordered[key] = fields[key]
    _yaml.dump(ordered, out)
    return out.getvalue()


def update_post(path: Path, changes: dict) -> dict:
    """Apply edits, normalize the whole front matter, preserve the body.

    `changes` may contain: title, description, date, published, categories, tags.
    """
    text = path.read_text(encoding="utf-8")
    split = _split_front_matter(text)
    if split is None:
        raise ValueError(f"{path} non ha una front matter valida")
    _, body = split
    raw, _ = parse_front_matter(text)

    layout = str(raw.get("layout", "post")).strip() or "post"
    title = changes.get("title", str(raw.get("title", "")).strip())
    description = changes.get("description", str(raw.get("description", "")).strip())
    date = changes.get("date", _to_str_date(raw.get("date")) if raw.get("date") else "")
    published = changes.get("published", bool(raw.get("published", False)))
    categories = changes.get("categories", _to_list(raw.get("categories")))
    tags = changes.get("tags", _to_list(raw.get("tags")))

    fields: dict = {"layout": layout}
    fields["title"] = title
    fields["description"] = description
    if date:
        try:
            fields["date"] = dt.date.fromisoformat(date)
        except ValueError:
            fields["date"] = date
    if categories:
        fields["categories"] = _block_seq(categories)
    if tags:
        fields["tags"] = _block_seq(tags)
    fields["published"] = bool(published)

    fm_text = _build_front_matter(fields)
    new_text = f"---\n{fm_text}---\n{body}"
    path.write_text(new_text, encoding="utf-8")
    return read_post(path)


def _block_seq(items: list[str]):
    seq = CommentedSeq(items)
    seq.fa.set_block_style()
    return seq


def find_path(post_identifier: str) -> Path:
    for p in iter_post_paths():
        if post_id(p) == post_identifier:
            return p
    raise FileNotFoundError(post_identifier)
