
import asyncio
import aioslite
from mysql.connector.aio import connect



async def connection(func):

    async def wrapper(*args, **kwargs):

        try:
            conn = await connect(
                host="localhost",
                user="yourusername",
                password="yourpassword"
            )

            result = await func(conn, *args, **kwargs)

            return result
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    return wrapper


@connection
async def async_fetch_users():
    try:
        cursor = conn.cursor()

        query = "SELECT * FROM USERS"

        await cursor.execute(query)

        users = cursor.fetchall()

        return users
    finally:
        if cursor:
            await cursor.close() # Ensure cursor is closed




@connection
async def async_fetch_older_users():
    try:
        cursor = conn.cursor()

        await cursor.execute("SELECT id, name, age FROM USERS WHERE age > %s", (40,))

        older_users = cursor.fetchall()

        return older_users
    finally:
        if cursor:
            await cursor.close() # Ensure cursor is closed




async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    asyncio.run(connection())
    asyncio.run(fetch_concurrently())