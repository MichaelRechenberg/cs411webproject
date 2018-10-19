from flask import g
from flask.views import MethodView

import json

# A simple test View to make sure the pipes fit with cPanel
class TestAPIView(MethodView):

    def get(self):
        # TODO: make this more testable by having a TestAPIView take a MySQLConnection in its constructor
        #   (but Flask is dumb and dependency injection isn't well supplied by default) instead of using magic g
        # "Ask, don't take"

        # This connection will automatically be closed when the HTTP request finishes (and on error)
        connection = g.mysql_connection.get_connection()

        # But we are responsible for closing the cursor ourselves in this function
        cursor = connection.cursor()

        # TODO: change this to SELECT from a table in cPanel for example
        query = 'SELECT * FROM TestDB'

        cursor.execute(query)


        # force loading of results before closing the cursor
        loaded_results = list(cursor)

        cursor.close()

        return json.dumps(loaded_results)

