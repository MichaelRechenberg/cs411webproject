import os
from flask import g, Flask, request, session
from flask_cors import CORS
from flask_session import Session



from .cs411project.database.database_connection import MySQLConnection

from .cs411project.views.main_view import mainView
from .cs411project.views.comment_html_view import CommentHTMLView
from .cs411project.views.comment_view import CommentChangeView, CommentView, AllDownageCategoriesView
from .cs411project.views.login_html_view import loginView, loginUser, logoutUser, loginError, loginMachineError
from .cs411project.views.comment_view import CommentChangeView, CommentView
from .cs411project.views.edit_view import editView
from .cs411project.views.machine_availability_view import BulkMachineAvailabilityView, MachineAvailabilityView
from .cs411project.views.machine_view import SpecificMachineView, MachinesView
from .cs411project.views.query_comment import QueryCommentView
from .cs411project.views.test_view import TestAPIView, TestPreparedStatementAPIView
from .cs411project.views.user_view import SpecificUserView, UsersView, NewUserView
from .cs411project.views.downage_category_view import SimpleDownageCategoryView, \
        SimpleDownageCategoryStartBatchView, MixtureModelDownageCategoryStartBatchView, \
        MixtureModelDownageCategoryView, DownageCategoriesEditingExistingCommentView
from .cs411project.views.user_view import SpecificUserView, UsersView
from .cs411project.views.hbtest_view import HBView
from .cs411project.views.ajax_view import AjaxView

# Create flask app
# TODO: specify static_folder and template_folder in this constructor
app = Flask(__name__, template_folder="cs411project/templates", static_folder="cs411project/templates/static")

# Enable CORS across all requests (later this can be on a per URL/regex level)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)
Session(app)

# Any global configuration (e.g. database configurations, before_request handlers)
app.config.update(
    # User to login to the MySQL database with
    MYSQL_USER = os.environ['CS411_MYSQL_USER'],
    # Password to use to login to the MySQL database with
    MYSQL_PASSWORD = os.environ['CS411_MYSQL_PASSWORD'],
    # Name of database to connect to by default
    MYSQL_DATABASE = os.environ['CS411_MYSQL_DATABASE']
)



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

# API endpoints
# User API
app.add_url_rule('/project/users/<NetID>', view_func=SpecificUserView.as_view('specificUser'))
app.add_url_rule('/project/users/all', view_func=UsersView.as_view('users'))
app.add_url_rule('/project/users/new', view_func=NewUserView.as_view('newUser'))

# Machine API
app.add_url_rule('/project/machines/all',view_func=MachinesView.as_view('machines'))
app.add_url_rule('/project/machines/<MachineID>', view_func=SpecificMachineView.as_view('specificMachine'))
app.add_url_rule('/project/machine/availability', view_func=BulkMachineAvailabilityView.as_view('bulk_machine_avail'))
app.add_url_rule('/project/machine/availability/<int:machineID>', view_func=MachineAvailabilityView.as_view('machine_avail'))

# Comment API
app.add_url_rule('/project/comment/query', view_func=QueryCommentView.as_view('query_comment'))
app.add_url_rule('/project/comment/<comment_id>', view_func=CommentView.as_view('get_specific_comment'))
app.add_url_rule('/project/comment/insert', view_func=CommentView.as_view('comment'))
app.add_url_rule('/project/comment/update/<CommentID>', view_func=CommentChangeView.as_view('commentChange'))
app.add_url_rule('/project/comment/delete/<CommentID>', view_func=CommentChangeView.as_view('commentDelete'))
app.add_url_rule('/project/comment/all-downage-categories', view_func=AllDownageCategoriesView.as_view('getAllDownageCategories'))

# Downage Category API
app.add_url_rule('/project/downage-category/simple/startBatch', view_func=SimpleDownageCategoryStartBatchView.as_view('downageCategorySimpleStartBatch'))
app.add_url_rule('/project/downage-category/simple', view_func=SimpleDownageCategoryView.as_view('downageCategorySimpleGET'))
app.add_url_rule('/project/downage-category/mixture/startBatch', view_func=MixtureModelDownageCategoryStartBatchView.as_view('downageCategoryMixtureStartBatch'))
app.add_url_rule('/project/downage-category/mixture/<int:machine_id>', view_func=MixtureModelDownageCategoryView.as_view('downageCategoryMixtureGET'))
app.add_url_rule('/project/downage-category/editing-comment/<int:comment_id>', view_func=DownageCategoriesEditingExistingCommentView.as_view('downageCategoryEditingComment'))

# Login API
app.add_url_rule('/login/<NetId>/<isTA>', view_func=loginUser.as_view('login'))
app.add_url_rule('/logout', view_func=logoutUser.as_view('logout'))


# HTML endpoints
app.add_url_rule('/home', view_func=mainView.as_view('mainPage'))
app.add_url_rule('/comment', view_func=CommentHTMLView.as_view('commentPage'))
app.add_url_rule('/comment/edit/<comment>', view_func=editView.as_view('editCommentPage'))
app.add_url_rule('/login', view_func=loginView.as_view('loginPage'))
app.add_url_rule('/login/error', view_func=loginError.as_view('loginError'))
app.add_url_rule('/login/MachineError', view_func=loginMachineError.as_view('loginMachineError'))

app.add_url_rule('/testingajax', view_func=AjaxView.as_view('testajax'))
app.add_url_rule('/project/hb/<NetID>/<MachineID>', view_func=HBView.as_view('hb'))
# Set variable to application so cPanel can use our Flask app
application = app
