# Adam's Comment view
from flask.views import View
from flask import Flask, render_template, session, redirect, request, url_for

class loginView(View):

        def dispatch_request(self):
                return render_template('login.html')

class loginError(View):

        def dispatch_request(self):
                return render_template('login.html', errorMessage="User not found")

class loginMachineError(View):

        def dispatch_request(self):
                return render_template('login.html', errorMessage="Machine ID does not exist")

class logoutUser(View):

        def dispatch_request(self):
                session.clear()
                return redirect(url_for('loginPage'))


class loginUser(View):

        def dispatch_request(self, NetId):
                session['netId'] = NetId
                return redirect(url_for('mainPage'))