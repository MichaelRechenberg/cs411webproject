import os
from flask import g, Flask, request


from .cs411project.database.database_connection import MySQLConnection
from .cs411project.views.home_view import HomeView
from .cs411project.views.user_view import UsersView,SpecificUserView
from .cs411project.views.machine_view import MachinesView,SpecificMachineView,SpecificMachineCommentsView
from .cs411project.views.comment_view import CommentView,CommentChangeView

# Create flask app
# TODO: specify static_folder and template_folder in this constructor
app = Flask(__name__)


# Any global configuration (e.g. database configurations, before_request handlers)
app.config.update(
    # User to login to the MySQL database with
    MYSQL_USER = os.environ['CS411_MYSQL_USER'],
    # Password to use to login to the MySQL database with
    MYSQL_PASSWORD = os.environ['CS411_MYSQL_PASSWORD'],
    # Name of database to connect to by default
    MYSQL_DATABASE = os.environ['CS411_MYSQL_DATABASE'])



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

app.add_url_rule('/project', view_func=HomeView.as_view('home'))
app.add_url_rule('/project/users/all', view_func=UsersView.as_view('users'))
app.add_url_rule('/project/machines/all',view_func=MachinesView.as_view('machines'))

app.add_url_rule('/project/users/<NetID>', view_func=SpecificUserView.as_view('specificUser'))
app.add_url_rule('/project/machines/<MachineID>', view_func=SpecificMachineView.as_view('specificMachine'))

app.add_url_rule('/project/machines/comments/<MachineID>', view_func=SpecificMachineCommentsView.as_view('specificMachineComments'))


app.add_url_rule('/project/comment/insert', view_func=CommentView.as_view('comment'))
app.add_url_rule('/project/comment/<CommentID>', view_func=CommentChangeView.as_view('commentChange'))
app.add_url_rule('/project/comment/delete/<CommentID>', view_func=CommentChangeView.as_view('commentDelete'))



app.run(port=8082)
application = app