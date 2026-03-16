---
layout: default
title: HackTheBox
permalink: /htb/
---

<div class="wrapper" style="padding-top: 2.5rem;">
  <h1 style="font-family: var(--font-head); margin-bottom: 0.5rem;">
    <span style="color: var(--accent)">// </span>HackTheBox
  </h1>
  <p style="color: var(--text-muted); margin-bottom: 2.5rem; font-size: 0.9rem;">
    Writeups de máquinas y challenges de HTB.
  </p>

  <ul class="post-list">
    {% for post in site.posts %}
      {% if post.categories contains 'HTB' %}
      <li>
        <div class="post-meta">
          <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%d %b %Y" }}</time>
          {% if post.difficulty %}
            <span class="post-category">{{ post.difficulty }}</span>
          {% endif %}
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
