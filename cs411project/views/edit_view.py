from flask.views import View
from flask import Flask, render_template, session, redirect, url_for

class editView(View):

    def dispatch_request(self, comment):
        if('netId' in session):
            return render_template('editComment.html', commentId = comment, netId=session['netId'])
        else:
            return redirect(url_for('loginPage'))

        
