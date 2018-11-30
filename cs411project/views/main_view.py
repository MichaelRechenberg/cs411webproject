from flask.views import View
from flask import Flask, render_template, session, redirect, url_for

class mainView(View):

    def dispatch_request(self):
        # if('netId' in session):
        #     return render_template('mainView.html', netId=session['netId'])
        # else:
        #     return redirect(url_for('loginPage'))
        return render_template('mainView.html',netId='hop2')
