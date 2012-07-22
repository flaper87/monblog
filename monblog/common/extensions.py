import jinjatag

@jinjatag.simple_block
def recent_posts(body, number=3):
    from monblog import db
    posts = db.find("posts.files").sort([("uploadDate", -1)]).limit(number)

    rst = []
    for post in posts:
        rst.append(body.format(id=post["_id"], title=post["metadata"]["title"]))

    return "\n".join(rst)

@jinjatag.simple_block
def most_popular(body, number=3):
    from monblog import db
    posts = db.find("posts.files").sort([("metadata.reads", -1), ("uploadDate", -1)]).limit(number)

    rst = []
    for post in posts:
        rst.append(body.format(id=post["_id"], title=post["metadata"]["title"]))

    return "\n".join(rst)
