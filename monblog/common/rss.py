#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .. import conf


class Feed(object):

    def __init__(self, posts):
        self.data = {
            "link": conf.BLOG_SETTINGS.get("link", ""),
            "title": conf.BLOG_SETTINGS.get("title", ""),
            "language": conf.BLOG_SETTINGS.get("language", "en"),
            "description": conf.BLOG_SETTINGS.get("description", "")}

        items = {"items": ""}
        for item in posts:
            items["items"] += self._prepare_item(item)
        self.data.update(items)

    def _prepare_item(self, item_dict):
        item = "<item>"
        for tag, value in item_dict.items():
            item += "\n<{tag}>{value}</{tag}>".format(tag=tag, value=value)
        item += "\n</item>"
        return item

    @property
    def rss(self):
        if not hasattr(self, "_rss"):
            self._rss = """
            <?xml version="1.0" encoding="UTF-8"?>
            <rss version="0.2">
                <channel>
                    <title>{title}</title>
                    <link>{link}</link>
                    <description>{description}</description>
                    <language>{language}</language>
                    {items}
                </channel>
            </rss>
            """.format(**self.data)
        return self._rss