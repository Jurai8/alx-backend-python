import time
import sqlite3 
import functools


query_cache = {}

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

def cache_query(func):
    @functools.wraps(func) 
    def wrapper(*args, **kwargs):
        query_string = kwargs.get('query')

        if query_string is None:
            print("Cache: Warning - 'query' keyword argument not found.")
            return func(*args, **kwargs) # Call original func without caching

        if query_string in query_cache:
            print(f"Cache: HIT for query: '{query_string}'")
            return query_cache[query_string] # Return the actual cached result
        else:
            print(f"Cache: MISS for query: '{query_string}'. Executing function...")
            result = func(*args, **kwargs)
            query_cache[query_string] = result # Store the actual result
            print(f"Cache: Stored result for query: '{query_string}'")
            return result
        
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")