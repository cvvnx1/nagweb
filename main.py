#!/usr/bin/env python

__title__ = "nagweb"
__author__ = "cvvnx1@163.com"

from flask import Flask
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__, template_folder="www/templates", static_folder="www/static")
app.debug = True
app.secret_key = "6d8908651d84f69b26c5afd5102d50ec"

def register_view():
    import www.admin as admin
    admin.host.ListView.register(app, route_prefix="/admin/")
    admin.host.EditHostView.register(app, route_prefix="/admin/")
    admin.host.EditHostgroupView.register(app, route_prefix="/admin/")
    admin.host.AddHostView.register(app, route_prefix="/admin/")
    admin.host.AddHostgroupView.register(app, route_prefix="/admin/")

if __name__ == "__main__":
    register_view()
    app.run(host="0.0.0.0", port=1236)

