from flask import g
from flask.views import MethodView
from flask.json import jsonify
from ..database.entity_serializer import EntitySerializer
from ..database.constants import MACHINE_STATUS_BROKEN, MACHINE_STATUS_ALIVE, STUB_LOCATION_DICT




# A simple test View to make sure the pipes fit with cPanel
class BulkMachineAvailabilityView(MethodView):

    def get(self):
        """Returns the availability of all machines and their locations in the UI as a list of JSON objects
        """
        # This connection will automatically be closed when the HTTP request finishes (and on error)
        connection = g.mysql_connection.get_connection()

        # But we are responsible for closing the cursor ourselves in this function
        cursor = connection.cursor(prepared=True)

        # LEFT JOIN because of a MachineID does not have a heartbeat sequence yet, we assume that no one has used that
        #   machine ever before
        query = """
                    SELECT
                      M.MachineID,
                      CASE WHEN M.Status = %s
                            THEN 'BROKEN' 
                           WHEN M.Status = %s AND tmp2.StillInUse = 1 
                            THEN 'IN-USE'
                           ELSE
                            'AVAILABLE'
                      END AS MachineAvailability
                    FROM Machine M
                    LEFT JOIN (SELECT HS.MachineID, SUBTIME(CURRENT_TIMESTAMP, HS.Tfail) <= tmp.LatestHeartbeatTS AS StillInUse
                          FROM
                            (SELECT MachineID,
                                 CASE WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS) ELSE MAX(FirstTS) END AS LatestHeartbeatTS
                             FROM HeartbeatSequence
                            GROUP BY MachineID) tmp
                          JOIN HeartbeatSequence HS
                            ON (tmp.LatestHeartbeatTS = HS.FirstTS OR tmp.LatestHeartbeatTS = HS.LastTS) AND tmp.MachineID = HS.MachineID) tmp2
                    ON M.MachineID = tmp2.MachineID;
                """

        cursor.execute(query, (MACHINE_STATUS_BROKEN, MACHINE_STATUS_ALIVE))



        # We can get the column names for each resulting SQL query from the cursor,
        #   then use those as keys in Python dictionaries
        # Or, we could use our own list of names for each column of a tuple returned by the DB
        field_names = [x[0] for x in cursor.description]

        # We use the list() to force the generator of the cursor to read the results of the query
        #   Otherwise, MySQL will complain that we closed the cursor with unread results
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))

        # Append location information from MachineLocation
        query2 = "SELECT * FROM MachineLocation"
        cursor.execute(query2)
        all_machine_locations_list = list(cursor)
        all_machine_locations_dict = {machine_id:{'x':x_coord, 'y':y_coord} for (machine_id, x_coord, y_coord) in all_machine_locations_list}

        for result_dict in result_as_dicts:
            machineID = result_dict['MachineID']
            result_dict['location'] = all_machine_locations_dict.get(machineID, {'x': "LOCATION NOT FOUND", 'y': "LOCATION NOT FOUND"})

        cursor.close()

        # We have the result set returned as JSON
        return jsonify(result_as_dicts)


class MachineAvailabilityView(MethodView):

    def get(self, machineID):
        """Returns the availability and location in the UI of a single machine as a JSON object


            Args:
                machineID: The integer machine ID
        """

        connection = g.mysql_connection.get_connection()

        cursor = connection.cursor(prepared=True)

        query = """
                SELECT
                  CASE WHEN Status = (%s)
                        THEN 'BROKEN' 
                       WHEN Status = (%s) AND (
                          /* If the last heartbeat for a machine occurred AFTER (Tfail amount of time BEFORE the current time), then the machine is still in use */
                          SELECT SUBTIME(CURRENT_TIMESTAMP, Tfail) <= (CASE WHEN (LastTS IS NULL) THEN FirstTS ELSE LastTS END) AS StillInUse
                          FROM HeartbeatSequence
                          WHERE (LastTS = (SELECT CASE 
                                              /* Find the last timestamp between the FirstTS and LastTS columns out of all HeartbeatSequence rows */
                                              WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS)
                                              ELSE MAX(FirstTS) END
                                              FROM HeartbeatSequence
                                              WHERE MachineID = (%s)) OR
                                FirstTS = (SELECT CASE 
                                              WHEN MAX(LastTS) > MAX(FirstTS) THEN MAX(LastTS)
                                              ELSE MAX(FirstTS) END
                                              FROM HeartbeatSequence
                                              WHERE MachineID = (%s)))
                                AND MachineID = (%s) 
                       ) 
                        THEN 'IN-USE'
                       ELSE
                        'AVAILABLE'
                  END AS MachineAvailability
                FROM Machine WHERE MachineID = (%s)
                """

        query_args = (MACHINE_STATUS_BROKEN, MACHINE_STATUS_ALIVE, machineID, machineID, machineID, machineID)

        cursor.execute(query, query_args)

        field_names = [x[0] for x in cursor.description]

        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))
        query2 = "SELECT * FROM MachineLocation WHERE MachineID = %s"
        cursor.execute(query2, (machineID,))

        # Append location information
        all_machine_locations_list = list(cursor)
        all_machine_locations_dict = {machine_id:{'x':x_coord, 'y':y_coord} for (machine_id, x_coord, y_coord) in all_machine_locations_list}


        for result_dict in result_as_dicts:
            result_dict['location'] = all_machine_locations_dict[machineID]


        cursor.close()

        result = {}
        # Only send one JSON object in the request
        if len(result_as_dicts) > 0:
            result = result_as_dicts[0]

        return jsonify(result)

