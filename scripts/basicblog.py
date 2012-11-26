#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Used to migrate posts from basic.blog

import os
import json
import argparse


def write_post(data, outputdir=""):
    fields = data["fields"]
    metadata = {
        "md": True,
        "tags": fields["tags"].split(),
        "slug": fields["slug"],
        "title": fields["title"],
        "upload_date": fields["publish"]
    }

    path = os.path.join(outputdir, fields["slug"])
    data = ['$"metadata"$']
    data.append(json.dumps(metadata))
    data.append('$"metadata"$')
    data.append(fields["body"])

    print("Exporting %s" % fields["slug"])
    with open(path, "w") as f:
        f.write("\n".join(data).encode('utf8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file", help="file to import")
    parser.add_argument("-o", "--output", default="./", dest="output", help="output dir")

    options = parser.parse_known_args()[0]

    with open(options.file) as f:
        for post in json.load(f):
            write_post(post, outputdir=options.output)

if __name__ == '__main__':
    main()