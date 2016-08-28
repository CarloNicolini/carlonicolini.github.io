---
layout: default
title: Forwarding-X11-maintaining-connection-with-xpra
categories: ubuntu
date: 2016-06-16
---

How to use XPRA for remote connection to the NeuralComputation Linux servers hosted in Mattarello

XPra is a X forwarding utility that solves the problem of interrupting remote display connection.
With XPra, that comes as an open-source multiplatform utility you can "attach" your local session to a remote session that you started before even on another platform.

On X11, it is also known as screen for X11: it allows you to run programs, usually on a remote host, direct their display to your local machine, and then to disconnect from these programs and reconnect from the same or another machine, without losing any state.

# Installation
XPRA is available for clients running any flavour of Linux (Ubuntu, Debian, etc...) as well as OSX and Windows.

- Go to xpra.org and check the Download section
- Install the version you need and follow the installer instructions
- Once installed, launch XPra, select to connect with ssh

## Practical example on Linux

Johnny needs to start a Matlab session on a server that is generating many interactive windows with figures and graphics. Unfortunately Johnny is leaving for a conference and he cannot be in front of his computer in the laboratory.
Though, he need to access the same session that he fired up on his desktop workstation, from his laptop, when he's traveling on the train, to see whether the figures and the computational processes are working as expected.

This is the most typical situation that I may imagine where one wants to connect "persistently" to the same session as if he's in front of the server.

He then decide to start a remote xpra session on the server.

Johnny uses a Linux workstation in his office and access through **ssh** the remote server

	{% highlight sh %}
    johnny@laptop:~$ ssh johhny@remoteserver
    {% endhighlight %}

After logged on he fires up an xpra session on the server and he **annotates** the session identifier (typically an integer in the 10 to 1000 range). Upon this session he decide to run MATLAB.

	{% highlight sh %}
    johnny@server:~$ xpra start :100 --start-child=matlab
    {% endhighlight %}

where in this case **100** is the integer that you should annotate. Nothing happens except that he will get this log information:

	{% highlight sh %}
    Entering daemon mode; any further errors will be reported to:
    /home/johnny/.xpra/:103.log
    {% endhighlight %}

He then logs-out the `remoteserver` and on his local laptop where he installed **xpra** and he **attach**s its local computer to the remote session that is *broadcasting* MATLAB.

He opens a console and types:

	{% highlight sh %}
    johnny@laptop:~$ xpra attach ssh:johnny@remoteserver:103
    {% endhighlight %}

This will start the MATLAB sessions actually hosted on the server but visualized on the local computer.

### Sharing sessions
Johnny makes all his stuff and wants to share the screen to his colleague Gina. Johnny tells Gina how to login the server (server remote address, user and password) and then Gina starts a terminal 

	{% highlight sh %}
    gina@laptop:~$ xpra attach ssh:johnny@remoteserver:103
    {% endhighlight %}

Then Gina can see the current MATLAB session of Johnny and check the results with him. Gina can then **detach** the session:

	{% highlight sh %}
    gina@laptop:~$ xpra detach ssh:johnny@remoteserver:103
    {% endhighlight %}

and let Johnny finish his work.

### Closing sessions
After he finishes his session, Johnny closes MATLAB normally and **stops** xpra.
He connects to the server and shut down the virtual screen *:103*

	{% highlight sh %}
    $> xpra stop :103
	{% endhighlight %}
	
He receives the message that the virtual screen **:103** has exited.

Johnny is happy with **XPRA**.

## Using XPRA on other platforms
XPra is run on the server side in its Linux implementation but on client side, anyone can connect to the session.

On the XPra webpage Windows and OSX installers are available.

### Windows
1. Download and install xpra http://xpra.org
2. Run XPRa on your local Windows computer 

![LOGO][Imgur]

3. Setup the connection as SSH, leave **Quality** and **Speed** as **auto**
4. Insert the credentials `johnny` as username and `remoteserver` as the address of the remote server. 
5. Leave the port 22 and after the `:` choose the display `103`.
6. Press Connect and when asked insert the password.


[Imgur]: http://i.imgur.com/tXDp5rj.png

