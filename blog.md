---
layout: page
title: Blog
---
	
<h2>Browse all posts by month and year.</h2>

{% assign postsByYearMonth = site.posts | group_by_exp: "post", "post.date | date: '%B %Y'" %}
{% for yearMonth in postsByYearMonth %}
  <h2>{{ yearMonth.name }}</h2>
  <ul>
    {% for post in yearMonth.items %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}

<h2>Browse all posts by tags</h2>

{% capture tags %}
  {% for tag in site.tags %}
    {{ tag[0] }}
  {% endfor %}
{% endcapture %}
{% assign sortedtags = tags | split:' ' | sort %}

{% for tag in sortedtags %}
  <h3 id="{{ tag }}">{{ tag }}</h3>
  <ul>
  {% for post in site.tags[tag] %}
  <li><a href="{{ post.url }}">{{ post.title }}</a>
    <span class="post-date">{{ post.date | date_to_string }}</span>
  </li>
  
  {% endfor %}
  </ul>
{% endfor %}
