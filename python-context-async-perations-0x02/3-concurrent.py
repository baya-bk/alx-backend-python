import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)


async def fetch_concurrently():
    """Run both queries concurrently."""
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
