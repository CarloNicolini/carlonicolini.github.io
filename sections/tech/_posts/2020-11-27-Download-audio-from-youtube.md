---
layout: post
title:  "Download audio from youtube"
date:   2020-11-17
categories: tech
tags: download youtube youtubedl
published: false
---

# How to download audio from youtube

With linux or mac shell create an alias:


	alias getmp3='function _youtube_to_mp3(){ youtube-dl --ignore-errors --format bestaudio --extract-audio --audio-format mp3 --audio-quality 160K --output "%(title)s.%(ext)s" --yes-playlist $1; };_youtube_to_mp3'

then

	getmp3 <your_youtube_page>

Simple!

