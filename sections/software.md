---
layout: page
title: Software
permalink: /sections/software
page_class: page--wide
---
<p class="section-description">
  Here is a list of ready-to-use software that I have developed over the course of these last years, both as scientific programmer, as PhD student and now as postdoc.
</p>

<div class="software-list">
  {% for code in site.data.software %}
  {% assign code_link = code.url | default: code.documentation | default: code.github %}
  <article class="software-item">
    <div class="software-head">
      <h2 class="software-title">
        {% if code_link %}
        <a href="{{ code_link }}">{{ code.name }}</a>
        {% else %}
        {{ code.name }}
        {% endif %}
      </h2>
      <p class="software-description">{{ code.description }}</p>
    </div>
    <aside class="software-aside">
      {% if code.image %}
      <img class="software-image" src="{{ code.image }}" alt="{{ code.name }}">
      {% endif %}
      <div class="software-links">
        {% if code.github %}
        <a href="{{ code.github }}"><span class="material-symbols-outlined" aria-hidden="true">code</span><span>Source</span></a>
        {% endif %}
        {% if code.gitlab %}
        <a href="{{ code.gitlab }}"><span class="material-symbols-outlined" aria-hidden="true">code</span><span>Source</span></a>
        {% endif %}
        {% if code.bitbucket %}
        <a href="{{ code.bitbucket }}"><span class="material-symbols-outlined" aria-hidden="true">code</span><span>Source</span></a>
        {% endif %}
        {% if code.documentation %}
        <a href="{{ code.documentation }}"><span class="material-symbols-outlined" aria-hidden="true">docs</span><span>Docs</span></a>
        {% endif %}
        {% if code.downloadform %}
        <a href="{{ code.downloadform }}"><span class="material-symbols-outlined" aria-hidden="true">download</span><span>Download</span></a>
        {% endif %}
        {% if code.releases %}
        <a href="{{ code.releases }}"><span class="material-symbols-outlined" aria-hidden="true">download</span><span>Releases</span></a>
        {% endif %}
      </div>
    </aside>
    {% if code.fulldescription %}
    <div class="software-body">
      {{ code.fulldescription | markdownify }}
    </div>
    {% endif %}
  </article>
  {% endfor %}
</div>
