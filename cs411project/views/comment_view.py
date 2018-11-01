from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json


class CommentChangeView(MethodView):
        def put(self,CommentID,CommentText,isResolved):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                query = "UPDATE Comments SET CommentText = '{}' , isResolved = '{}' WHERE CommentID = '{}' ".format(newCommentText,str(isResolved),int(CommentID))
                cursor.execute(query)
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
                category = request_json["Category"] if request_json["Category"] else ""
                commentText = request_json["CommentText"] if request_json["CommentText"] else ""
                hardwareID = request_json["HardwareID"] if request_json["HardwareID"] else ""
                AuthorNetID = request_json["AuthorNetID"] if request_json["AuthorNetID"] else ""
                MachineID = request_json["MachineID"] if request_json["MachineID"] else ""
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)
                query = "INSERT INTO Comments (Category,CommentText,isResolved, HardwareID,AuthorNetID,MachineID) VALUES(%s,%s,0,%s,%s,%s)"
                cursor.execute(query,(category,commentText,hardwareID,AuthorNetID,MachineID))
                connection.commit()
                cursor.close()
                return jsonify({'Result': True})