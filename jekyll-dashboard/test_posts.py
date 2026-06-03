"""Round-trip tests: body must survive untouched, front matter normalizes."""

from pathlib import Path

import posts


def write(tmp_path, name, text) -> Path:
    section = tmp_path / "tech" / "_posts"
    section.mkdir(parents=True, exist_ok=True)
    p = section / name
    p.write_text(text, encoding="utf-8")
    return p


BODY = "## Heading\n\nSome **markdown** body.\n\n---\n\nA line with three dashes inside.\n"


def test_body_preserved_and_field_updated(tmp_path):
    src = (
        "---\n"
        "layout: post\n"
        "title: Old Title\n"
        "date: 2016-09-01 11:00:00\n"
        "categories: tech\n"
        "tags: spark scala python\n"
        "published: false\n"
        "---\n"
    ) + BODY
    p = write(tmp_path, "post.md", src)

    posts.update_post(p, {"title": "New Title", "published": True})
    out = p.read_text()

    # body intact (everything after the closing ---)
    assert out.endswith(BODY)
    # field changed + date normalized to ISO
    rec = posts.read_post(p)
    assert rec["title"] == "New Title"
    assert rec["published"] is True
    assert rec["date"] == "2016-09-01"
    # tags coerced from space-separated to list
    assert rec["tags"] == ["spark", "scala", "python"]


def test_duplicate_keys_detected(tmp_path):
    src = (
        "---\n"
        "layout: post\n"
        "title: First\n"
        "title: Second\n"
        "date: 2021-05-19\n"
        "categories: finance\n"
        "published: false\n"
        "---\n"
    ) + BODY
    p = write(tmp_path, "dup.md", src)
    rec = posts.read_post(p)
    assert "title" in rec["duplicate_keys"]
    assert any("duplicate" in i for i in rec["issues"])


def test_missing_description_flagged(tmp_path):
    src = (
        "---\n"
        "layout: post\n"
        "title: No Desc\n"
        "date: 2020-01-01\n"
        "categories: tech\n"
        "published: true\n"
        "---\n"
    ) + BODY
    p = write(tmp_path, "nodesc.md", src)
    rec = posts.read_post(p)
    assert any("description" in i for i in rec["issues"])


def test_duplicate_keys_do_not_wipe_other_fields(tmp_path):
    # Regression: ruamel raised on dup keys, which previously wiped date/categories.
    src = (
        "---\n"
        "layout: post\n"
        "date: 2021-05-19\n"
        "title: First\n"
        "published: false\n"
        "title: Second\n"
        "categories: finance\n"
        "---\n"
    ) + BODY
    p = write(tmp_path, "dupkeep.md", src)
    posts.update_post(p, {"published": True})
    rec = posts.read_post(p)
    assert rec["date"] == "2021-05-19"
    assert rec["categories"] == ["finance"]
    assert rec["published"] is True
    assert p.read_text().endswith(BODY)
    # date is written unquoted as a native YAML date
    assert "date: 2021-05-19\n" in p.read_text()


def test_tags_written_as_block_list(tmp_path):
    src = "---\nlayout: post\ntitle: T\ndate: 2020-01-01\ncategories: tech\npublished: true\n---\n" + BODY
    p = write(tmp_path, "tags.md", src)
    posts.update_post(p, {"tags": ["a", "b"]})
    raw = p.read_text()
    assert "tags:\n- a\n- b\n" in raw or "tags:\n  - a\n  - b\n" in raw
