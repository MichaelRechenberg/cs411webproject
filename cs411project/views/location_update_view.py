from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json

class LocationView(MethodView):
  def post(self):
    request_json = request.get_json()

    NetID = request_json["NetID"]
    locations = request_json["locations"]

    connection = g.mysql_connection.get_connection()
    cursor = connection.cursor(prepared=True)
    cursor.execute("SELECT * FROM Users WHERE NetID = %s AND isTA = 1", (NetID,))
    result = list(cursor)

    # User is a TA, allow the location change to go through
    if result:
      delete_all_previous_locations_query = "DELETE FROM MachineLocation"
      cursor.execute(delete_all_previous_locations_query)

      for machine_dict in locations:
        machineID = machine_dict["MachineID"]
        x = (machine_dict["location"])["x"]
        y = (machine_dict["location"])["y"]
        insert_new_location_query = "INSERT INTO MachineLocation(X_COORDINATE, Y_COORDINATE, MachineID) VALUES ((%s), (%s), (%s))"
        cursor.execute(insert_new_location_query, (x,y,machineID))

      cursor.close()
      connection.commit()
      return jsonify("Successfully updated machine locations"), 202
    else:
      cursor.close()
      connection.rollback()
      return (jsonify("You are NOT a TA! Only TAs can update machine locations"), 400)
