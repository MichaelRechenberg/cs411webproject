from flask.views import View
from flask import Flask, render_template, session, redirect, url_for

class mainView(View):

    def dispatch_request(self):
        if('netId' in session and 'machineId' in session):
            return render_template('mainView.html', netId=session['netId'], machineId=session['machineId'])
        else:
            return redirect(url_for('loginPage'))
