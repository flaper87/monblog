#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

# Monblog
from monblog import conf
from monblog.app import app


def serve(parser):
    parser.add_argument("-b", "--bind",
                      dest="bind",
                      default="0.0.0.0",
                      help="bind")

    parser.add_argument("-p", "--port",
                      type=int,
                      default=5000,
                      dest="port",
                      help="port")
    options = parser.parse_known_args()[0]

    app.load_apps()
    app.run(host=options.bind, port=options.port)


def upload(parser):
    import simplejson
    from monblog import db

    parser.add_argument("-f", "--file",
                        dest="file",
                        help="bind")
    options = parser.parse_known_args()[0]

    with open(options.file, "r") as f:
        metadata = {}
        line = f.readline()
        if line.startswith('$"metadata"$'):
            _metadata = ""
            while True:
                line = f.readline()
                if line.startswith('$"metadata"$'):
                    if _metadata:
                        metadata = simplejson.loads(_metadata)
                    break
                _metadata += line.strip()
        else:
            f.seek(0)

        filename = metadata.get("filename", os.path.basename(options.file))
        new_post = db.fs.put(f, filename=filename, metadata=metadata)
        #db.fs.put(f)


def export(parser):
    pass

def monblog():

    if len(sys.argv) < 2:
        print "monblog command [options]"
        return

    command = sys.argv[1]

    # We'll parse args 2 times
    # One for global parameters
    # and the second one inside
    # the commands, if needed.
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbhost", dest="dbhost", help="dbhost")
    parser.add_argument("--dbname", dest="dbname", help="dbname")

    options = parser.parse_known_args()[0]
    if options.dbhost:
        conf.DB["CONN"]["host"] = options.dbhost

    if options.dbname:
        conf.DB["NAME"] = options.dbname

    try:
        return globals()[command](parser=argparse.ArgumentParser())
    except KeyError:
        pass

