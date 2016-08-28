---
layout: post
title: How to install latest R on servers under proxy
categories: tech
date: 2016-06-27
---

It's possible to keep your R version updated on Ubuntu 14.04 if you decide not to use the version provided by the package maintainer. In this small guide I explain how to do that especially if you are under a proxy server.

In this case I use the proxy of unitn on port 3128. Open a terminal and export the variables `https_proxy`, `http_proxy`, `ftp_proxy` and `ftps_proxy` to the same value `http://proxy.unitn.it:3128`.

Then add the string `"deb http://cran.rstudio.com/bin/linux/ubuntu precise/"`  and `"deb http://cran.rstudio.com/bin/linux/ubuntu trusty/"` to your `/etc/apt/sources.list` file to enable `trusty` and `precise` repositories from the CRAN. We do this with the command:

	{% highlight sh linenos %}	
	sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu precise/" >> /etc/apt/sources.list'
	sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list'
	{% endhighlight %}

We then add to the keyserver the key from the CRAN repo:

	sudo -E gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9

It's important to do `sudo -E` so that the super-user environment variables are the same as the one set before (in particular the proxy variables).

# How to install latest R on servers under proxy

This is the final list of commands to issue in a terminal.

	{% highlight sh linenos %}	
	export http_proxy=http://proxy.unitn.it:3128
	export https_proxy=http://proxy.unitn.it:3128
	export ftp_proxy=http://proxy.unitn.it:3128
	export ftps_proxy=http://proxy.unitn.it:3128
	sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu precise/" >> /etc/apt/sources.list'
	sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list'
	sudo -E gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
	sudo -E gpg -a --export E084DAB9 | sudo apt-key add -
	sudo apt-get update
	sudo apt-get -y install r-base
	{% endhighlight %}

