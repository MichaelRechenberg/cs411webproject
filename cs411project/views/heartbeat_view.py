from flask import g
from flask.views import MethodView
from flask.json import jsonify
from ..database.entity_serializer import EntitySerializer

import json

class InsertHB(MethodView):

    def get(self, NetID, machineID):
        connection  = g.mysql_connection.get_connection()
        cursor = connection.cursor(prepared=True)
        query = "SELECT * FROM Machine WHERE Machine.MachineID = %s"
        cursor.execute(query,(machineID))
        col_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
        cursor.close()
        return jsonify(col_names)