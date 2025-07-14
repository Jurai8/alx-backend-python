
import sqlite3 
import functools
from contextlib import contextmanager
import mysql.connector
import time


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
    
    return wrapper

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    result = func(*args, **kwargs) 
                    return result 
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts}/{retries} failed for {func.__name__}: {e}")
                    if attempts < retries:
                        print(f"Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed for {func.__name__}.")
                        raise 
        return wrapper
    return decorator
                
   
@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)