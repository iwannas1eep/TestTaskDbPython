import psycopg2
import time
from config import host, user, password, db_name
from tabulate import tabulate

def find_employees():
    try:
        print("\nSelecting search parameters:")

        gender_input = input("Enter gender (Мужской/Женский): ").strip().capitalize()
        while gender_input not in ['Мужской', 'Женский']:
            print("[WARNING] Use 'Мужской' or 'Женский'")
            gender_input = input("Enter gender (Мужской/Женский): ").strip().capitalize()

        letter = input("Enter the first letter of your surname: ").strip().upper()
        while len(letter) != 1 or letter not in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
            print("[WARNING] Enter one Russian letter")
            letter = input("Enter the first letter of your surname: ").strip().upper()

        connection = psycopg2.connect(host=host,user=user,password=password,database=db_name)

        start_time = time.time()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, full_name, birth_date, gender 
                FROM employees 
                WHERE gender = %s AND full_name LIKE %s
            """, (gender_input, f'{letter}%'))

            results = cursor.fetchall()
            execution_time = time.time() - start_time

            headers = ["ID", "ФИО", "Дата рождения", "Пол"]
            table_data = []

            for row in results:
                table_data.append([row[0], row[1], row[2].strftime("%d-%m-%Y"), row[3]])

            print(f"\nResults ({gender_input} with surname beginning with the letter “{letter}”)):")
            if table_data:
                print(tabulate(table_data, headers=headers, tablefmt="simple_grid", stralign= "left"))
            else:
                print("No matches found")

            print(f"\nExecution time: {execution_time:.4f} seconds")
            print(f"Records found: {len(results)}")

    except Exception as err:
        print(f"[INFO] Error: {err}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    find_employees()