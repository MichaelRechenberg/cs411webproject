from flask import g
from flask.views import MethodView
from flask.json import jsonify
from ..database.entity_serializer import EntitySerializer

import json

class InsertHB(MethodView):

    def get(self, netID, machineID):
        """netID is a string given from URL
        """

        connection = g.mysql_connection.get_connection()

        cursor = connection.cursor(prepared=True)

        #query = 'INSERT INTO HeartbeatSequence(Tfail, NumHeartBeats, NetID, MachineID, FirstTS, LastTS) VALUES (%s, 1, %s, %s, SUBTIME(CURRENT_TIMESTAMP, %s), SUBTIME(CURRENT_TIMESTAMP,%s));'
        #query_args = ('00:05:00',netID,machineID, '00:10:00', '00:09:00')
	
        query = """
                SELECT NetID, FirstTS, LastTS, Tfail, SeqID
                FROM HeartbeatSequence
                WHERE SeqID =
                    (SELECT Max(SeqID) AS M
                    FROM HeartbeatSequence
                    WHERE MachineID = %s
                    GROUP BY MachineID)
                    AND
                    NetID = %s
                """


        cursor.execute(query, (machineID, netID))

        field_names = [x[0] for x in cursor.description]

        # We use the list() to force the generator of the cursor to read the results of the query
        #   Otherwise, MySQL will complain that we closed the cursor with unread results
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))

        # if not result:
        #     query = """
        #             INSERT INTO HeartbeatSequence 
        #             (`NetID`, `MachineID`) 
        #             VALUES (%s,%s)
        #             """
        #     cursor.execute(query, (netID, machineID))
        # else if result[0]['LastTS'] is None:
        #     if result[0]['FirstTS'] + result[0]['Tfail'] < CURRENT_TIMESTAMP:
        #         query = """
        #             INSERT INTO HeartbeatSequence 
        #             (`NetID`, `MachineID`) 
        #             VALUES (%s,%s)
        #             """
        #         cursor.execute(query, (netID, machineID))
        #     else:
        #         query = """
        #             UPDATE `HeartbeatSequence` SET NumHeartbeats = NumHeartbeats + 1 WHERE SeqID = %i
        #             """
        #         cursor.execute(query, (result[0]['SeqID']))
        # else:
        #     if result[0]['LastTS'] + result[0]['Tfail'] < CURRENT_TIMESTAMP:
        #         query = """
        #             INSERT INTO HeartbeatSequence 
        #             (`NetID`, `MachineID`) 
        #             VALUES (%s,%s)
        #             """
        #         cursor.execute(query, (netID, machineID))
        #     else:
        #         query = """
        #             UPDATE `HeartbeatSequence` SET NumHeartbeats = NumHeartbeats + 1 WHERE SeqID = %i
        #             """
        #         cursor.execute(query, (result[0]['SeqID']))

        cursor.close()

        result = {}
        if len(result_as_dicts) > 0:
            result = result_as_dicts[0]

        return jsonify(result_as_dicts)