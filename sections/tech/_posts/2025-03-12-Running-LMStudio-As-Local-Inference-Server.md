---
layout: post
title: Running LM-Studio headlessly on Ubuntu 24.04 with CUDA
categories: tech
published: true
date: 2025-09-26
---

# Running LM-Studio Headlessly on Ubuntu 24.04 with CUDA and Systemd

Tested with:

- OS: Ubuntu 24.04
- CUDA: Version 12
- LM-Studio: `LM-Studio-0.3.16-8-x64.AppImage`

## 🛠️ Prerequisites

Install all required libraries for the LM-Studio AppImage and headless operation:

```bash
sudo apt update
sudo apt install -y \
  appimage \
  fuse \
  libasound2-dev \
  libgtk3 \
  libgdk-pixbuf-2.0-0 \
  xvfb \
  xauth \
  libasound2t64 \
  libcups2-dev \
  libatk1.0-0t64
```


## 📦 Download LM-Studio AppImage

Download and make the AppImage executable:

```bash
cd ~
curl -o LM_Studio.AppImage https://releases.lmstudio.ai/linux/x86/0.3.16/8/LM_Studio-0.3.16-8-x64.AppImage
chmod +x LM_Studio.AppImage
```



## 🧾 Create systemd Unit Files

Create the following two systemd unit files under ~/.config/systemd/user/.

```
xvfb-user.service

[Unit]
Description=XVFB Virtual Display
After=network.target

[Service]
Type=simple
EnvironmentFile=%h/lmstudio.env
ExecStartPre=-/bin/rm -f /tmp/.X${DISPLAY#*:}-lock
ExecStartPre=-/bin/rm -f /tmp/.X11-unix/X${DISPLAY#*:}
ExecStart=/usr/bin/Xvfb $DISPLAY -screen 0 1920x1080x24 -ac +extension GLX +render -noreset
Restart=always
RestartSec=10

[Install]
WantedBy=default.target

lmstudio-user.service

[Unit]
Description=LM-Studio Headless Service
After=xvfb-user.service

[Service]
Type=simple
EnvironmentFile=%h/lmstudio.env
WorkingDirectory=%h
ExecStartPre=-/usr/bin/pkill -f lm-studio
ExecStart=/bin/bash -c './${LM_STUDIO} --no-sandbox'
ExecStop=-/usr/bin/pkill -f lm-studio
RestartSec=10

[Install]
WantedBy=default.target
```

## 📁 Environment File

Create `~/lmstudio.env` with the following content:

```
DISPLAY=:99
LM_STUDIO=LM_Studio.AppImage
```

Ensure `DISPLAY` is unique per user on multi-user systems.


## 🚀 Start & Enable Services

Start the virtual display and LM-Studio:

```bash
systemctl --user daemon-reexec
systemctl --user start xvfb-user
systemctl --user status xvfb-user
systemctl --user start lmstudio-user
systemctl --user status lmstudio-user
```

Enable them at boot:

```bash
systemctl --user enable xvfb-user
systemctl --user enable lmstudio-user
```

Allow auto-start on login:

```bash
sudo loginctl enable-linger $USER
```

## 🧠 Bootstrap the LMS CLI Tool

Run:

```bash
$HOME/.lmstudio/bin/lms bootstrap
```

This adds lms to your PATH upon next login.

## 🧪 Start LM-Studio Server

Start the server (without model):

```bash
$HOME/.lmstudio/bin/lms server start
```

## 🌐 Allow Remote Access (Optional)


Stop the service:

```bash
systemctl --user stop lmstudio-user
```

Edit the config:

```
nano $HOME/.lmstudio/.internal/http-server-config.json
```

Then change:

```
"address": "127.0.0.1"
```

to:

```
"address": "0.0.0.0"
```

Then restart:

```bash
systemctl --user start lmstudio-user
sleep 5
$HOME/.lmstudio/bin/lms server start
```

LM-Studio will now listen on all interfaces, default port `1234`.
You can now successfully use LM Studio for all your purposes!