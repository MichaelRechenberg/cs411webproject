from flask import Flask
from cs411project.views.home_view import HomeView

# TODO: remove this
from cs411project.views.test_view import TestAPIView


# Create flask app
# TODO: specify template_folder in this constructor
app = Flask(__name__)



# Apply views, other Flask global configuration here
app.add_url_rule('/project/test/<user_id>', view_func=TestAPIView.as_view('test'))
app.add_url_rule('/project', view_func=HomeView.as_view('home'))


#
# The Flask app will be imported by passenger_wsgi.py in cPanel
#   to hook up Flask to cPanel's own web server
#
# If you're doing local development, you can uncomment the
#   the below line to run the Flask server locally
#
app.run(port=8080)


