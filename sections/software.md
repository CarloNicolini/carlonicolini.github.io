---
layout: page
title: Software
permalink: /sections/software
---


<div class="body">
	{% for code in site.data.software %}
		<h1>{{ code.name }}</h1>
		<p>{{ code.description }}</p>
		<p></p>
		<div class="row" style="text-align: justify;">
			<div class="col-xs-3">
				<p><img width="100%" src="{{code.image}}"></p>
			</div>
			<div class="col-xs-2" style="text-align: left">
				{% if code.github %}
				<p>
					<a href="{{code.github}}" alt="Website">Source: <span class="fa fa-github"></span>  </a>
				</p>
				{% endif %}
				{% if code.gitlab %}
				<p>
					<a href="{{code.gitlab}}" alt="Website">Source: <span class="fa fa-gitlab"></span>  </a>
				</p>
				{% endif %}
				{% if code.downloadform %}
				<p>
					<a href="{{code.downloadform}}" alt="Download"><span class="fa fa-download"></span></a>
				</p>
				{% endif %}
				{% if code.releases %}
				<p>
					<a href="{{code.releases}}" alt="Download">Releases: <span class="fa fa-download"></span></a>
				</p>
				{% endif %}
			</div>
			<div class="col-xs-7" style="text-align: justify-all;">
				{{code.fulldescription | markdownify }}
			</div>
		</div>
	<hr/>
	<p>
	</p>
	{% endfor %}
</div>

# GraphInsight
GraphInsight is a software that let you visualize complex networks interactively.

<img src="/static/img/software/logoGI.png" alt="GraphInsight" style="width: 150px;"/>

[GraphInsight](https://github.com/carlonicolini/graphinsight) is released in its final version in many flavours: OSX, Linux and Windows 7. Here is a complete list of the versions you can download depending on your operating system.

**Linux** Tested on Ubuntu 10.04 or newer, Debian.
- 15.3 MB [GraphInsight-Pro-1.3.3-Linux-i686.deb](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.deb)
- 3.41 MB [GraphInsight-Pro-1.3.3-Linux-i686.rpm](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.rpm)
- 15.4 MB [GraphInsight-Pro-1.3.3-Linux-i686.sh](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.sh)
- 15.3 MB [GraphInsight-Pro-1.3.3-Linux-i686.tar.gz](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-i686.tar.gz)
- 19.9 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.deb](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.deb)
- 3.51 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.rpm](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.rpm)
- 19.9 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.sh](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.sh)
- 19.9 MB [GraphInsight-Pro-1.3.3-Linux-x86_64.tar.gz](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Linux-x86_64.tar.gz)

**OSX** Tested on OSX 10.8 or newer
- 28.8 MB [GraphInsight-Pro-1.3.3-MacOSX-i386.dmg](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-MacOSX-i386.dmg)

**Windows** Tested on Windows 7 or newer
- 6.36 MB [GraphInsight-Pro-1.3.3-Windows-x86.exe](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Windows-x86.exe)
- 8.17 MB [GraphInsight-Pro-1.3.3-Windows-x86.zip](https://github.com/CarloNicolini/GraphInsight/releases/download/1.3.3/GraphInsight-Pro-1.3.3-Windows-x86.zip)
- [Source code (zip)](https://github.com/CarloNicolini/GraphInsight/archive/1.3.3.zip)
- [Source code (tar.gz)](https://github.com/CarloNicolini/GraphInsight/archive/1.3.3.tar.gz)

For the Python API of GraphInsight, please look here <a class="page-link" href="/sections/GIAPI">GraphInsight Python API</a>
