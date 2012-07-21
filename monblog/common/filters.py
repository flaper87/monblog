import datetime

from monblog.app import app

def datetime_filter(date, fmt='%c'):
    # check whether the value is a datetime object
    if not isinstance(date, (datetime.date, datetime.datetime)):
        try:
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
        except Exception, e:
            return date
    return date.strftime(fmt)

app.jinja_env.filters['datetime'] = datetime_filter

def markdown(text):
    # check whether the value is a datetime object
    from markdown2 import markdown
    return markdown(text.encode('utf-8')).decode('utf-8')

app.jinja_env.filters['markdown'] = markdown
