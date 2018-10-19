from flask import g
from flask.views import MethodView

from ..database.entity_serializer import EntitySerializer

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

        query = 'SELECT * FROM Users'

        cursor.execute(query)


        # We can get the column names for each resulting SQL query from the cursor,
        #   then use those as keys in Python dictionaries
        # Or, we could use our own list of names for each column of a tuple returned by the DB
        field_names = [x[0] for x in cursor.description]

        result_as_dicts = EntitySerializer.db_entities_to_python(cursor, field_names)

        cursor.close()

        # We have the result set returned as JSON
        return json.dumps(result_as_dicts)

