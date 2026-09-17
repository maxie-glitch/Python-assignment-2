import sqlite3
connection = sqlite3.connect("students.db")
cursor = connection.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
""")

# Insert some data
students_data = [
    ("Rumbidzai", 20),
    ("Fadzai", 25),
    ("Viterlix", 22)
]
cursor.executemany("INSERT INTO students (name, age) VALUES (?, ?)", students_data)
connection.commit()

# Retrieve and display the data
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

print("Students table contents:")
for row in rows:
    print(row)

connection.close()

## Question 2: Encapsulation — BankAccount Class##
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # private attribute (name-mangled to _BankAccount__balance)

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.__balance += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self.__balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.__balance:
            print("Insufficient funds.")
            return
        self.__balance -= amount
        print(f"Withdrew ${amount:.2f}. New balance: ${self.__balance:.2f}")

    def display_balance(self):
        print(f"Current balance for {self.owner}: ${self.__balance:.2f}")


# Demonstration
account = BankAccount("Fadzai", 530)
account.display_balance()
account.deposit(66)
account.withdraw(90)
account.withdraw(900)   # insufficient funds

# Direct access is blocked/hidden:
# print(account.__balance)        # AttributeError
print(account._BankAccount__balance)  # 120.0 — shows name mangling, but you shouldn't rely on this

## Question 3: Client-Server Program with Sockets##
import socket

def start_server(host="127.0.0.1", port=65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(1)
            print(f"Server listening on {host}:{port}...")

            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    print(f"Received message: {data.decode('utf-8')}")
                else:
                    print("No data received.")

    except OSError as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    start_server()
import socket

def start_client(host="127.0.0.1", port=65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            message = "Hello from client!"
            client_socket.sendall(message.encode("utf-8"))
            print(f"Sent: {message}")

    except ConnectionRefusedError:
        print("Connection failed: is the server running?")
    except OSError as e:
        print(f"Client error: {e}")

if __name__ == "__main__":
    start_client()

    ## Question 4: Random Floats — Minimum and Maximum##
import random

# Generate 5 random floating-point numbers between 0 and 10
numbers = [random.uniform(0, 10) for _ in range(5)]

print("Generated numbers:", [round(n, 3) for n in numbers])
print("Minimum value:", round(min(numbers), 3))
print("Maximum value:", round(max(numbers), 3))

## Question 5: Abstract Base Class — FileHandler##
from abc import ABC, abstractmethod

class FileHandler(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass


class TextFileHandler(FileHandler):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, "r") as f:
            content = f.read()
        print(f"Text content read from {self.filename}:\n{content}")
        return content

    def write(self, data):
        with open(self.filename, "w") as f:
            f.write(data)
        print(f"Text data written to {self.filename}.")


class BinaryFileHandler(FileHandler):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, "rb") as f:
            content = f.read()
        print(f"Binary content read from {self.filename}: {len(content)} bytes")
        return content

    def write(self, data):
        with open(self.filename, "wb") as f:
            f.write(data)
        print(f"Binary data written to {self.filename}.")


# Demonstration
text_handler = TextFileHandler("notes.txt")
text_handler.write("Hello, this is a text file.")
text_handler.read()

binary_handler = BinaryFileHandler("data.bin")
binary_handler.write(b"\x00\x01\x02\x03")
binary_handler.read()

# Attempting to instantiate the abstract class directly fails:
# handler = FileHandler()   # TypeError: Can't instantiate abstract class

## Question 6: Class Hierarchy — Vehicle, Car, Bike##
class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def describe(self):
        print(f"{self.brand} is a vehicle that can travel at {self.speed} km/h.")


class Car(Vehicle):
    def __init__(self, brand, speed, doors):
        super().__init__(brand, speed)
        self.doors = doors

    def describe(self):  # overriding the base class method
        print(f"{self.brand} is a car with {self.doors} doors, travelling at {self.speed} km/h.")


class Bike(Vehicle):
    def __init__(self, brand, speed, has_gears):
        super().__init__(brand, speed)
        self.has_gears = has_gears

    def describe(self):  # overriding the base class method
        gear_text = "with gears" if self.has_gears else "single-speed"
        print(f"{self.brand} is a {gear_text} bike, travelling at {self.speed} km/h.")


# Demonstration
vehicles = [
    Vehicle("Tractor", 50),
    Car("Toyota Aqua", 140, 4),
    Bike("Cargo Bike", 40, True),
]

for v in vehicles:
    v.describe()
