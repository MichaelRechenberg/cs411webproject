from flask import g, jsonify, request
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer
from ..database.construct_comment_query import construct_comment_select_query

import json

class QueryCommentView(MethodView):

    def post(self):


        query_dict = request.json
        query, query_args = construct_comment_select_query(query_dict)

        connection = g.mysql_connection.get_connection()
        cursor = connection.cursor(prepared=True)


        cursor.execute(query, query_args)


        # We can get the column names for each resulting SQL query from the cursor,
        #   then use those as keys in Python dictionaries
        # Or, we could use our own list of names for each column of a tuple returned by the DB
        field_names = [x[0] for x in cursor.description]

        # We use the list() to force the generator of the cursor to read the results of the query
        #   Otherwise, MySQL will complain that we closed the cursor with unread results
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))

        cursor.close()

        # We have the result set returned as JSON
        return jsonify(result_as_dicts)


