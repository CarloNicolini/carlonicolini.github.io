---
layout: post
categories: tech
title: How to expand the loopback device size
---

[From this answer](https://askubuntu.com/questions/260620/resize-dev-loop0-and-increase-space)


You can use sudo losetup /dev/loop0 to see what file the loopback device is attached to, then you can increase its size with, for example, sudo dd if=/dev/zero bs=1MiB of=/path/to/file conv=notrunc oflag=append count=xxx where xxx is the number of MiB you want to add. After that,  sudo losetup -c /dev/loop0 and sudo resize2fs /dev/loop0 should make the new space available for use.

In my case I had the Dropbox storage in

    .dropbox/storage

that is a file of 10GB, but needed more space.
So what I did is to add other 4 fresh GB.
I first unmounted the partion with disk utility then did:

    sudo if=/dev/zero bs=1MiB of=~/.dropbox/storage conv=notrunc oflag=append count=4096

then remounted. 
Et voilà!

