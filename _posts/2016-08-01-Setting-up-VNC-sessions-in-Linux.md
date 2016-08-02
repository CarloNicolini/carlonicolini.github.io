---
title: Setting up VNC sessions in Linux
layout: default
---

# Server side

## Ubuntu 16.04

### Step 1 — Installing the Desktop Environment and VNC Server

By default, an Ubuntu 16.04 Droplet does not come with a graphical desktop environment or a VNC server installed, so we'll begin by installing those. Specifically, we will install packages for the latest Xfce desktop environment and the TightVNC package available in the official Ubuntu repository.

On your server, install the Xfce and TightVNC packages.

    {% highlight sh %}
    sudo apt install xfce4 xfce4-goodies tightvncserver
    {% endhighlight %}

To complete the VNC server's initial configuration after installation, use the vncserver command to set up a secure password.

    {% highlight sh %}
    vncserver
    {% endhighlight %}

You'll be promoted to enter and verify a password, and also a view-only password. Users who log in with the view-only password will not be able to control the VNC instance with their mouse or keyboard. This is a helpful option if you want to demonstrate something to other people using your VNC server, but isn't necessary.

Running vncserver completes the installation of VNC by creating default configuration files and connection information for our server to use. With these packages installed, you are now ready to configure your VNC server.

### Step 2 — Configuring the VNC Server

First, we need to tell our VNC server what commands to perform when it starts up. These commands are located in a configuration file called xstartup in the .vnc folder under your home directory. The startup script was created when you ran the vncserver in the previous step, but we need modify some of the commands for the Xfce desktop.

When VNC is first set up, it launches a default server instance on port 5901. This port is called a display port, and is referred to by VNC as :1. VNC can launch multiple instances on other display ports, like :2, :3, etc. When working with VNC servers, remember that :X is a display port that refers to 5900+X.

Because we are going to be changing how the VNC server is configured, we'll need to first stop the VNC server instance that is running on port 5901.

    {% highlight sh %}
    vncserver -kill :1
    {% endhighlight %}

The output should look like this, with a different PID:

    {% highlight sh %}
    Output
    Killing Xtightvnc process ID 17648
    {% endhighlight %}

Before we begin configuring the new xstartup file, let's back up the original.

    {% highlight sh %}
    mv ~/.vnc/xstartup ~/.vnc/xstartup.bak
    {% endhighlight %}

Now create a new xstartup file with nano or your favorite text editor.

    {% highlight sh %}
    nano ~/.vnc/xstartup
    {% endhighlight %}

Paste these commands into the file so that they are performed automatically whenever you start or restart the VNC server, then save and close the file.

    {% highlight sh %}
    ~/.vnc/xstartup
    #!/bin/bash
    xrdb $HOME/.Xresources
    startxfce4 &
    {% endhighlight %}

The first command in the file, `xrdb $HOME/.Xresources`, tells VNC's GUI framework to read the server user's .Xresources file. .Xresources is where a user can make changes to certain settings of the graphical desktop, like terminal colors, cursor themes, and font rendering. The second command simply tells the server to launch Xfce, which is where you will find all of the graphical software that you need to comfortably manage your server.

To ensure that the VNC server will be able to use this new startup file properly, we'll need to grant executable privileges to it.

    {% highlight sh %}
    sudo chmod +x ~/.vnc/xstartup
    {% endhighlight %}

Now, restart the VNC server.

    {% highlight sh %}
    vncserver
    {% endhighlight %}

The server should be started with an output similar to this:

    {% highlight sh %}
    Output
    New 'X' desktop is your_server_name.com:1

    Starting applications specified in `/home/iit/.vnc/xstartup`
    Log file is `/home/iit/.vnc/liniverse.com:1.log`
    {% endhighlight %}


### Step 3 — Creating a VNC Service File

Next, we'll set up the VNC server as a systemd service. This will make it possible to start, stop, and restart it as needed, like any other systemd service.

First, create a new unit file called /etc/systemd/system/vncserver@.service using your favorite text editor:

    {% highlight sh %}
    sudo nano /etc/systemd/system/vncserver@.service
    {% endhighlight %}

Copy and paste the following into it. Be sure to change the value of User and the username in the value of PIDFILE to match your username.

    {% highlight sh %}
    [Unit]
    Description=Start TightVNC server at startup
    After=syslog.target network.target

    [Service]
    Type=forking
    User=iit
    PAMName=login
    PIDFile=/home/iit/.vnc/%H:%i.pid
    ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
    ExecStart=/usr/bin/vncserver -depth 24 -geometry 1280x800 :%i
    ExecStop=/usr/bin/vncserver -kill :%i

    [Install]
    WantedBy=multi-user.target
    {% endhighlight %}

