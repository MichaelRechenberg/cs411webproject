from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json


class CommentChangeView(MethodView):
        def put(self,CommentID):
                request_json = request.get_json()
                arg_count = len(request_json)
                args = ()

                category = request_json["Category"] if "Category" in request_json else ""
                commentText = request_json["CommentText"] if "CommentText" in request_json else ""
                hardwareID = request_json["HardwareID"] if "HardwareID" in request_json else ""
                AuthorNetID = request_json["AuthorNetID"] if "AuthorNetID" in request_json else ""
                query = "UPDATE Comments SET "
                if len(category) > 0:
                        query += "Category = %s, "
                        args = args + (request_json['Category'],)
                if len(commentText) > 0:
                        query += "CommentText = %s,"
                        args = args + (request_json['CommentText'],)
                if len(hardwareID) > 0:
                        query += "HardwareID = %s, "
                        args = args + (request_json['HardwareID'],)
                if len(AuthorNetID) > 0:
                        query += "AuthorNetID = %s, "
                        args = args + (request_json['AuthorNetID'],)
                query_end = " WHERE CommentID = %s"
                args = args + (str(CommentID),)
                query = query[0:len(query) - 2] + query_end                
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True) 
                cursor.execute(query, args)
                connection.commit()
                cursor.close()
                return jsonify({'Result': True})

        def delete(self,CommentID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)
                query = "DELETE FROM Comments WHERE CommentID = %s"
                cursor.execute(query,(CommentID))
                connection.commit()
                cursor.close()
                return jsonify({'Result': True})




class CommentView(MethodView):
        def post(self):
                request_json = request.get_json() 
                category = request_json["Category"] if "Category" in request_json else "NULL"
                commentText = request_json["CommentText"] if "CommentText" in request_json else "NULL"
                hardwareID = request_json["HardwareID"] if "HardwareID" in request_json else "NULL"
                AuthorNetID = request_json["AuthorNetID"] if "AuthorNetID" in request_json else "NULL"
                MachineID = request_json["MachineID"] if "MachineID" in request_json else "NULL"
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)
                query = "INSERT INTO Comments (Category,CommentText,isResolved, HardwareID,AuthorNetID,MachineID) VALUES(%s,%s,0,%s,%s,%s)"
                cursor.execute(query,(category,commentText,hardwareID,AuthorNetID,MachineID))
                connection.commit()
                cursor.close()
                return jsonify({'Result': True})