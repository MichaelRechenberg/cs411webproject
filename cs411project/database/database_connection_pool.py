import mysql.connector.pooling

class MySQLConnectionPool:
    """Class to encapusate a connection pool with MySQL
    """

    def __init__(self, connection_pool_name: str, pool_size: int, dbconfig: dict):
        """Initialize a connection pool with MySQL


            Args:
                connection_pool_name: The name to use for the connection pool
                pool_size: The number of connections to have in the pool
                dbconfig: Dictionary of kwargs to pass to mysql.connector.pooling.MySQLConnectionPool

            Additional Notes:
                
                Example dbconfig:
                
                {
                  'database': 'some_database_name',
                  'user':     'some_user',
                  'password': 'hunter2'
                }
                
                So all connections taken from the pool configured with the
                  above config will be made against the database some_database_name
                  under the user some_user, logging in with password hunter2
                
                If creation of the pool fails, an exception is thrown

        """
        self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                                    pool_name=connection_pool_name,
                                    pool_size=pool_size,
                                    **dbconfig)

    def get_connection(self):
        """Return a new connection from the connection pool, throwing an error if no
            connections are available
        """
        return self.connection_pool.get_connection()


