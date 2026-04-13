---
layout: post
title: "Unleash Claude Code CLI with OpenRouter: Free AI Coding Power!"
description: "Claude Code with OpenRouter and free models; env and auth notes."
date: 2026-03-14
categories: tech
tags: [claude-code, openrouter, cli]
---

## Claude Code CLI with OpenRouter

The Claude Code CLI is an incredibly powerful AI assistant that lives right in your terminal, capable of navigating your codebase, running commands, and helping you build. But what if you don't have an Anthropic subscription, or want to leverage the diverse, free (and paid) models available on platforms like OpenRouter?

This guide shows you how to "trick" Claude Code into using OpenRouter as its backend, unlocking a world of alternative models, including the highly intelligent (and often free tier) NVIDIA Nemotron-3-4-12B-Instruct.

---

### Why OpenRouter + Claude Code?

* Model Freedom: Access hundreds of models beyond Anthropic's ecosystem.
* Cost Efficiency: Leverage free tiers of powerful models like Nemotron-3 (8B Instruct) or other providers.
* Performance: Experiment with different LLMs to find the best fit for your coding tasks.
* Unified API: OpenRouter provides a consistent API layer, making it easy to swap models.

---

### Step 1: Get Your OpenRouter API Key

If you don't already have one, creating an OpenRouter API key is quick and easy.

1.  Visit OpenRouter: Go to [OpenRouter website](openrouter.ai).
2.  Sign In/Up: You can sign in using your Google, GitHub, or Discord account.
3.  Navigate to API Keys: Once logged in, go to your dashboard and find the "Keys" or "API Keys" section. This is usually under your profile dropdown or a dedicated "Settings" page.
4.  Create a New Key: Click "Create New Key." Give it a descriptive name (e.g., "Claude Code CLI").
5.  Copy Your Key: Your API key will be displayed. Copy it immediately as you won't be able to see it again. It will look something like `sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.

---

### Step 2: Install Claude Code CLI

If you haven't already, install the Claude Code CLI. This requires Node.js (v18 or higher) and npm/yarn.

1.  Install Node.js: If you don't have Node.js, download it from [nodejs.org](https://nodejs.org/) or use a version manager like `nvm`.
2.  Install Claude Code via npm, or if you find it using your package manager (on MacOs it's now on `brew install --cask claude`)

```bash
npm install -g @anthropic-ai/claude-cli
# or if you prefer yarn
yarn global add @anthropic-ai/claude-cli
```

### Step 3: Configuration of API keys

This is where we tell Claude Code to route its requests through OpenRouter. 
We'll use environment variables.

Add the following lines to your shell's configuration file (e.g., `~/.zshrc`, `~/.bashrc`, `~/.config/fish/config.fish`).

```bash
# --- OpenRouter Configuration for Claude Code ---
export OPENROUTER_API_KEY="sk-or-YOUR_OPENROUTER_KEY_HERE"
export ANTHROPIC_BASE_URL="[https://openrouter.ai/api](https://openrouter.ai/api)" # Important: Use /api, NOT /api/v1
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY="" # Ensure this is empty to avoid conflicts
```

Then trick Claude into thinking to use its models instead routing them to our models. 
We'll target NVIDIA Nemotron-3-4-12B-Instruct, which often has a free tier.
```
export ANTHROPIC_DEFAULT_SONNET_MODEL="nvidia/nemotron-3-super-120b-a12b:free"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="nvidia/nemotron-3-super-120b-a12b:free"
export ANTHROPIC_DEFAULT_OPUS_MODEL="nvidia/nemotron-3-super-120b-a12b:free"
```

#### Step 4: Enjoy

You can now start Claude Code, specifiyng the model name at startup. I've created an alias for that

```bash
alias claude-nemotron-free='claude --model nvidia/nemotron-3-super-120b-a12b:free'
```

