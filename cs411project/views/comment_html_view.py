# Adam's Comment view
from flask.views import View
from flask import Flask, render_template, url_for, redirect, session

class CommentHTMLView(View):

        def dispatch_request(self):
                if('netId' in session):
                        return render_template('commentSection.html', netId=session['netId'])
                else:
                        return redirect(url_for('loginPage'))