Save and close the file.

Next, make the system aware of the new unit file.

    {% highlight sh %}
    sudo systemctl daemon-reload
    {% endhighlight %}

Enable the unit file.

    {% highlight sh %}
    sudo systemctl enable vncserver@1.service
    {% endhighlight %}

Stop the current instance of the VNC server if it's still running.

    {% highlight sh %}
    vncserver -kill :1
    {% endhighlight %}

Then start it as you would start any other systemd service.

    {% highlight sh %}
    sudo systemctl start vncserver@1
    {% endhighlight %}

You can verify that it started with this command:

    {% highlight sh %}
    sudo systemctl status vncserver@1
    {% endhighlight %}

If it started correctly, the output should look like this:

    {% highlight sh %}
    Output:
    vncserver@1.service - TightVNC server on Ubuntu 16.04
       Loaded: loaded (/etc/systemd/system/vncserver@.service; enabled; vendor preset: enabled)
       Active: active (running) since Mon 2016-04-25 03:21:34 EDT; 6s ago
      Process: 2924 ExecStop=/usr/bin/vncserver -kill :%i (code=exited, status=0/SUCCESS)

    ...

     systemd[1]: Starting TightVNC server on Ubuntu 16.04...
     systemd[2938]: pam_unix(login:session): session opened for user finid by (uid=0)
     systemd[2949]: pam_unix(login:session): session opened for user finid by (uid=0)
     systemd[1]: Started TightVNC server on Ubuntu 16.04.
     {% endhighlight %}


## Ubuntu 14.04

### Step One — Install Desktop Environment and VNC Server

By default, most Linux server installations will not come with a graphical desktop environment. If this is the case, we'll need to begin by installing one that we can work with. In this example, we will install XFCE4, which is very lightweight while still being familiar to most users.

We can get the XFCE packages, along with the package for TightVNC, directly from Ubuntu's software repositories using apt:

    {% highlight sh %}
    sudo apt-get update
    sudo apt-get install xfce4 xfce4-goodies tightvncserver
    {% endhighlight %}

To complete the VNC server's initial configuration, use the vncserver command to set up a secure password:

    {% highlight sh %}
    vncserver
    {% endhighlight %}

(After you set up your access password, you will be asked if you would like to enter a view-only password. Users who log in with the view-only password will not be able to control the VNC instance with their mouse or keyboard. This is a helpful option if you want to demonstrate something to other people using your VNC server.)

vncserver completes the installation of VNC by creating default configuration files and connection information for our server to use. With these packages installed, you are ready to configure your VNC server and graphical desktop.

### Step Two — Configure VNC Server

First, we need to tell our VNC server what commands to perform when it starts up. These commands are located in a configuration file called xstartup. Our VNC server has an xstartup file preloaded already, but we need to use some different commands for our XFCE desktop.

When VNC is first set up, it launches a default server instance on port `5901`. This port is called a display port, and is referred to by VNC as :1. VNC can launch multiple instances on other display ports, like :2, :3, etc. When working with VNC servers, remember that :X is a display port that refers to 5900+X.

Since we are going to be changing how our VNC servers are configured, we'll need to first stop the VNC server instance that is running on port 5901:

    {% highlight sh %}
    vncserver -kill :1
    {% endhighlight %}

Before we begin configuring our new xstartup file, let's back up the original in case we need it later:

    {% highlight sh %}
    mv ~/.vnc/xstartup ~/.vnc/xstartup.bak
    {% endhighlight %}

Now we can open a new xstartup file with nano:

    {% highlight sh %}
    nano ~/.vnc/xstartup
    {% endhighlight %}

Insert these commands into the file so that they are performed automatically whenever you start or restart your VNC server:

    {% highlight sh %}
    #!/bin/bash
    xrdb $HOME/.Xresources
    startxfce4 &
    {% endhighlight %}

The first command in the file, `xrdb $HOME/.Xresources`, tells VNC's GUI framework to read the server user's .Xresources file. .Xresources is where a user can make changes to certain settings of the graphical desktop, like terminal colors, cursor themes, and font rendering.

The second command simply tells the server to launch XFCE, which is where you will find all of the graphical software that you need to comfortably manage your server.

To ensure that the VNC server will be able to use this new startup file properly, we'll need to grant executable privileges to it:

    {% highlight sh %}
    sudo chmod +x ~/.vnc/xstartup
    {% endhighlight %}

### Step Three — Create a VNC Service File

