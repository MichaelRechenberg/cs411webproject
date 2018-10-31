from flask.views import View
from flask import Flask, render_template

class editView(View):

    def dispatch_request(self):
        return render_template('editComment.html')