# -*- coding: utf-8 -*-

from urlparse import urljoin
from bson.objectid import ObjectId
from werkzeug.contrib.atom import AtomFeed
from flask import request, render_template, url_for, redirect

# Monblog
from ..app import app
from .. import db, conf
from ..common.filters import markdown

PAGE_SIZE = 50


@app.route('/', methods=["GET"])
def index():
    posts = db.find("posts.files", {}).sort([("uploadDate", -1)]).limit(3)
    return render_template('%s/base.html' % conf.TEMPLATE_THEME, posts=posts)


def _posts(query=None):
    try:
        page = int(request.values.get("page", 0))
    except ValueError:
        page = 0

    posts = db.find("posts.files", query or {}).\
        sort([("uploadDate", -1)]).\
        skip(page * PAGE_SIZE).limit(PAGE_SIZE)
    return render_template('%s/posts.html' % conf.TEMPLATE_THEME,
                            posts=posts, query=query)


@app.route('/posts', methods=["GET"])
def get_posts():
    return _posts()


@app.route('/tag/<tag>/', methods=["GET"])
def get_posts_by_tag(tag):
    return _posts({"metadata.tags": tag})


def _feeds(query=None, title='Recent Articles'):
    posts = db.find("posts.files", query or {}).\
        sort([("uploadDate", -1)]).limit(PAGE_SIZE)

    feed = AtomFeed(title,
                    feed_url=request.url,
                    url=request.url_root)

    from monblog.common.encodings import force_bytes

    for post in posts:
        author = conf.BLOG_SETTINGS.get("AUTHOR", "")
        url = urljoin(request.url_root,
            url_for("get_post", post_id=str(post["_id"])))
        text = force_bytes(db.fs.get(ObjectId(post["_id"])).read(),
                                        "ascii", errors="ignore")
        feed.add(post["metadata"].get("title"), markdown(text),
                 id=url, content_type='html', url=url,
                 updated=post["uploadDate"],
                 published=post["uploadDate"],
                 author=post["metadata"].get("author", author))

    return feed.get_response()


@app.route('/post/<post_id>/', methods=["GET"])
def get_post(post_id):
    post = db.fs.get(ObjectId(post_id))
    db.update("posts.files",
              {"_id": ObjectId(post_id)},
              {"$inc": {"metadata.reads": 1}})
    return render_template('%s/post.html' % conf.TEMPLATE_THEME,
                           post=post, **post.metadata)


@app.route('/post/file/<filename>/', methods=["GET"])
def get_post_by_filename(filename):
    post = db.fs.get_last_version(filename=filename)
    return redirect(url_for('get_post', post_id=post._id))


@app.route('/feeds/latest/', methods=["GET"])
def recent_feeds():
    return _feeds()


@app.route('/feeds/latest/tag/<tag>/', methods=["GET"])
def recent_feeds_by_tag(tag):
    return _feeds({"metadata.tags": tag},
                  title='Recent Articles for tag %s' % tag)
