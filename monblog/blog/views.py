#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson.objectid import ObjectId
from flask import request, render_template, make_response


# Monblog
from ..app import app
from .. import db, conf
from ..common import rss

PAGE_SIZE = 10


@app.route('/', methods=["GET"])
def get_posts():
    try:
        page = int(request.values.get("page", 0))
    except ValueError:
        page = 0

    posts = db.find("posts.files").\
        sort([("uploadDate", -1)]).\
        skip(page * PAGE_SIZE).limit(PAGE_SIZE)
    return render_template('%s/posts.html' % conf.TEMPLATE_THEME, posts=posts)


@app.route('/feeds/latest', methods=["GET"])
def get_rss_latest():
    posts = db.find("posts.files").\
        sort([("uploadDate", -1)]).limit(PAGE_SIZE)

    items = []
    for post in posts:
        items.append({
            "title": post["metadata"].get("title") or posts["filename"],
            "content": db.fs.get(ObjectId(post["_id"])).read(),
            "pubDate": post["uploadDate"],
        })
    feed = rss.Feed(items)
    rv = make_response(feed.rss)
    rv.headers['Content-Type'] = 'application/rss+xml'
    return rv


@app.route('/post/<post_id>', methods=["GET"])
def get_post(post_id):
    post = db.fs.get(ObjectId(post_id))
    db.update("posts.files",
              {"_id": ObjectId(post_id)},
              {"$inc": {"metadata.reads": 1}})
    return render_template('%s/post.html' % conf.TEMPLATE_THEME,
                           post=post, **post.metadata)
