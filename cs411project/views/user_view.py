from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json

class SpecificUserView(MethodView):
        def get(self,NetID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)
                query = "SELECT * FROM Users WHERE Users.NETID = %s"
                cursor.execute(query,(NETID))
                col_names = [x[0] for x in cursor.description]
                result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
                cursor.close()
                return jsonify(result_as_dicts)



class UsersView(MethodView):

    def get(self):
        connection = g.mysql_connection.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Users"
        cursor.execute(query)
        field_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))
        cursor.close()
        return jsonify(result_as_dicts)