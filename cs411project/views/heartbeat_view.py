from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json

class SpecificMachineView(MethodView):
    def get(self,MachineID):
        connection  = g.mysql_connection.get_connection()
        cursor = connection.cursor(prepared=True)
        query = "SELECT * FROM Machine WHERE Machine.MachineID = %s"
        cursor.execute(query,(MachineID))
        col_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
        cursor.close()
        return jsonify(result_as_dicts)