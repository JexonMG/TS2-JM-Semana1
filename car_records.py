import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname='CarRegistry',
    user='postgres',
    password='1234',
    host='localhost',
    port='5432'
)
cur = conn.cursor()


def add_entry(brand, entry_time):
    query = "INSERT INTO car_records (brand, entry_time) VALUES (%s, %s)"
    cur.execute(query, (brand, entry_time))
    conn.commit()

def get_history():
    cur.execute("SELECT brand, entry_time, exit_time FROM car_records")
    records = cur.fetchall()
    for record in records:
        brand, entry_time, exit_time = record
        formatted_entry_time = entry_time.strftime('%Y-%m-%d %H:%M:%S') if entry_time else None
        formatted_exit_time = exit_time.strftime('%Y-%m-%d %H:%M:%S') if exit_time else None
        print(brand, "Entry: ", formatted_entry_time, "Exit: ", formatted_exit_time)

def exit_time():
    cur.execute("SELECT id, brand FROM car_records WHERE exit_time IS NULL")
    records = cur.fetchall()
    for record in records:
        print(record)
    car_id = int(input("Enter ID of car that left: "))
    current_time = datetime.now()
    cur.execute("UPDATE car_records SET exit_time = %s WHERE id = %s", (current_time, car_id))
    conn.commit()
    print("Exit time updated successfully!")

while True:
    choice = input("\n1. Add Entry\n2. View History\n3. Exit Time\n4. Exit\nChoose (1/2/3/4): ")

    if choice == '1':
        print()
        print()
        brand = input("Enter car brand: ")
        entry_time = datetime.now()
        add_entry(brand, entry_time)
        print("Entry added successfully!")

    elif choice == '2':
        print()
        print()
        print("History of entries and exit:\n ")  
        get_history()

    elif choice == '3':
        print()
        print()
        print("Cars that haven't left yet:\n ")
        exit_time()

    elif choice == '4':
        break

cur.close()
conn.close()