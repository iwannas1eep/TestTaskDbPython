import psycopg2
from datetime import datetime
from config import host, user, password, db_name
from tabulate import tabulate

def show_employees():
    try:
        connection = psycopg2.connect( host=host, user=user, password=password, database=db_name)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT ON (full_name, birth_date) 
                    full_name, 
                    birth_date, 
                    gender
                FROM employees
                ORDER BY full_name, birth_date
            """)

            headers = ["Full Name", "Birthday", "Gender", "Age"]
            table_data = []

            for record in cursor.fetchall():
                full_name, birth_date, gender = record
                age = calculate_age(birth_date)
                table_data.append([
                    full_name,
                    birth_date.strftime("%d-%m-%Y"),
                    gender,
                    age
                ])
            print("\n\t\t\t\tList of employees")
            print(tabulate(table_data, headers=headers, tablefmt="simple_grid", stralign="left"))

    except Exception as err:
        print("\n[INFO] Error while working with PostgreSQL", err)
    finally:
        if connection:
            connection.close()
            print("\n[INFO] PostgreSQL connection is closed")


def calculate_age(birth_date):
    today = datetime.now().date()
    age = today.year - birth_date.year
    return age

if __name__ == "__main__":
    show_employees()