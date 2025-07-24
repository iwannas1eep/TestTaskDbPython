import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta
from task2 import Employee
import time


class DataGenerator:
    def __init__(self):
        self.fake = Faker('ru_RU')
        self.genders = ['Мужской', 'Женский']
        self.first_letters = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ'

        self.name_cache = {
            'Мужской': {
                'last_names': [self.fake.last_name_male() for _ in range(1000)],
                'first_names': [self.fake.first_name_male() for _ in range(1000)],
                'middle_names': [self.fake.middle_name_male() for _ in range(1000)]
            },
            'Женский': {
                'last_names': [self.fake.last_name_female() for _ in range(1000)],
                'first_names': [self.fake.first_name_female() for _ in range(1000)],
                'middle_names': [self.fake.middle_name_female() for _ in range(1000)]
            }
        }

    def generate_employee(self, gender=None, first_letter=None):
        if gender is None:
            gender = random.choice(self.genders)
        if first_letter is None:
            first_letter = random.choice(self.first_letters)

        last_names = [ln for ln in self.name_cache[gender]['last_names']
                      if ln[0].upper() == first_letter]
        first_name = random.choice(self.name_cache[gender]['first_names'])
        middle_name = random.choice(self.name_cache[gender]['middle_names'])

        if not last_names:
            last_name = first_letter + self.fake.last_name_male()[1:]
        else:
            last_name = random.choice(last_names)

        full_name = f"{last_name} {first_name} {middle_name}"

        end_date = datetime.now() - timedelta(days=365 * 18)
        start_date = end_date - timedelta(days=365 * 47)
        birth_date = self.fake.date_between(start_date=start_date, end_date=end_date)

        return Employee(full_name=full_name,birth_date=birth_date.strftime('%d-%m-%Y'),gender=gender)

    def generate_batch(self, size, gender=None, first_letter=None):
        return [self.generate_employee(gender, first_letter) for _ in range(size)]

def generate_and_insert_data():
    try:
        generator = DataGenerator()
        batch_size = 10000
        total_records = 1000000
        batches = total_records // batch_size

        print(f"Generating {total_records+100} employees...")
        start_time = time.time()

        for i in range(batches):
            employees = generator.generate_batch(batch_size)
            Employee.batch_insert(employees)
            print(f"Batch {i + 1}/{batches} inserted ({len(employees)} records)")

        print(f"Adding 100 'Ф' males...")
        male_f_employees = generator.generate_batch(100, gender='Мужской', first_letter='Ф')
        Employee.batch_insert(male_f_employees)

        total_time = time.time() - start_time
        print(f"\nTotal: {total_records + 100} records")
        print(f"Time: {total_time // 60} min {total_time % 60:.2f} sec")

    except Exception as err:
        print("[INFO]Error:", err)
    finally:
        print("[INFO] PostgreSQL connection is closed")

if __name__ == "__main__":
    generate_and_insert_data()