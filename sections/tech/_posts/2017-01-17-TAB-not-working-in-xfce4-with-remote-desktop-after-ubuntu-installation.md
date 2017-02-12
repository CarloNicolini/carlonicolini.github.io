---
layout: post
title: TAB is not working with XFCE4 after installation from Ubuntu for use with remote desktop
categories: tech
date: 2017-01-17
---

You have installed Ubuntu 14.04 or latest Ubuntu LTS 16.04 on your server and you want to make it available for remote desktop connections with the help of XRDP.
You install xrdp and you connect to your server with some client, like remmina.
Suddenly XFCE4 is showing up in its simplicity.

You start pressing TAB though and nothing happens. For some reason the behaviour of TAB key is screwed up in this case. To fix you need to edit the xfce4 configuration file.

Start a text editor and edit this file:

    {% highlight xml %}    
    ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
    {% endhighlight %}

Then look for the line where it's written:

    <property name="&lt;Super&gt;Tab" type="string" value="switch_window_key"/>

and change it to 

    {% highlight xml %}
    <property name="&lt;Super&gt;Tab" type="empty"/>
    {% endhighlight %}

reboot or whatever and then tab will work properly!
I have no idea why but when using vnc this file seems to override tab's normal behaviour and makes it into a switch window key.
