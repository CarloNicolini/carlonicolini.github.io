"""FastAPI server for the Jekyll post dashboard."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import posts

app = FastAPI(title="Jekyll Dashboard")

STATIC_DIR = Path(__file__).parent / "static"


class PostUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date: str | None = None
    published: bool | None = None
    categories: list[str] | None = None
    tags: list[str] | None = None


@app.get("/api/posts")
def list_posts() -> dict:
    return {"posts": posts.all_posts(), "tags": posts.tag_universe()}


@app.put("/api/posts/{post_id:path}")
def update_post(post_id: str, update: PostUpdate) -> dict:
    try:
        path = posts.find_path(post_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"post non trovato: {post_id}")

    changes = {k: v for k, v in update.model_dump().items() if v is not None}
    try:
        return posts.update_post(path, changes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
