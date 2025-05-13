
import csv
import hashlib
import os
from crud.student import Student
from crud.teacher import Teacher

DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "users.csv")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as file:
        reader = csv.reader(file)
        return list(reader)


def save_user(user):
    users = load_users()
    users.append(user)
    with open(USERS_FILE, 'w', newline='') as file:
        csv.writer(file).writerows(users)


def login():
    user_email = input("Your email: ")
    password = input("Your password: ")
    hashed_password = hash_password(password)
    users = load_users()
    for user in users:
        if user[0] == user_email and user[1] == hashed_password:
            print(f'Login successful! Welcome, {user[3].capitalize()} ({user[2]})')
            return user
    print('Login failed')
    return None


def register():
    email = input("Enter your email: ")
    users = load_users()
    if any(user[0] == email for user in users):
        print("Email already exists.")
        return None

    password = input("Enter your password: ")
    hashed_password = hash_password(password)
    name = input("Enter your name: ")
    role = input("Enter role (student/teacher): ").lower()
    if role not in ['student', 'teacher']:
        print("Invalid role. Use 'student' or 'teacher'.")
        return None

    balance = "100.00"
    purchased_ids = ""
    user = [email, hashed_password, role, name, balance, purchased_ids]
    save_user(user)
    print("Registration successful! You can now log in.")
    return user


def main():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    while True:
        print("\nWelcome to the Educational Website Project")
        print("1. Login")
        print("2. Register")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = login()
            if user:
                role = user[2].lower()
                if role == 'student':
                    student = Student(user)
                    student.menu()
                elif role == 'teacher':
                    teacher = Teacher(user)
                    teacher.menu()
                else:
                    print("Invalid role found in user data.")
        elif choice == "2":
            register()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")


if __name__ == '__main__':
    main()
