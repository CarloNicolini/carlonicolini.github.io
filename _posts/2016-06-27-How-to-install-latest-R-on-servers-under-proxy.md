---
layout: default
title: How to install latest R on servers under proxy
categories: science
date: 2016-06-27
---

# How to install latest R on servers under proxy

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