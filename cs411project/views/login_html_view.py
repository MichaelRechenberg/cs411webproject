# Adam's Comment view
from flask.views import View
from flask import Flask, render_template, session, redirect, request, url_for

class loginView(View):

        def dispatch_request(self):
                return render_template('login.html')

class logoutUser(View):

        def dispatch_request(self):
                session.clear()
                return redirect(url_for('loginPage'))


class loginUser(View):
        methods = ['GET', 'POST']
        def dispatch_request(self):
                if request.method == 'POST':
                        netID = request.form['NetId']
                        session['netId'] = netID
                        return redirect(url_for('mainPage'))