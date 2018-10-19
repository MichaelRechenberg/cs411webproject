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

        query = "SELECT * FROM Users"

        cursor.execute(query)


        #
        # If you needed to execute multiple queries in one HTTP request that couldn't be merged into a transaction,
        #   you can run cursor.execute() again to issue another query. But note that if any previous query returned
        #   results (i.e. SELECT), you need to read those results (force cursor generator to produce results
        #   with something like list()) before executing a second query that generates results. Othewise MySQL
        #   will complain about unread results
        #
        # print(list(cursor))
        # print("Exec second query")
        #
        # query = 'SELECT * From Users'
        # cursor.execute(query)
        #



        # We can get the column names for each resulting SQL query from the cursor,
        #   then use those as keys in Python dictionaries
        # Or, we could use our own list of names for each column of a tuple returned by the DB
        field_names = [x[0] for x in cursor.description]

        # We use the list() to force the generator of the cursor to read the results of the query
        #   Otherwise, MySQL will complain that we closed the cursor with unread results
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))

        cursor.close()

        # We have the result set returned as JSON
        return json.dumps(result_as_dicts)


class TestPreparedStatementAPIView(MethodView):

    def get(self, netID):
        """netID is a string given from URL
        """

        connection = g.mysql_connection.get_connection()

        cursor = connection.cursor(prepared=True)

        query = 'SELECT * FROM Users WHERE NetID = (%s) OR IsTA = (%s)'
        query_args = (netID,1)

        cursor.execute(query, query_args)

        field_names = [x[0] for x in cursor.description]

        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))

        cursor.close()

        return json.dumps(result_as_dicts)

