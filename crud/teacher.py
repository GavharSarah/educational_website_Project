import csv
import os

DATA_FOLDER = 'data'
USERS_FILE = os.path.join(DATA_FOLDER, 'users.csv')
COURSES_FILE = os.path.join(DATA_FOLDER, 'courses_list.csv')
PURCHASED_FILE = os.path.join(DATA_FOLDER, 'purchased_courses.csv')


class Teacher:
    def __init__(self, user):
        self.user = user

    def menu(self):
        while True:
            print(f"\nWelcome {self.user[3]}")
            print("""1. Add new course
2. View my courses
3. Update course price
4. View who purchased my courses
5. Logout""")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_course()
            elif choice == "2":
                self.view_my_courses()
            elif choice == "3":
                self.update_course_price()
            elif choice == "4":
                self.view_purchases()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    def add_course(self):
        title = input("Enter course name: ")
        try:
            price = float(input("Enter course price: "))
        except ValueError:
            print("Invalid price. Please enter a number.")
            return


        courses = []
        if os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, 'r') as file:
                courses = list(csv.reader(file))
        course_id = str(len(courses) + 1)


        with open(COURSES_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([course_id, title, self.user[0], price])
        print("Course added successfully!")

    def view_my_courses(self):
        print("\nYour Courses:")
        found = False
        if os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2] == self.user[0]:
                        print(f"ID: {row[0]} - {row[1]} (${row[3]})")
                        found = True
        if not found:
            print("You have no courses.")

    def update_course_price(self):
        courses = []
        if os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, 'r') as file:
                courses = list(csv.reader(file))


        teacher_courses = [c for c in courses if c[2] == self.user[0]]
        if not teacher_courses:
            print("You have no courses to update.")
            return

        for course in teacher_courses:
            print(f"ID: {course[0]} - {course[1]} (${course[3]})")

        course_id = input("Enter course ID to update price: ")
        try:
            new_price = float(input("Enter new price: "))
        except ValueError:
            print("Invalid price. Please enter a number.")
            return


        for i, course in enumerate(courses):
            if course[0] == course_id and course[2] == self.user[0]:
                courses[i][3] = str(new_price)
                break
        else:
            print("Course not found or you are not the instructor.")
            return

        with open(COURSES_FILE, 'w', newline='') as file:
            csv.writer(file).writerows(courses)
        print("Price updated successfully.")

    def view_purchases(self):
        print("\nPurchased by Students:")
        found = False
        if os.path.exists(PURCHASED_FILE) and os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, 'r') as file:
                courses = {c[0]: c[1] for c in csv.reader(file) if c[2] == self.user[0]}

            with open(PURCHASED_FILE, 'r') as file:
                for row in csv.reader(file):
                    user_email, course_id = row
                    if course_id in courses:
                        print(f"{user_email} purchased your course: {courses[course_id]}")
                        found = True
        if not found:
            print("No purchases found for your courses.")