To easily control our new VNC server, we should set it up as an Ubuntu service. This will allow us to start, stop, and restart our VNC server as needed.

First, open a new service file in `/etc/init.d` with nano:

    {% highlight sh %}
    sudo nano /etc/init.d/vncserver
    {% endhighlight %}

The first block of data will be where we declare some common settings that VNC will be referring to a lot, like our username and the display resolution.

    {% highlight sh %}
    #!/bin/bash
    PATH="$PATH:/usr/bin/"
    export USER="user"
    DISPLAY="1"
    DEPTH="16"
    GEOMETRY="1024x768"
    OPTIONS="-depth ${DEPTH} -geometry ${GEOMETRY} :${DISPLAY} -localhost"
    . /lib/lsb/init-functions
    {% endhighlight %}

Be sure to replace user with the non-root user that you have set up, and change `1024x768` if you want to use another screen resolution for your virtual display.

Next, we can start inserting the command instructions that will allow us to manage the new service. The following block binds the command needed to start a VNC server, and feedback that it is being started, to the command keyword start.

    {% highlight sh %}
    case "$1" in
    start)
    log_action_begin_msg "Starting vncserver for user '${USER}' on localhost:${DISPLAY}"
    su ${USER} -c "/usr/bin/vncserver ${OPTIONS}"
    ;;
    {% endhighlight %}

    The next block creates the command keyword stop, which will immediately kill an existing VNC server instance.

    {% highlight sh %}
    stop)
    log_action_begin_msg "Stopping vncserver for user '${USER}' on localhost:${DISPLAY}"
    su ${USER} -c "/usr/bin/vncserver -kill :${DISPLAY}"
    ;;
    {% endhighlight %}

The final block is for the command keyword restart, which is simply the two previous commands (stop and start) combined into one command.

    {% highlight sh %}
    restart)
    $0 stop
    $0 start
    ;;
    esac
    exit 0
    {% endhighlight %}

Once all of those blocks are in your service script, you can save and close that file. Make this service script executable, so that you can use the commands that you just set up:

    sudo chmod +x /etc/init.d/vncserver

Now try using the service and command to start a new VNC server instance:

    {% highlight sh %}
    sudo service vncserver start
    {% endhighlight %}

# Ubuntu 12.04

## Step 1: Install Desktop Environment and VNC Server

    sudo apt-get install xfce4 xfce4-goodies tightvncserver

## Step 2: Setup TighVNC as a service

Let’s create the init.d script:

    {% highlight sh %}
    #!/bin/bash
    PATH="$PATH:/usr/bin/"
    export USER="ram"
    DISPLAY="1"
    DEPTH="16"
    GEOMETRY="1024x768"
    OPTIONS="-depth ${DEPTH} -geometry ${GEOMETRY} :${DISPLAY} -localhost"
    . /lib/lsb/init-functions
    case "$1" in
    start)
    log_action_begin_msg "Starting vncserver for user '${USER}' on localhost:${DISPLAY}"
    su ${USER} -c "/usr/bin/vncserver ${OPTIONS}"
    ;;
    stop)
    log_action_begin_msg "Stoping vncserver for user '${USER}' on localhost:${DISPLAY}"
    su ${USER} -c "/usr/bin/vncserver -kill :${DISPLAY}"
    ;;
    restart)
    $0 stop
    $0 start
    ;;
    esac
    exit 0
    {% endhighlight %}


Note that by specifying the - localhost option to the server we disallow access from anything but localhost. This is more secure but it does mean we will need to use an SSH tunnel to connect to it. Now let’s set the right permissions on this script and start it up:

    sudo chmod 755 /etc/init.d/vncserver
    sudo /etc/init.d/vncserver start

The first time you start the script it will ask you for a password. This is the password which VNC clients will have to supply when they connect to the server.

Once you’ve created a password kill the server. Now edit the vnc config file at `/home/<your username="">/.vnc/xstartup:</your>`

    #!/bin/sh

    xrdb $HOME/.Xresources
    xsetroot -solid grey
    export XKL_XMODMAP_DISABLE=1
    echo starting gnome
    startxfce4 &

So we’re telling VNC to create a new GUI session using the the Unity 2D desktop manager when a client connects. Now restart the server. And this time we’ll make sure it runs on bootup too:

    sudo /etc/init.d/vncserver start
    sudo update-rc.d vncserver defaults

Now, from your local machine SSH into your server with port forwarding enabled:

    ssh -L 5901:localhost:5901 username@my-remote-server.com

Now launch your VNC client and connect to localhost:5901. You should be prompted for the password you created earlier. Once you’re in you should see the Unity desktop and be able to interact with it.

All done!
