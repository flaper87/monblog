import datetime
from functools import partial
from simplejson import dumps, loads

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
dumps = partial(dumps, default=dthandler)