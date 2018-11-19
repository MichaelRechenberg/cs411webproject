from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer
import mysql.connector

import json

class SpecificUserView(MethodView):
        def get(self,NetID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)
                query = "SELECT * FROM Users WHERE Users.NETID = %s"
                cursor.execute(query,(NetID,))
                col_names = [x[0] for x in cursor.description]
                result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))
                cursor.close()

                if len(result_as_dicts) == 0:
                    return jsonify("User with netID {0} does not exist".format(NetID)), 400
                else:
                    return jsonify(result_as_dicts[0])



class UsersView(MethodView):

    def get(self):
        connection = g.mysql_connection.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Users"
        cursor.execute(query)
        field_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))
        cursor.close()
        return jsonify(result_as_dicts)


class NewUserView(MethodView):
    def post(self):
        connection = g.mysql_connection.get_connection()
        cursor = connection.cursor(prepared=True)
        request_json = request.get_json()

        netID = request_json["NetID"] if "NetID" in request_json else None
        is_TA = request_json["isTA"] if "isTA" in request_json else None
        first_name = request_json["FirstName"] if "FirstName" in request_json else None
        last_name = request_json["LastName"] if "LastName" in request_json else None

        if all([x is not None for x in [netID, is_TA, first_name, last_name]]):
            query = "INSERT INTO Users(NetID, isTA, FirstName, LastName) VALUES ((%s), (%s), (%s), (%s))"

            response = 500
            try:
                cursor.execute(query, (netID, is_TA, first_name, last_name))
            except mysql.connector.IntegrityError as integrity_error:
                response = jsonify({"error": "INSERT rejected because a User already exists with the supplied netID"}), 400
                connection.rollback()
            except mysql.connector.Error as err:
                response = jsonify({"error": "Unknown database error"}), 500
                connection.rollback()
            else:
                response = jsonify({"message": "Success"}), 202
            finally:
                cursor.close()
                connection.commit()
                return response
        else:
            return jsonify({"error": "Missing required fields for creating a new user"}), 400

