from sqlalchemy import text

from app.database.connection import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database Connected Successfully!")
        print("Result:", result.scalar())

except Exception as e:
    print("Database Connection Failed!")
    print(e)