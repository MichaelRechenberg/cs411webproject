import os
from flask import Flask, g
from flask_cors import CORS


from .cs411project.database.database_connection import MySQLConnection
from .cs411project.views.home_view import HomeView
from .cs411project.views.main_view import mainView
from .cs411project.views.comment_view import commentView
from .cs411project.views.edit_view import editView
from .cs411project.views.test_view import TestAPIView, TestPreparedStatementAPIView
from .cs411project.views.machine_availability_view import BulkMachineAvailabilityView, MachineAvailabilityView

# Create flask app
# TODO: specify static_folder and template_folder in this constructor
app = Flask(__name__, template_folder="cs411project/templates", static_folder="cs411project/templates/static")

# Enable CORS across all requests (later this can be on a per URL/regex level)
CORS(app)


# Any global configuration (e.g. database configurations, before_request handlers)
app.config.update(
    # User to login to the MySQL database with
    MYSQL_USER = "Foo", #os.environ['CS411_MYSQL_USER'],
    # Password to use to login to the MySQL database with
    MYSQL_PASSWORD = "foo", #os.environ['CS411_MYSQL_PASSWORD'],
    # Name of database to connect to by default
    MYSQL_DATABASE = "Foo", #os.environ['CS411_MYSQL_DATABASE']
)

# Before each request, initialize a MySQLConnection instance
#   that is available throughout the HTTP request
#
# Other Flask entities (e.g. Views) can access this MySQLConnection through
#   g.mysql_connection
@app.before_request
def before_request_prepare():
    if not hasattr(g, 'mysql_connection'):
        dbconfig = {
            'user': app.config['MYSQL_USER'],
            'password': app.config['MYSQL_PASSWORD'],
            'database': app.config['MYSQL_DATABASE']
        }
        g.mysql_connection = MySQLConnection(dbconfig)

@app.teardown_appcontext
def after_request_cleanup(error):
    """Close the mysql connection after the request has finished
    """

    if hasattr(g, 'mysql_connection'):
        g.mysql_connection.close()




# Apply routing: map URLs to the View class to handle the logic of that route
app.add_url_rule('/project/test', view_func=TestAPIView.as_view('test'))
app.add_url_rule('/project/test/<netID>', view_func=TestPreparedStatementAPIView.as_view('testPrepared'))
app.add_url_rule('/project', view_func=HomeView.as_view('home'))
app.add_url_rule('/project/machine/availability', view_func=BulkMachineAvailabilityView.as_view('bulk_machine_avail'))
app.add_url_rule('/project/machine/availability/<int:machineID>', view_func=MachineAvailabilityView.as_view('machine_avail'))
app.add_url_rule('/home', view_func=mainView.as_view('mainPage'))
app.add_url_rule('/comment', view_func=commentView.as_view('commentPage'))
app.add_url_rule('/comment/edit/<comment>', view_func=editView.as_view('editCommentPage'))




#
# The Flask app will be imported by passenger_wsgi.py in cPanel
#   to hook up Flask to cPanel's own web server via the variable 'application'
#
# If you're doing local development, you can uncomment the
#   the below line to run the Flask server locally
#
# app.run(port=8080)

application = app


