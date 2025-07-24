import sys
from task1 import create_table
# from task1_1 import drop_table
from task2 import add_employee
# from task2_2 import truncate_table
from task3 import show_employees
from task4 import generate_and_insert_data
from task5 import find_employees
connection = 0
def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print("Select mode: ")
        print("1 - Create an employee table")
        # print("11 - Drop an employee table")
        print("2 - Add an employee table")
        print("3 - Show employees")
        # print("33 - Truncate table")
        print("4 - Generate 1.000.000 records")
        print("5 - Search for employees by filter")
        mode = input("Enter the mode number: ")
    try:
        if mode == "1":
            create_table()
        # elif mode == "11":
        #     drop_table()
        elif mode == "2":
            if len(sys.argv) > 4:
                full_name = sys.argv[2]
                birth_date = sys.argv[3]
                gender = sys.argv[4]
                add_employee(full_name, birth_date, gender)
            else:
                print("\nAdding a new employee")
                full_name = input("Enter full name: ")
                birth_date = input("Enter birth date: ")
                gender = input("Enter gender (М/Ж): ")
                add_employee(full_name, birth_date, gender)
        elif mode == "3":
            show_employees()
        # elif mode == "33":
        #     truncate_table()
        elif mode == "4":
            generate_and_insert_data()
        elif mode =="5":
            find_employees()
        else:
            print("Incorrect operation mode")
    except Exception as err:
        print("[INFO] Error while working with PostgreSQL", err)

if __name__ == "__main__":
    main()

