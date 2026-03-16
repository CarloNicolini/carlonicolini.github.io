---
layout: post
title: "Running Claude Code via OpenRouter in Docker: A Guide to Smooth Sandboxing"
date: 2026-03-16
categories: ai devops
tags: [docker, claude-code, openrouter, python]
---

AI coding agents like **Claude Code** are incredibly powerful, but running them directly on your host machine can feel risky. Containerizing them is the logical step, but it often leads to auth conflicts, 401 errors, or terminal freezes.

Here is the definitive guide to running Claude Code inside a Docker sandbox using **OpenRouter** and free models like **Nvidia Nemotron**.

## The Challenges
1. **The Alpine Trap:** Small images like Alpine cause Claude Code to hang or run slowly due to `musl` vs `glibc` incompatibilities.
2. **Auth Conflicts:** Claude Code gets confused when it sees both an internal OAuth session and external environment variables.
3. **The Docker Freeze:** The CLI often hangs while waiting for a browser-based login that doesn't exist in a headless container.

## The Solution: A Better Dockerfile

We use a Debian-slim base for performance and pre-seed the configuration to bypass the onboarding flow.

```dockerfile
# Use uv for fast Python management on Debian
FROM ghcr.io/astral-sh/uv:debian-slim AS base

# Install Node.js, npm, and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# Create a non-root user for security
RUN useradd -m -u 1000 appuser
WORKDIR /app

# PRE-SEED CONFIG: This prevents the "Freeze" by skipping onboarding
RUN mkdir -p /home/appuser/.claude && \
    echo '{"hasCompletedOnboarding": true}' > /home/appuser/.claude.json && \
    chown -R appuser:appuser /home/appuser

USER appuser

# Default to shell
CMD ["/bin/bash"]

```

## Running the Sandbox

To avoid 401 errors, do **not** hardcode keys in the Dockerfile. Instead, inject them at runtime from your host's `.zshrc` or `.bashrc`.

### The Magic Command

Note that we explicitly blank out `ANTHROPIC_API_KEY` to force the tool to use our OpenRouter token.

```bash
docker run -it --rm \
  -e ANTHROPIC_BASE_URL="[https://openrouter.ai/api](https://openrouter.ai/api)" \
  -e ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY" \
  -e ANTHROPIC_API_KEY="" \
  -e ANTHROPIC_MODEL="nvidia/nemotron-3-super-120b-a12b:free" \
  -e ANTHROPIC_SMALL_FAST_MODEL="nvidia/nemotron-3-super-120b-a12b:free" \
  -v "$(pwd)":/app \
  my-claude-image \
  claude --model nvidia/nemotron-3-super-120b-a12b:free

```

## Why This Works

* **No Freezing:** By creating the `.claude.json` file during the build, the agent thinks it's already logged in, bypassing the OAuth browser requirement.
* **Pure OpenRouter:** Setting `ANTHROPIC_API_KEY=""` prevents "Auth Conflict" warnings and ensures the agent routes through the OpenRouter gateway.
* **Resource Limits:** You can safely append `--memory="2g" --cpus="1.0"` to the run command to ensure the agent doesn't over-consume host resources.

Now you have a fully sandboxed, performant coding agent that can't touch your host system unless you explicitly let it!

```