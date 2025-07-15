import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword"
)


class DatabaseConnection:

    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None


    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("Database connection established.")

            return self.cursor
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")

            # Re-raise the exception to indicate connection failure
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
            print("Cursor closed.")
        if self.connection:
            # Commit any pending transactions if no exception occurred
            if exc_type is None:
                self.connection.commit()
                print("Changes committed.")
            else:
                # Rollback if an exception occurred
                self.connection.rollback()
                print("Transaction rolled back due to error.")
            self.connection.close()
            print("Database connection closed.")

        return False
    
try:
    with DatabaseConnection(mydb) as cursor:
        # The specified query
        query_string = "SELECT * FROM users"
        cursor.execute(query_string)

        # Fetch and print the results
        # cursor.fetchall() retrieves all rows as a list of tuples
        results = cursor.fetchall()

        if results:
            print("\nQuery Results:")
            for row in results:
                print(row)
        else:
            print("\nNo results found for the query.")

except mysql.connector.Error as err:
    print(f"Error during query execution: {err}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")