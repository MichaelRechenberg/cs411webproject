from flask import g
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json



class SpecificMachineCommentsView(MethodView):
        def get(self,MachineID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                query = str("SELECT AuthorNetID, Category, CommentText  FROM Comments WHERE Comments.MachineID = '{}'".format(str(MachineID)))
                cursor.execute(query)
                col_names = [x[0] for x in cursor.description]
                result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
                cursor.close()
                return json.dumps(result_as_dicts)

class SpecificMachineView(MethodView):
        def get(self,MachineID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                query = str("SELECT * FROM Machine WHERE Machine.MachineID = '{}'".format(str(MachineID)))
                cursor.execute(query)
                col_names = [x[0] for x in cursor.description]
                result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
                cursor.close()
                return json.dumps(result_as_dicts)


class MachinesView(MethodView):

    def get(self):
        connection = g.mysql_connection.get_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM Machine"

        cursor.execute(query)

        field_names = [x[0] for x in cursor.description]

        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))

        cursor.close()

        # We have the result set returned as JSON
        return json.dumps(result_as_dicts)