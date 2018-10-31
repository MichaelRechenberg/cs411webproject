from flask import g
from flask.views import MethodView
from ..database.entity_serializer import EntitySerializer

import json


class CommentChangeView(MethodView):
        def put(self,CommentID,CommentText,isResolved):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                newCommentText = str(CommentText).replace("_"," ")
                query = "UPDATE Comments SET CommentText = '{}' , isResolved = '{}' WHERE CommentID = '{}' ".format(newCommentText,str(isResolved),int(CommentID))
                cursor.execute(query)
                connection.commit()
                cursor.close()
                return json.dumps(query)

        def delete(self,CommentID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                query = "DELETE FROM Comments WHERE Comments.CommentID = '{}' ".format(str(CommentID))
                cursor.execute(query)
                connection.commit()
                cursor.close()
                return json.dumps(query)




class CommentView(MethodView):
        def post(self,MachineID,AuthorNetID,Category,CommentText):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                newCommentText = str(CommentText).replace("_"," ")
                query = "INSERT INTO Comments (CommentID,LastModifiedTS, Category,CommentText,isResolved, HardwareID,AuthorNetID,MachineID) VALUES(NULL,NULL,'{}','{}',0,NULL,'{}','{}')".format(str(Category),newCommentText,str(AuthorNetID),str(MachineID))
                cursor.execute(query)
                connection.commit()
                cursor.close()
                return json.dumps(query)
