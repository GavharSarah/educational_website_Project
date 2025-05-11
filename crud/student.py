
import csv
import os

DATA_FOLDER = 'data'
USERS_FILE = os.path.join(DATA_FOLDER, 'users.csv')
COURSES_FILE = os.path.join(DATA_FOLDER, 'courses_list.csv')
PURCHASED_FILE = os.path.join(DATA_FOLDER, 'purchased_courses.csv')

class Student:
    def __init__(self, user):
        self.user = user

    def menu(self):
        while True:
            print(f"\nWelcome {self.user[3]}")
            print("""
1. Show my courses
2. Purchase a course
3. Show balance
4. Logout
""")
            choice = input("Choose: ")
            if choice == '1':
                self.show_courses()
            elif choice == '2':
                self.buy_course()
            elif choice == '3':
                print(f"Balance: ${self.user[4]}")
            elif choice == '4':
                break
            else:
                print("Invalid choice.")

    def show_courses(self):
        if not self.user[5]:
            print("You have not purchased any courses.")
            return
        ids = self.user[5].split('|')
        with open(COURSES_FILE, 'r') as f:
            for row in csv.reader(f):
                if row[0] in ids:
                    print(f"{row[1]} by {row[2]}")

    def buy_course(self):
        with open(COURSES_FILE, 'r') as f:
            courses = list(csv.reader(f))
        for row in courses:
            print(f"{row[0]}. {row[1]} - ${row[3]}")
        course_id = input("Enter course ID to purchase: ")

        course = next((c for c in courses if c[0] == course_id), None)
        if not course:
            print("Course not found.")
            return

        price = float(course[3])
        balance = float(self.user[4])
        if balance < price:
            print("Insufficient balance.")
            return

        self.user[4] = str(balance - price)
        self.user[5] = self.user[5] + '|' + course_id if self.user[5] else course_id
        self.save_user()

        with open(PURCHASED_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([self.user[0], course_id])

        print("Course purchased successfully.")

    def save_user(self):
        with open(USERS_FILE, 'r') as f:
            users = list(csv.reader(f))
        for i, u in enumerate(users):
            if u[0] == self.user[0]:
                users[i] = self.user
                break
        with open(USERS_FILE, 'w', newline='') as f:
            csv.writer(f).writerows(users)














