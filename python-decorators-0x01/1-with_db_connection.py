import sqlite3 
import functools
from contextlib import contextmanager
import mysql.connector

def with_db_connection(func):
    def wrapper(*args, **kwargs):
       
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="yourusername",
                password="yourpassword"
            )

            result = func(mydb, *args, **kwargs)
            return result
        
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
    
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        finally:
            if mydb:
                mydb.close()
                print("Database connection closed.")


@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
    #### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)