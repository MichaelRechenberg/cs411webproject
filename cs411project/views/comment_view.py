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

                category = request_json["Category"] if "Category" in request_json else None
                commentText = request_json["CommentText"] if "CommentText" in request_json else None
                hardwareID = request_json["HardwareID"] if "HardwareID" in request_json else None 
                authorNetID = request_json["AuthorNetID"] if "AuthorNetID" in request_json else None
                isResolved = request_json["IsResolved"] if "IsResolved" in request_json else None
                query = "UPDATE Comments SET "
                if category is not None:
                        query += "Category = (%s), "
                        args = args + (category,)
                if commentText is not None:
                        query += "CommentText = (%s), "
                        args = args + (commentText,)
                if hardwareID is not None:
                        query += "HardwareID = (%s), "
                        args = args + (hardwareID,)
                if authorNetID is not None:
                        query += "AuthorNetID = (%s), "
                        args = args + (authorNetID,)
                if isResolved is not None:
                        query += "IsResolved = (%s), "
                        args = args + (isResolved,)

                query_end = " WHERE CommentID = (%s)"
                args = args + (str(CommentID),)
                # the -2 is to remove the space and comma after adding a new attribute to update
                query = query[0:len(query) - 2] + query_end                
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True) 
                cursor.execute(query, args)


                # Update the status of the Machine M associated with this Comment C to either BROKEN or ALIVE
                #   based on if there are no more unresolved Comments for machine M after updating C
                update_machine_status_query = """
                    UPDATE Machine
                    SET Status = (SELECT CASE WHEN EXISTS (
                            SELECT * FROM Comments
                            WHERE MachineID = (SELECT MachineID FROM Comments WHERE CommentID = (%s)) AND IsResolved = 0
                        )
                        THEN 0
                        ELSE 1
			END
                    )
                    WHERE MachineID = (SELECT MachineID FROM Comments WHERE CommentID = (%s))
                """
                cursor.execute(update_machine_status_query, (CommentID, CommentID))

                connection.commit()
                cursor.close()
                return jsonify({'Result': True})

        def delete(self,CommentID):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)


                # Get the MachineID associated with the comment we are about to delete before we delete it
                get_machine_id_query = "SELECT MachineID FROM Comments WHERE CommentID = (%s)"
                cursor.execute(get_machine_id_query, (CommentID,))
                machine_id = cursor.fetchone()[0]

                # Delete the Comment
                delete_comment_query = "DELETE FROM Comments WHERE CommentID = (%s)"
                cursor.execute(delete_comment_query, (CommentID,))

                # Update the status of the Machine M associated with this Comment C to either BROKEN or ALIVE
                #   based on if there are no more unresolved Comments for machine M after deleting C
                update_machine_status_query = """
                    UPDATE Machine
                    SET Status = (SELECT CASE WHEN EXISTS (
                            SELECT * FROM Comments WHERE MachineID = (%s) AND IsResolved = 0
                        )
                        THEN 0
                        ELSE 1
			END
                    )
                    WHERE MachineID = (%s)
                """
                cursor.execute(update_machine_status_query, (machine_id, machine_id))
                connection.commit()
                cursor.close()
                return jsonify({'Result': True})




class CommentView(MethodView):
        def post(self):
                request_json = request.get_json() 
                category = request_json["Category"] if "Category" in request_json else None
                commentText = request_json["CommentText"] if "CommentText" in request_json else None
                hardwareID = request_json["HardwareID"] if "HardwareID" in request_json else None
                AuthorNetID = request_json["AuthorNetID"] if "AuthorNetID" in request_json else None
                MachineID = request_json["MachineID"] if "MachineID" in request_json else None
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)
                query = "INSERT INTO Comments (Category,CommentText,IsResolved,HardwareID,AuthorNetID,MachineID) VALUES((%s),(%s),0,(%s),(%s),(%s))"
                cursor.execute(query,(category,commentText,hardwareID,AuthorNetID,MachineID))

                # Set the machine associated with this Comment to have status BROKEN because a new comment is always unresolved
                set_machine_broken_query = "UPDATE Machine SET Status = 0 WHERE MachineID = (%s)"
                cursor.execute(set_machine_broken_query, (MachineID,))

                connection.commit()
                cursor.close()
                return jsonify({'Result': True})

        # Get the comment with this given comment_id as one JSON object (or an empty JSON object if the comment doesn't exist)
        def get(self, comment_id):
                connection  = g.mysql_connection.get_connection()
                cursor = connection.cursor(prepared=True)
                query = "SELECT * FROM Comments WHERE CommentID = (%s)"
                cursor.execute(query,(comment_id,))

                field_names = [x[0] for x in cursor.description]
                result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, field_names))
                cursor.close()

                # Only return one comment object
                return jsonify(result_as_dicts[0] if len(result_as_dicts) > 0 else {})

class AllDownageCategoriesView(MethodView):
        # Get all the distinct downage categories present in all existing comments
        def get(self):
                connection = g.mysql_connection.get_connection()
                cursor = connection.cursor()
                query = "SELECT DISTINCT Category FROM Comments"
                cursor.execute(query)
                all_downage_categories = [x[0] for x in cursor]
                cursor.close()
                return jsonify(all_downage_categories)


