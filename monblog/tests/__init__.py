from .. import conf
from ..log import logger

for app in conf.APPS:
    try:
        __import__("monblog.%s.tests" % (app, mod),
                                        globals(),
                                        locals())
    except ImportError, e:
        logger.debug("No tests found for %s" % app)
