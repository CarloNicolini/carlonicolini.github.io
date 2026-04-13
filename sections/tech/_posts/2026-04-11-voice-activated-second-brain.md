---
layout: post
title: "From brain to disk: how I built a voice-activated second brain for $0"
date: 2026-04-11
categories: tech, productivity
tags: obsidian, AI, automation, secondbrain
---

We've all been there. You're out for a walk or just about to fall asleep when a perfect idea hits. You grab your phone, record a quick voice note, and then... it just sits there. It becomes a digital fossil in your chat history that you'll probably never listen to again.

I got tired of losing those sparks. I wanted a way to just *talk* to my notes and have them actually organize themselves without me having to lift a finger—or spend a fortune. 

Here is how I built a "second brain" that listens, transcribes, and connects my thoughts for zero dollars.

## The goal: Making it effortless
The main enemy of a good idea is friction. If it takes more than two taps to save a thought, I probably won't do it. My dream setup was simple:
1. **Talk:** Send a voice note to a private Telegram bot.
2. **Clean up:** An AI turns my messy rambling into a clean, structured note.
3. **Connect:** The system looks at my old notes and tells me how the new idea fits in.

## The "zero dollar" stack
You don't need a monthly subscription to do this. You just need to bridge a few free tools together:

### Telegram as the doorway
WhatsApp is a bit of a headache to build on, but Telegram is wide open. Creating a bot takes about a minute. It's the perfect, free interface that's always in my pocket.

### Groq for the transcription
To turn audio into text, I use Whisper (an open-source model). Instead of running it on my own laptop, I send it to Groq. They have a free tier that is incredibly fast—it transcribes a one-minute ramble in about two seconds.

### Gemini for the logic
Once I have the text, I need it to look like a real note. I use Google Gemini 1.5 Flash. It's free, it's smart, and it can handle massive amounts of text. I tell it to take my transcript and turn it into a markdown note with a title and a few bullet points.

---

## How to actually set it up
If you're not a coder, you don't have to build this from scratch. There are "off-the-shelf" ways to make it happen:

* **The Obsidian way:** If you use Obsidian for your notes, there's a plugin called **Telegram Sync**. You just plug in your bot details and an API key, and your voice notes start appearing as files in your vault automatically.
* **The connection part:** To make the "agent" connect your thoughts, I use **Khoj**. It's an open-source tool that reads your note folders. When you ask it a question, it doesn't just search for words; it understands the meaning and tells you which old notes relate to your new ones.

## Why this matters
The friction is gone. I don't have to "sit down to work" anymore. I talk to my bot while I'm doing the dishes or walking the dog. By the time I'm back at my desk, my thoughts are already formatted and linked to things I wrote months ago.

It feels less like a database and more like an extension of my own memory. And since it's all built on free tiers and open-source tools, the only thing it costs is the time it took to set it up.

If you have a bunch of ideas dying in your voice memos, it might be time to build a bridge for them.