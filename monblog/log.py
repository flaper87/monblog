#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf
import logging

logger = logging.getLogger(__name__)
logger.setLevel(conf.DEBUG and 10 or 20)

ch = logging.StreamHandler()
FORMAT = '%(asctime)-15s %(message)s'
ch.setFormatter(logging.Formatter(FORMAT))

logger.addHandler(ch)
