---
layout: page
title: Publications
permalink: /sections/publications
content_class: page-content--wide
---
<p class="section-description">
  Here is a short list of some of my major publications. From 2020 onward I moved from neuroscience to artificial intelligence.
</p>

<div class="publication-list">
  {% for pub in site.data.publications %}
  {% assign pub_link = pub.url | default: pub.pdf %}
  <article class="publication-item">
    <div class="publication-head">
      <h2 class="publication-title">
        {% if pub_link %}
        <a href="{{ pub_link }}">{{ pub.title }}</a>
        {% else %}
        {{ pub.title }}
        {% endif %}
      </h2>
      <p class="publication-authors">{{ pub.authors }}</p>
      <p class="publication-meta">
        {{ pub.journal }}
        {% if pub.volume %}
          <strong>{{ pub.volume }}</strong>,
        {% endif %}
        {% if pub.pages %}
          {{ pub.pages }},
        {% endif %}
        {% if pub.year %}
          ({{ pub.year }})
        {% endif %}
      </p>
    </div>
    <aside class="publication-aside">
      {% if pub.image %}
      <img class="publication-image" src="{{ pub.image }}" alt="{{ pub.title }}">
      {% endif %}
      <div class="publication-links">
        {% if pub.pmid %}
        <a href="https://www.ncbi.nlm.nih.gov/pubmed/{{ pub.pmid }}"><span class="material-symbols-outlined" aria-hidden="true">clinical_notes</span><span>PubMed {{ pub.pmid }}</span></a>
        {% endif %}
        {% if pub.pdf %}
        <a href="{{ pub.pdf }}"><span class="material-symbols-outlined" aria-hidden="true">picture_as_pdf</span><span>PDF</span></a>
        {% elsif pub.preprint %}
        <a href="{{ pub.preprint }}"><span class="material-symbols-outlined" aria-hidden="true">description</span><span>Preprint</span></a>
        {% endif %}
        {% if pub.ris %}
        <a href="{{ pub.ris }}"><span class="material-symbols-outlined" aria-hidden="true">download</span><span>RIS</span></a>
        {% endif %}
        {% if pub.code %}
        <a href="{{ pub.code }}"><span class="material-symbols-outlined" aria-hidden="true">code</span><span>Code</span></a>
        {% endif %}
      </div>
      {% if pub.caption %}
      <p class="publication-caption">{{ pub.caption }}</p>
      {% endif %}
    </aside>
    {% if pub.abstract %}
    <div class="publication-abstract">
      {{ pub.abstract | markdownify }}
    </div>
    {% endif %}
  </article>
  {% endfor %}
</div>
