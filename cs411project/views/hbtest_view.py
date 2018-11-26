from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json

class HBView(MethodView):
	def get(self,NetID,MachineID):
		cursor = g.mysql_connection.get_connection().cursor(prepared=True)
		#curosr = connection.cursor(prepared=True)
		#cursor = connectoin.cursor()
		#query = "SELECT * FROM Machine WHERE MachineID = %s"
		query = """SELECT NetID,SeqID
                           FROM HeartbeatSequence
                           WHERE SeqID IN 
                               (SELECT Max(SeqID) AS M
                               FROM HeartbeatSequence
                               WHERE MachineID = %s
                               GROUP BY MachineID)
                               AND
                               NetID = (%s)
                               AND
                               ((LastTS IS NOT NULL AND NOT (LastTS + Tfail < CURRENT_TIMESTAMP))
                               OR
                               (LastTS IS NULL AND NOT (FirstTS + Tfail < CURRENT_TIMESTAMP)))"""
		cursor.execute(query,(MachineID,NetID,))
		result = list(cursor)
		#cursor.close()
		if not result:
			query2 = "INSERT INTO HeartbeatSequence(NetID, MachineID) Values (%s, %s)"
			cursor.execute(query2, (NetID, MachineID,))
			g.mysql_connection.get_connection().commit()
			cursor.close()
			#connection.close()
			return jsonify("inserted new row")
		else:
			query2 = "UPDATE HeartbeatSequence SET NumHeartbeats = NumHeartbeats + 1 WHERE SeqID = %s"
			cursor.execute(query2,(result[0][1],))
			g.mysql_connection.get_connection().commit()
			cursor.close()
			#connection.close()
			return jsonify(result)
		#col_names = [x[0] for x in cursor.description]
		#result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
		#cursor.close()
		#return jsonify(result)


