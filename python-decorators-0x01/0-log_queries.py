
import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""
def log_queries(func):
    def wrapper(*args):
        print(f"log query: { args }")


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")