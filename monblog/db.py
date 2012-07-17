import conf
from pymongo import Connection


class LazyDB(object):

    def __init__(self):
        self._db = None

    def __getattribute__(self, name):
        if not object.__getattribute__(self, "_db"):
            self._db = getattr(Connection(**(conf.DB["CONN"])),
                                                conf.DB["NAME"])
        db = object.__getattribute__(self, "_db")
        return getattr(db, name)

db = LazyDB()

def insert(collection, *args, **kwargs):
    coll = getattr(db, collection)
    return coll.insert(*args, **kwargs)


def save(collection, *args, **kwargs):
    coll = getattr(db, collection)
    return coll.save(*args, **kwargs)


def find(collection, *args, **kwargs):
    coll = getattr(db, collection)
    return coll.find(*args, **kwargs)


def find_one(collection, *args, **kwargs):
    coll = getattr(db, collection)
    return coll.find_one(*args, **kwargs)


def update(collection, *args, **kwargs):
    coll = getattr(db, collection)
    return coll.update(*args, **kwargs)


def ensure_index(collection, *args, **kwargs):
    coll = getattr(db, collection)
    return coll.ensure_index(*args, **kwargs)
