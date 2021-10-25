---
title: Docker on MacOS
date: 2021-09-28
published: true
layout: post
---

# How to install Docker on MacOs

Docker

    $ brew install docker docker-machine
    $ brew cask install virtualbox
    -> need password
    -> possibly need to address System Preference setting
    $ docker-machine create --driver virtualbox default
    $ docker-machine env default
    $ eval "$(docker-machine env default)"
    $ docker run hello-world
    $ docker-machine stop default


To instal Graph-tool with docker:

    https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions

