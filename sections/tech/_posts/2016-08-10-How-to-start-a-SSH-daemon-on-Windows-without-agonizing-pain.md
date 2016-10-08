---
layout: post
title: How to start a SSH daemon on Windows without agonizing pain
categories: tech
date: 2016-10-06
---

I recently needed to connect via ssh to my windows computer from a Linux server, but I couldn’t figure how to do it since ssh servers for windows are expensive and I don’t want to pay for a software that on Linux comes for free. Some of the typical ssh servers (daemon in linux terminology) are bitvise tunnelier, freesshd.

This is a list of software
[http://stackoverflow.com/questions/18292/what-are-some-good-ssh-servers-for-windows](http://stackoverflow.com/questions/18292/what-are-some-good-ssh-servers-for-windows)

My solution relies on the very good cygwin.

So first of all you have to install cygwin on your Windows 7 computer:

- [64 bit cygwin](http://cygwin.com/setup-x86_64.exe)

- [32 bit](http://cygwin.com/setup-x86.exe)

Then start the installation. As always try to select, when asked, a mirror that is close to you.
For Italian users I warmly suggest bo.garr.it (garr in Bologna).
People who are under a proxy should also set it as asked during installation of cygwin.

Then in the package list you have to search for `openssh` and install it. It is typically under *Net* packages.
Another good thing you can do is to install `scp, rsync, nano, vim, more, less`.
They are the basic editing tools one wants to use.

Then after you’ve installed cygwin, start it with administrator privileges and run the following:

    $ ssh-host-config

You will be prompted with a series of questions:

	{% highlight sh %}
    carlo@carlo-PC ~
	$ ssh-host-config

	*** Query: Overwrite existing /etc/ssh_config file? (yes/no) yes
	*** Info: Creating default /etc/ssh_config file
	*** Query: Overwrite existing /etc/sshd_config file? (yes/no) yes
	*** Info: Creating default /etc/sshd_config file
	*** Info: Privilege separation is set to yes by default since OpenSSH 3.3.
	*** Info: However, this requires a non-privileged account called 'sshd'.
	*** Info: For more info on privilege separation read /usr/share/doc/openssh/README.privep.
	*** Query: Should privilege separation be used? (yes/no) yes
	*** Info: Note that creating a new user requires that the current account have
	*** Info: Administrator privileges.  Should this script attempt to create a
	*** Query: new local account 'sshd'? (yes/no) yes
	*** Info: Updating /etc/sshd_config file
	*** Query: Do you want to install sshd as a service?
	*** Query: (Say "no" if it is already installed as a service) (yes/no) yes
	*** Query: Enter the value of CYGWIN for the daemon: [] PRESS ENTER HERE
	*** Info: On Windows Server 2003, Windows Vista, and above, the
	*** Info: SYSTEM account cannot setuid to other users -- a capability
	*** Info: sshd requires.  You need to have or to create a privileged
	*** Info: account.  This script will help you do so.
	*** Info: You appear to be running Windows XP 64bit, Windows 2003 Server,
	*** Info: or later.  On these systems, it's not possible to use the LocalSystem
	*** Info: account for services that can change the user id without an
	*** Info: explicit password (such as passwordless logins [e.g. public key
	*** Info: authentication] via sshd).
	*** Info: If you want to enable that functionality, it's required to create
	*** Info: a new account with special privileges (unless a similar account
	*** Info: already exists). This account is then used to run these special
	*** Info: servers.
	*** Info: Note that creating a new user requires that the current account
	*** Info: have Administrator privileges itself.
	*** Info: No privileged account could be found.
	*** Info: This script plans to use 'cyg_server'.
	*** Info: 'cyg_server' will only be used by registered services.
	no
	*** Query: Create new privileged user account 'cyg_server'? (yes/no) yes
	*** Info: Please enter a password for new user cyg_server.  Please be sure
	*** Info: that this password matches the password rules given on your system.
	*** Info: Entering no password will exit the configuration.
	*** Query: Please enter the password: ENTER YOUR PASSWORD HERE
	*** Query: Reenter: ENTER YOUR PASSWORD HERE

	*** Info: User 'cyg_server' has been created with password '********'.
	*** Info: If you change the password, please remember also to change the
	*** Info: password for the installed services which use (or will soon use)
	*** Info: the 'cyg_server' account.

	*** Info: Also keep in mind that the user 'cyg_server' needs read permissions
	*** Info: on all users' relevant files for the services running as 'cyg_server'.
	*** Info: In particular, for the sshd server all users' .ssh/authorized_keys
	*** Info: files must have appropriate permissions to allow public key
	*** Info: authentication. (Re-)running ssh-user-config for each user will set
	*** Info: these permissions correctly. [Similar restrictions apply, for
	*** Info: instance, for .rhosts files if the rshd server is running, etc].
	*** Info: The sshd service has been installed under the 'cyg_server'
	*** Info: account.  To start the service now, call `net start sshd' or
	*** Info: `cygrunsrv -S sshd'.  Otherwise, it will start automatically
	*** Info: after the next reboot.
	*** Info: Host configuration finished. Have fun!
	{% endhighlight %}

Then start the sshd service:
	
	{% highlight sh %}
	$ net start sshd
	The CYGWIN sshd service is starting.
	The CYGWIN sshd service was started successfully.
	{% endhighlight %}

If everything worked as you expected, you can try to login to yourself

	$ ssh localhost		

You should be able to connect to yourself without problems.
You may have problems with your Windows firewall.
You have to open the port 22 for ssh.

Open Windows Firewall by clicking the *Start* button, and then clicking *Control Panel*.
In the search box, type firewall, and then click Windows Firewall.
In the left pane, click Advanced settings. 
If you’re prompted for an administrator password or confirmation, type the password or provide confirmation.
In the Windows Firewall with Advanced Security dialog box, in the left pane, click Inbound Rules, and then, in the right pane, click *New Rule*.

Follow the instructions in the New Inbound Rule wizard

[http://windows.microsoft.com/en-us/windows/open-port-windows-firewall#1TC=windows-7](http://windows.microsoft.com/en-us/windows/open-port-windows-firewall#1TC=windows-7)

![Immagine](https://braintrekking.files.wordpress.com/2014/03/firewall_ssh_port.png)

Then this should be enough to let incoming connections on port 22 from ssh.

If you don’t know how to connect, you have to know your IP address. To get your current IP address:

*Start-> Run-> cmd*

then from the prompt run ipconfig

	C:\Users\foobar> ipconfig

and look under **IPv4** address.

So from the outside server you can now connect to your local computer, let’s suppose you windows username is foobar and your windows login password is mypassword and your ip address is `XXX.YYY.ZZZ.WWW`

	$> ssh foobar@XXX.YYY.ZZZ.WWW

then type your windows password mypassword and you are inside!
