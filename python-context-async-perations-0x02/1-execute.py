import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword"
)

class ExecuteQuery:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None


    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")

            # Re-raise the exception to indicate connection failure
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close

        return False
    
    def execute_query(self,query, param):
        try:
            with self.cursor as cursor:
                cursor.execute(query, param)

                result = cursor.fetchall()

                if result:
                    print("result: " + result)
                else:
                    print("no results")

        except mysql.connector.Error as err:
            print(err)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")




        