from flask import g, Flask, request
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json

class SpecificUserView(MethodView):
        def get(self,NetID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                query = str("SELECT * FROM Users WHERE Users.NetID = '{}'".format(str(NetID)))
                cursor.execute(query)
                col_names = [x[0] for x in cursor.description]
                result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
                cursor.close()
                return json.dumps(result_as_dicts)



class UsersView(MethodView):

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

        #   then use those as keys in Python dictionaries
        # Or, we could use our own list of names for each column of a tuple returned by the DB
        field_names = [x[0] for x in cursor.description]

        # We use the list() to force the generator of the cursor to read the results of the query
        #   Otherwise, MySQL will complain that we closed the cursor with unread results
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))

        cursor.close()

        # We have the result set returned as JSON
        return json.dumps(result_as_dicts)