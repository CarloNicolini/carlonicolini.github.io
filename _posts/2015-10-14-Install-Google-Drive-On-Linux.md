---
layout: default
title: Install Google Drive for Linux
categories: ubuntu
date: 2015-10-14
---

Gsync is the rsync for Google Drive. If you like me, have unlimited storage space on Google Drive, this guide that can be very useful to you. You can store your precious date on the google cloud with the warranty that they are not lost nor destroyed. Google treats data very seriously :smile: (pun intended).

1. Install the [GSync](www.https://github.com/iwonbigbro/gsync/blob/master/README.rst)

  {% highlight sh %}
  $> sudo apt-get install python-setuptools
  $> sudo easy_install pip
  $> sudo pip install gsync  {% endhighlight %}


2. If you already have **gsync** update it to the latest version, skip this step, otherwise:

  {% highlight sh %}
  sudo pip install --upgrade gsync  {% endhighlight %}

3. At this point you need to authenticate your **Google** account to use **Gsync**. To do that, try to copy some local folder that here we indicate with `~/MyTemporaryFolder/` to your main *GoogleDrive* folder, that here we indicate as `drive://` (the mountpoint of your GoogleDrive).

    {% highlight sh %}
    gsync -r -d -u -i -h --progress ~/MyTemporaryFolder drive://    {% endhighlight %}

With this command you are asking to copy the foilder `~/MyTemporaryFolder` recursively (`-r`), to transfer directories without recursing (`-r`), to skip files that are newer on the receiver (`-u`) and to print the output in human readable format (`-h`).

This is the list of currently supported options.



    -v, --verbose               enable verbose output
    -debug                 enable debug output
    -q, --quiet                 suppress non-error messages
    -c, --checksum              skip based on checksum, not mod-time & size
    -r, --recursive             recurse into directories
    -R, --relative              use relative path names
    -u, --update                skip files that are newer on the receiver
    -d, --dirs                  transfer directories without recursing
    -g, --group                 preserve group
    -o, --owner                 preserve owner (super-user only)
    -p, --perms                 preserve permissions
    -i, --itemize-changes       output a change-summary for all updates
    --progress              show progress during transfer



## FAQ:
It may happen that gsync is having some problems in moving the files and you end up not moving anything, with a log of **gsync** that looks like:


    MyTemporaryFolder/file1.png
               0   0%     0.00B/s    0:00:00
    MyTemporaryFolder/file2.mp3
               0   0%     0.00B/s    0:00:00
    MyTemporaryFolder/file3.txt
               0   0%     0.00B/s    0:00:00
    sent 0 bytes  received 0 bytes  0.00 bytes/sec


this is a problem with the source code of **gsync**. Here I post one solution that I've found [online](https://github.com/iwonbigbro/gsync/issues/66)

On Ubuntu, you have to look for the `/usr/local/lib/python2.7/dist-packages/libgsync/drive/__init__.py` file and modify line 644 where it starts like:


    {% highlight python %}
    for k, v in properties.iteritems():
        body[k] = _Drive.utf8(v)    {% endhighlight %}

and modify it to:

    {% highlight python %}
    for k, v in properties.iteritems():
        if v is not None:
            body[k] = _Drive.utf8(v)    {% endhighlight %}
