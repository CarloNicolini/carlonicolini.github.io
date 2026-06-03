---
layout: post
title:  "Download audio from youtube with youtube-dl"
description: 'Download audio from youtube from command line in batch'
date:   2020-11-17
categories: tech
tags: download youtube youtubedl
published: false
---

## How to download audio from youtube

With linux or mac shell create an alias:

```bash
alias getmp3='function _youtube_to_mp3(){ youtube-dl --ignore-errors --format bestaudio --extract-audio --audio-format mp3 --audio-quality 160K --output "%(title)s.%(ext)s" --yes-playlist $1; };_youtube_to_mp3'
```

then

```bash
getmp3 <your_youtube_page>
```

Simple!