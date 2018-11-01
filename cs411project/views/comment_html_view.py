# Adam's Comment view
from flask.views import View
from flask import Flask, render_template

class CommentHTMLView(View):

        def dispatch_request(self):
                    return render_template('commentSection.html')
