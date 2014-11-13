#encoding=UTF8

from flask import request
from www.base import WebView

class AdminView(WebView):
    def __init__(self):
        super(AdminView, self).__init__(__file__)
        self.assign("layout", request.args.get("layout", "default"))

