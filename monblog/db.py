#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf
from gridfs import GridFS
from pymongo import Connection


class LazyDB(object):

    def __init__(self):
        self._db = None

    def _setup(self):
        if not object.__getattribute__(self, "_db"):
            self._db = getattr(Connection(**(conf.DB["CONN"])),
                                                   conf.DB["NAME"])

            if conf.DB.get("USERNAME") and conf.DB.get("PASSWORD"):
                global db
                db.authenticate(conf.DB.get("USERNAME"),
                                conf.DB.get("PASSWORD"))

    def __getitem__(self, name):
        object.__getattribute__(self, "_setup")()
        db = object.__getattribute__(self, "_db")

        return db.__getitem__(name)

    def __getattribute__(self, name):
        object.__getattribute__(self, "_setup")()
        db = object.__getattribute__(self, "_db")
        return getattr(db, name)

db = LazyDB()


class LazyFS(object):

    def __init__(self):
        self._fs = None

    def _setup(self):
        if not object.__getattribute__(self, "_fs"):
            # Forcing connection
            db["test"]
            self._fs = GridFS(db, collection="posts")

    def __getitem__(self, name):
        object.__getattribute__(self, "_setup")()
        fs = object.__getattribute__(self, "_fs")
        return fs.__getitem__(name)

    def __getattribute__(self, name):
        object.__getattribute__(self, "_setup")()
        fs = object.__getattribute__(self, "_fs")
        return getattr(fs, name)


fs = LazyFS()

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
