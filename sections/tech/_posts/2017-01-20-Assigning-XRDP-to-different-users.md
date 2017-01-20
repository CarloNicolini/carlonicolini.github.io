---
layout: post
title: Assigning XRDP to different users
categories: tech
date: 2017-01-20
---

Sometimes it is necessary to run multiple Xrdp sessions assigning them to different people that insist on the same user.
For example, you have a user on your remote server, called `johnny` and you want to let the `johnny@remote_host` be accessed by three different guys in your lab. You can assign different ports to different guys by explicitly modifying the `/etc/xrdp/`

It is possible to assign each

# http://serverfault.com/questions/727057/how-to-find-disconnected-xrdp-sessions
# How to find disconnected xrdp sessions
alias xrdp-list-sessions="sudo lsof  -b -w -n -c /^Xvnc$/b -a -iTCP:5900-5999"

sudo apt-get install xprintidle

#!/bin/bash

displays=`ps aux | grep Xvnc | grep -v 'grep\|sed' | sed -r 's|.*(Xvnc :[0-9]*).*|\1|' | cut -d' ' -f 2`
limit=180

date
echo "Checking for inactive sessions!"
while read -r d; do
    export DISPLAY=$d
    idle=`xprintidle`
    idleMins=$(($idle/1000/60))
    if [[ $idleMins -gt $limit ]]; then
        echo "WARN Display $d is logged in for longer than ${limit}min (${idleMins}m)"
    else
        echo "INFO Display $d is still ok (${idleMins}m)"
    fi  
done <<< "$displays"