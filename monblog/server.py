import sys
from monblog.app import app


def start():
    app.load_apps()
    app.run(host="0.0.0.0", port=5000)
