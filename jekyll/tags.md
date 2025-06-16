---
layout: default
title: 标签云
permalink: /tags/
---

# 标签云

本站所有标签及相关文档：

<ul>
{% assign tags_sorted = site.tags | sort %}
{% for tag in tags_sorted %}
  <li><a id="{{ tag[0] }}" href="{{ '/notes/tags/' | append: tag[0] | relative_url }}">{{ tag[0] }}</a> ({{ tag[1].size }})</li>
{% endfor %}
</ul>
