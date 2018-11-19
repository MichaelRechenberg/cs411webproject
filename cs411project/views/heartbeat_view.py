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
                WHERE SeqID IN
                    (SELECT Max(SeqID) AS M
                    FROM HeartbeatSequence
                    WHERE MachineID = %s
                    GROUP BY MachineID)
                    AND
                    NetID = %s
                """


        cursor.execute(query, (machineID, netID))

        result = list(cursor);

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

        return jsonify(result)