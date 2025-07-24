import psycopg2
from config import host, user, password, db_name

def drop_table():
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cursor:
            cursor.execute("""
                DROP TABLE  employees
                    """)
            connection.commit()
            print("The 'employees' table was successfully deleted")
    except Exception as err:
        print("[INFO] Error while working with PostgreSQL",err)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection is closed")