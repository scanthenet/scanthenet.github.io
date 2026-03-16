---
layout: default
title: Labs
permalink: /labs/
---

<div class="wrapper" style="padding-top: 2.5rem;">
  <h1 style="font-family: var(--font-head); margin-bottom: 0.5rem;">
    <span style="color: var(--accent)">// </span>Labs Propios
  </h1>
  <p style="color: var(--text-muted); margin-bottom: 2.5rem; font-size: 0.9rem;">
    Entornos controlados, técnicas y experimentos de laboratorio.
  </p>

  <ul class="post-list">
    {% for post in site.posts %}
      {% if post.categories contains 'Lab' or post.categories contains 'Labs' %}
      <li>
        <div class="post-meta">
          <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%d %b %Y" }}</time>
        </div>
        <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
        {% if post.excerpt %}
          <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 25 }}</p>
        {% endif %}
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>
