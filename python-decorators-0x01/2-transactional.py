import sqlite3 
import functools

"""your code goes here"""

import sqlite3 
import functools
from contextlib import contextmanager
import mysql.connector

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        mydb
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

def transactional(func):
    def transaction(*args, **kwargs):
        conn = args[0]
        try:
            conn.autocommit = False
            print("Transaction started (autocommit disabled).")

            result = func(*args, **kwargs)

            conn.commit()
            print(f"Transaction for '{func.__name__}' committed successfully.")
            return result
        
        except Exception as e:
            if conn: # Ensure conn exists before trying to rollback
                conn.rollback()
                print(f"Transaction for '{func.__name__}' rolled back due to error: {e}")
            raise

    return transaction


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
