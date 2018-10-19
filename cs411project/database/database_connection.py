import mysql.connector

class MySQLConnection:
    """Class to encapusate a single connection to MySQL
    """

    def __init__(self, dbconfig: dict):
        """Create a MySQLConnection (need to call get_connection to retrieve an actual connection to the database)


            Args:
                dbconfig: Dictionary of kwargs to pass to mysql.connector.connect()

            Additional Notes:
                
                Example dbconfig:
                
                {
                  'database': 'some_database_name',
                  'user':     'some_user',
                  'password': 'hunter2'
                }
                
                So all connections will be configured with the
                  above config and will be made against the database some_database_name
                  under the user some_user, logging in with password hunter2
        """
        self.dbconfig = dbconfig
        self.active_connection = None


    def get_connection(self):
        """Return a new connection to the database as defined by self.dbconfig
        """

        if self.active_connection is None:
            self.active_connection = mysql.connector.connect(**self.dbconfig)

        return self.active_connection

    def close(self):
        """Close the connection to the database (if the connection was nevery actually made with
            the MySQL database, then this function can be safely called as a no-op)
        """
        if self.active_connection is not None:
            print("Closing DB connection")
            self.active_connection.close()

        self.active_connection = None



