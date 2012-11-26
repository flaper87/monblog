#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

import conf
import jinjatag
from log import logger


class Application(Flask):

    def __init__(self, name=None, apps=None, *args, **kwargs):
        super(Application, self).__init__(name or __name__, *args, **kwargs)
        self._apps = apps or []
        self.debug = conf.DEBUG
        jinja_tag = jinjatag.JinjaTag()
        self.jinja_options["extensions"].append(jinja_tag)
        self.jinja_env
        jinja_tag.init()

    def load_apps(self, apps=None):
        for app in apps or self._apps:
            for mod in ["views", "models", "filters"]:
                try:
                    __import__("monblog.%s.%s" % (app, mod),
                                                  globals(),
                                                  locals())
                except ImportError, e:
                    logger.debug("Import error importing %s" % e)
            if not app in self._apps:
                self._apps.append(app)

app = Application(apps=conf.APPS)


@app.context_processor
def template_context():
    data = {
        "STATIC_URL": app.static_url_path,
        "TEMPLATE_THEME": conf.TEMPLATE_THEME,
    }
    data.update(conf.BLOG_SETTINGS)
    return data
