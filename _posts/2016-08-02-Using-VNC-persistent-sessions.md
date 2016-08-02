---
title: Using-VNC-persistent-sessions
layout: default
---

In this guide I briefly explain how you can get remote persistent session on the Mattarello Linux servers from any local computer, Windows, Linux or OSX.

1. Write me a mail where you ask to obtain a VNC session. You need to specify:
    Name
    Surname
    Period of usage
    Server IP address

2. I will provide you a number (an integer), let's call it **ID** together with a password (typically the password is the same of the ssh user enabled to use matlab). I've installed on every server the **XFCE4** desktop manager as it is fast and very reactive. I hope you like it.

3. Depending on your operating system follow these instructions. This method is based on TightVNC, a client to visualize VNC sessions.

## Windows:

### Download and install TightVNC

1. Go to TightVNC http://www.tightvnc.com/download.php
2. Download the *Installer for Windows 64 bit*. The current version as of August, 2, 2016 is the following: http://www.tightvnc.com/download/2.7.10/tightvnc-2.7.10-setup-64bit.msi 
3. Start the installation, press **Install** and during the installation select Custom and just install **TightVNC Viewer**
4. ![tightvnc1]
5. ![tightvnc2]
6. Leave the checkboxes `Associate to .vnc files` and `Add exception for TightVNC to Windows Firewall`  to checked:
7. ![tightvnc3]
8. ![tightvnc4]
8. Continue to *Next* and end the installation

After the installation ended, fire up **TightVNC Viewer**

1. Start **TightVNC Viewer**
2. You will get the following screen 
3. This is the TightVNC Viewer default window <br>![tightvnc5]
4. In the *Remote host* text box insert the server address followed by colon and the specific VNC port that you received. Change `serveraddress` with your server IP address and `ID` with the **ID** I've provided.
5. For example: <br>![tightvnc6]
6. Press **connect** and you should get your remote session up and running!

## EXAMPLE ##

You need to use server 10.231.128.17 and I gave you the ID=5902. You need to start TightVNC Viewer and in the remote host textbox insert:

    10.231.128.17:5902

and after that press **Connect**.
This ID will follow you everywhere and you can connect to the same remote session from multiple places also together if you want to showcast your screen to other people.

It's **extremely important that you don't logout** otherwise you will lose your session.


# Linux
Remmina is the default VNC viewer that is installed in Linux. If you don't have Remmina installed, open a terminal and install it:

`sudo apt-get install remmina`

1. Start Remmina (also called Remmina Remote Desktop Connection Client)
2. Choose "New Connection"
3. ![remmina1]
3. On the Remote Desktop Preference window, choose the name of the connection under Profile:Name 
4. Change the Profile:Protocol from the standard "RDP -Remote Desktop Protocol" to **VNC - Virtual Network Computing**
5. Under the Basic tab, in the server textbox you must insert the server name followed py ":"  and the ID of the VNC session.
6. ![remmina2]
7. For example: `10.231.128.17:5902`
8. Choose Color Depth: **True Color 24 bit**
9. Choose Quality: **Best (slowest)**
10. Save the Connection to use it in the future
11. Et voilà you have your remote VNC connection to the server.

# Mac OSX
OSX already has a VNC viewer installed that is called *Screen Sharing*.
Look into `Applications->Screen



[tightvnc1]: http://i.imgur.com/8aK0uzJl.png "TightVNC Viewer installation1"
[tightvnc2]: http://i.imgur.com/b9KrPccl.png "TightVNC Viewer installation2"
[tightvnc3]: http://i.imgur.com/sLYYtKal.png "TightVNC Viewer installation3"
[tightvnc4]: http://i.imgur.com/AdgQgSgl.png "TightVNC Viewer installation4"
[tightvnc5]: http://i.imgur.com/VnUxoCWl.png "TightVNC Viewer"
[tightvnc6]: http://i.imgur.com/dsnMn9jl.png "TightVNC Viewer example"

[remmina1]: http://i.imgur.com/toQDBgGl.png "Remmina new connection"
[remmina2]: http://i.imgur.com/YkVzSm5l.png "Remmina new connection2"
