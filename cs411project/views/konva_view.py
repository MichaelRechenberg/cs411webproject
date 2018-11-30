from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json

class KonvaView(MethodView):
  def post(self):
    request_json = request.get_json()
    if request_json:
      arg_count = len(request_json)
    else:
      return jsonify([])
    NetID = request_json["NetID"]
    locations = request_json["locations"]
    connection = g.mysql_connection.get_connection()
    cursor = connection.cursor(prepared=True)
    cursor.execute("SELECT * FROM Users WHERE NetID = %s AND isTA = 1", (NetID,))
    result = list(cursor)
    if result:
      for machine_dict in locations:
        machineID = machine_dict["MachineID"]
        x = machine_dict["location"]["x"]
        y = machine_dict["location"]["y"]
        cursor.execute("UPDATE MachineLocation SET X_COORDINATE = %s, Y_COORDINATE = %s  WHERE MachineID = %s", (x,y,machineID,))
    else:
      return (jsonify("You are NOT a TA!"), 400)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify([])
