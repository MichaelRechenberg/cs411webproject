from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json

class HBView(MethodView):
	def post(self,NetID,MachineID):
		cursor = g.mysql_connection.get_connection().cursor(prepared=True)
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
		#Find the most recent heartbeat sequence with given NetID and MachineID, and its LastTS + Tfail should be less than CURRENT_TIMESTAMP, if LastTS is NULL, FirstTS + Tfail should be less than CURRENT_TIMESTAMP, meaning this sequence is within the update time window. If we didn't find such sequence (result == NULL), we will go ahead and insert a new sequnce, otherwise we will update the returned sequence. 
		if not result:
			cursor.execute("UPDATE Machine SET NetIDofLastUsed = %s WHERE MachineID = %s", (NetID, MachineID,))
			query2 = "INSERT INTO HeartbeatSequence(NetID, MachineID) Values (%s, %s)"
			cursor.execute(query2, (NetID, MachineID,))
			g.mysql_connection.get_connection().commit()
			cursor.close()
			return jsonify("inserted new row")
		else:
			cursor.execute("UPDATE Machine SET NetIDofLastUsed = %s WHERE MachineID = %s", (NetID, MachineID,))
			query2 = "UPDATE HeartbeatSequence SET NumHeartbeats = NumHeartbeats + 1 WHERE SeqID = %s"
			cursor.execute(query2,(result[0][1],))
			g.mysql_connection.get_connection().commit()
			cursor.close()
			return jsonify(result)


