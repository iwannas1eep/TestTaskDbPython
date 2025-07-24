import psycopg2
from config import host, user, password, db_name

def create_table():
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    birth_date DATE NOT NULL,
                    gender VARCHAR(10) NOT NULL)
                    """)
            connection.commit()
            print("The 'employees' table was successfully created")
    except Exception as err:
        print("[INFO] Error while working with PostgreSQL",err)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection is closed")