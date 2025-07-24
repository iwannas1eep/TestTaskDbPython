import psycopg2
from datetime import datetime
from config import host, user, password, db_name
from psycopg2 import extras
import sys

class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def calculate_age(self):
        today = datetime.now()
        birth = datetime.strptime(self.birth_date, "%d-%m-%Y")
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age

    def insert_into_db(self):
        try:
            conn = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            cursor = conn.cursor()
            query = "INSERT INTO employees (full_name, birth_date, gender) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.full_name, datetime.strptime(self.birth_date, "%d-%m-%Y").date(), self.gender))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("Insert error:", e)

    @classmethod
    def batch_insert(self, employees):
        try:
            conn = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            cursor = conn.cursor()

            values = [
                (e.full_name, datetime.strptime(e.birth_date, "%d-%m-%Y").date(), e.gender)
                for e in employees
            ]

            insert_query = """
                INSERT INTO employees (full_name, birth_date, gender)
                VALUES %s
            """

            extras.execute_values(cursor, insert_query, values, page_size=10000)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("Batch insert error:", e)

def add_employee(full_name, birth_date, gender):
    try:
        employee = Employee(full_name, birth_date, gender)
        age = employee.calculate_age()
        employee_id = employee.save_to_db()
        print("\nEmployee information:")
        print("ID: ", employee_id)
        print("Full name: ", employee.full_name)
        print("Birth date: ", employee.birth_date)
        print("Gender: ", employee.gender)
        print("Age: ", age)
        return employee_id

    except Exception as er:
        print("[INFO] Error adding an employee", er)
        raise

if __name__ == "__main__":
    if len(sys.argv) > 3:
        add_employee(sys.argv[1], sys.argv[2], sys.argv[3])