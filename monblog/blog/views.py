

from bson.objectid import ObjectId
from flask import request, render_template


# Monblog
from monblog import db
from monblog import conf
from monblog.app import app

PAGE_SIZE = 10


@app.route('/', methods=["GET"])
def get_posts():
    try:
        page = int(request.values.get("page", 0))
    except ValueError:
        page = 0

    posts = db.find("posts.files").sort([("_id", -1)]).skip(page * PAGE_SIZE).limit(PAGE_SIZE)
    return render_template('%s/posts.html' % conf.TEMPLATE_THEME, posts=posts)
   # return list(


@app.route('/post/<post_id>', methods=["GET"])
def get_post(post_id):
    return post_id
